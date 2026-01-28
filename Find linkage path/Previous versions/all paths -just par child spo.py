import sqlite3
from collections import deque, defaultdict

# ---------------------------------------------------------
# Graph construction
# ---------------------------------------------------------

def load_graph(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # graph[node] = list of (neighbor, relationship_type, role)
    graph = defaultdict(list)

    # -----------------------------------------------------
    # FANTypeTable: association labels and roles
    # -----------------------------------------------------
    cur.execute("""
        SELECT FANTypeID, Name, Role1, Role2
        FROM FANTypeTable
    """)
    fan_types = {
        ftid: {"name": name, "role1": role1, "role2": role2}
        for ftid, name, role1, role2 in cur.fetchall()
    }

    # -----------------------------------------------------
    # FamilyTable + ChildTable: parent/child + spouse
    # -----------------------------------------------------
    cur.execute("""
        SELECT f.FatherID, f.MotherID, c.ChildID
        FROM FamilyTable f
        JOIN ChildTable c ON c.FamilyID = f.FamilyID
    """)
    for father, mother, child in cur.fetchall():
        # father ↔ child
        if father and father > 0 and child and child > 0:
            graph[father].append((child, "parent", None))
            graph[child].append((father, "child", None))
        # mother ↔ child
        if mother and mother > 0 and child and child > 0:
            graph[mother].append((child, "parent", None))
            graph[child].append((mother, "child", None))
        # spouse ↔ spouse
        if father and father > 0 and mother and mother > 0:
            graph[father].append((mother, "spouse", None))
            graph[mother].append((father, "spouse", None))

    # -----------------------------------------------------
    # FANTable: associations with roles from FANTypeTable
    # -----------------------------------------------------
    cur.execute("""
        SELECT ID1, ID2, FanTypeID
        FROM FANTable
        WHERE ID1 > 0 AND ID2 > 0
    """)
    for id1, id2, fan_type_id in cur.fetchall():
        info = fan_types.get(fan_type_id)
        if info:
            assoc_name = info["name"]
            role1 = info["role1"]
            role2 = info["role2"]
        else:
            assoc_name = f"Type {fan_type_id}"
            role1 = None
            role2 = None

        label = f"association:{assoc_name}"
        # id1 → id2
        graph[id1].append((id2, label, role1))
        # id2 → id1
        graph[id2].append((id1, label, role2))

    # -----------------------------------------------------
    # Shared facts: EventTable + WitnessTable + RoleTable + FactTypeTable
    # -----------------------------------------------------

    # FactTypeTable: FactTypeID → fact name
    cur.execute("""
        SELECT FactTypeID, Name
        FROM FactTypeTable
    """)
    fact_type_lookup = {ftid: name for ftid, name in cur.fetchall()}

    # RoleTable: RoleID → RoleName
    cur.execute("""
        SELECT RoleID, RoleName
        FROM RoleTable
    """)
    role_lookup = {rid: rname for rid, rname in cur.fetchall()}

    # EventTable: EventID → (OwnerID, EventTypeID)
    cur.execute("""
        SELECT EventID, OwnerID, EventType
        FROM EventTable
        WHERE OwnerID > 0
    """)
    event_principals = {}
    event_type_name = {}
    for event_id, owner_id, event_type_id in cur.fetchall():
        event_principals.setdefault(event_id, set()).add(owner_id)
        event_type_name[event_id] = fact_type_lookup.get(
            event_type_id, f"Type {event_type_id}"
        )

    # WitnessTable: EventID → (PersonID, RoleName)
    cur.execute("""
        SELECT EventID, PersonID, Role
        FROM WitnessTable
        WHERE PersonID > 0
    """)
    event_witnesses = defaultdict(list)
    for event_id, person_id, role_id in cur.fetchall():
        role_name = role_lookup.get(role_id, "Witness")
        event_witnesses[event_id].append((person_id, role_name))

    # Build EventID → list of (PersonID, RoleName, FactName)
    event_people = defaultdict(list)

    # Principals
    for event_id, owners in event_principals.items():
        fact_name = event_type_name.get(event_id, "Fact")
        for owner in owners:
            event_people[event_id].append((owner, "Principal", fact_name))

    # Witnesses
    for event_id, plist in event_witnesses.items():
        fact_name = event_type_name.get(event_id, "Fact")
        for person_id, role_name in plist:
            event_people[event_id].append((person_id, role_name, fact_name))

    # Add shared-fact edges
    for event_id, people in event_people.items():
        for i in range(len(people)):
            for j in range(i + 1, len(people)):
                p1, role1, fact_name = people[i]
                p2, role2, _ = people[j]
                label = f"shared_fact:{fact_name}"
                # p1 → p2
                graph[p1].append((p2, label, role1))
                # p2 → p1
                graph[p2].append((p1, label, role2))

    return graph, conn


# ---------------------------------------------------------
# BFS shortest path (single path)
# ---------------------------------------------------------

def bfs_shortest_path(graph, start, target):
    if start == target:
        return [start]
    visited = {start}
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbor, _rel, _role in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                if neighbor == target:
                    return new_path
                queue.append(new_path)
    return None


# ---------------------------------------------------------
# DFS all simple paths
# ---------------------------------------------------------

def find_all_paths(graph, start, target, max_depth=20):
    """
    Returns all simple paths from start → target.
    max_depth prevents runaway recursion in very large graphs.
    """
    all_paths = []
    visited = set()

    def dfs(node, path):
        if len(path) > max_depth:
            return
        if node == target:
            all_paths.append(path.copy())
            return

        visited.add(node)
        for neighbor, _rel, _role in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor])
        visited.remove(node)

    dfs(start, [start])
    return all_paths


# ---------------------------------------------------------
# Name lookup (primary name via NameTable.IsPrimary = 1)
# ---------------------------------------------------------

def get_names(conn, person_ids):
    if not person_ids:
        return []
    cur = conn.cursor()
    q = f"""
        SELECT OwnerID, Surname, Given
        FROM NameTable
        WHERE IsPrimary = 1
          AND OwnerID IN ({','.join('?' for _ in person_ids)})
    """
    cur.execute(q, person_ids)
    rows = {
        pid: f"{given} {surname}".strip()
        for pid, surname, given in cur.fetchall()
    }
    return [rows.get(pid, f"[{pid}]") for pid in person_ids]


# ---------------------------------------------------------
# Relationship table builder (for a single path)
# ---------------------------------------------------------

def build_relationship_table(graph, path, names):
    table = []
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]

        rel, role = "unknown", None
        for nbr, r, rl in graph[a]:
            if nbr == b:
                rel = r
                role = rl
                break

        assoc_name = None
        shared_fact_name = None
        if rel.startswith("association:"):
            assoc_name = rel.split(":", 1)[1]
        elif rel.startswith("shared_fact:"):
            shared_fact_name = rel.split(":", 1)[1]

        table.append({
            "from_id": a,
            "to_id": b,
            "from_name": names[i],
            "to_name": names[i + 1],
            "relationship": rel,
            "association_name": assoc_name,
            "shared_fact_name": shared_fact_name,
            "role": role,
        })
    return table


# ---------------------------------------------------------
# Build relationship tables for all paths
# ---------------------------------------------------------

def build_all_relationship_tables(graph, all_paths, conn):
    """
    For each path in all_paths, build:
      - names list
      - relationship table
    Returns a list of (path, names, table) tuples.
    """
    results = []
    for path in all_paths:
        names = get_names(conn, path)
        table = build_relationship_table(graph, path, names)
        results.append((path, names, table))
    return results


# ---------------------------------------------------------
# Main APIs
# ---------------------------------------------------------

def find_relationship_path(db_path, start_id, target_id):
    graph, conn = load_graph(db_path)
    path = bfs_shortest_path(graph, start_id, target_id)
    if not path:
        return None, None, None
    names = get_names(conn, path)
    table = build_relationship_table(graph, path, names)
    return path, names, table


def find_all_relationship_paths(db_path, start_id, target_id, max_depth=20):
    graph, conn = load_graph(db_path)
    all_paths = find_all_paths(graph, start_id, target_id, max_depth=max_depth)
    all_tables = build_all_relationship_tables(graph, all_paths, conn)
    return all_tables


# ---------------------------------------------------------
# Example usage against your test DB
# ---------------------------------------------------------

if __name__ == "__main__":
    DB_PATH = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Find linkage path\DB\TEST-Find linkage path.rmtree"

    # Single shortest path
    path, names, table = find_relationship_path(DB_PATH,  3, 21121)
    print("Shortest path IDs:", path)
    print("Shortest path names:", " → ".join(names) if names else None)
    print("\nShortest path relationship table:")
    if table:
        print(f"{'from':>6} {'to':>6}  {'relationship':>22}  {'assoc_name':>15}  {'shared_fact':>15}  {'role':>12}  from_name → to_name")
        for row in table:
            print(
                f"{row['from_id']:6} {row['to_id']:6}  {row['relationship']:>22}  "
                f"{str(row['association_name']):>15}  {str(row['shared_fact_name']):>15}  {str(row['role']):>12}  "
                f"{row['from_name']} → {row['to_name']}"
            )
    else:
        print("No relationship found.")

    # All paths
    print("\n\nALL PATHS:")
    all_results = find_all_relationship_paths(DB_PATH, 3, 21121, max_depth=5)
    print(f"Found {len(all_results)} paths.\n")

    for idx, (path, names, table) in enumerate(all_results, start=1):
        print(f"Path #{idx}: IDs   :", path)
        print(f"Path #{idx}: Names :", ' → '.join(names))
        print(f"Path #{idx}: Relationship table:")
        if table:
            print(f"{'from':>6} {'to':>6}  {'relationship':>22}  {'assoc_name':>15}  {'shared_fact':>15}  {'role':>12}  from_name → to_name")
            for row in table:
                print(
                    f"{row['from_id']:6} {row['to_id']:6}  {row['relationship']:>22}  "
                    f"{str(row['association_name']):>15}  {str(row['shared_fact_name']):>15}  {str(row['role']):>12}  "
                    f"{row['from_name']} → {row['to_name']}"
                )
        else:
            print("  (no edges?)")
        print()
