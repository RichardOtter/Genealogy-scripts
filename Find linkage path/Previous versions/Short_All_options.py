# =========================================================
#  SECTION 1 — Imports and Defaults
# =========================================================

import sqlite3
from collections import deque, defaultdict

# Default: genealogical edges only
DEFAULT_ALLOWED_TYPES = {
    "parent": True,
    "child": True,
    "spouse": True,
    "association": False,
    "shared_fact": False,
}

DB_PATH = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Find linkage path\DB\TEST-Find linkage path.rmtree"

    # Example: genealogical edges only, shortest path + all paths
allowed = {
        "parent": True,
        "child": True,
        "spouse": True,
        "association": False,
        "shared_fact": False,
    }

def main():
    result = find_paths(
        DB_PATH,
        start_id=1,
        target_id=17,
        allowed_types=allowed,
        allpaths=True,
        max_depth=12,
    )

    shortest = result["shortest_path"]
    all_paths = result["all_paths"]

    print("=== SHORTEST PATH ===")
    if shortest:
        print("IDs   :", shortest["path"])
        print("Names :", " → ".join(shortest["names"]))
        print("Table :")
        print(f"{'from':>6} {'to':>6}  {'relationship':>22}  {'assoc_name':>15}  {'shared_fact':>15}  {'role':>12}  from_name → to_name")
        for row in shortest["table"]:
            print(
                f"{row['from_id']:6} {row['to_id']:6}  {row['relationship']:>22}  "
                f"{str(row['association_name']):>15}  {str(row['shared_fact_name']):>15}  {str(row['role']):>12}  "
                f"{row['from_name']} → {row['to_name']}"
            )
    else:
        print("No shortest path found.")

    print("\n=== ALL PATHS (sorted by length) ===")
    print(f"Total paths: {len(all_paths)}\n")

    for idx, item in enumerate(all_paths, start=1):
        path = item["path"]
        names = item["names"]
        table = item["table"]

        print(f"Path #{idx}: IDs   :", path)
        print(f"Path #{idx}: Names :", " → ".join(names))
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



# =========================================================
#  SECTION 2 — Graph Construction
#     - Family relationships
#     - FAN associations
#     - Shared facts
#     - Roles and fact types
# =========================================================

def load_graph(db_path):
    """
    Build the relationship graph from the RootsMagic DB.

    graph[person_id] = list of (neighbor_id, relationship_label, role)
      relationship_label examples:
        'parent'
        'child'
        'spouse'
        'association:Witness'
        'shared_fact:Census'
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

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
        graph[id1].append((id2, label, role1))
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
                graph[p1].append((p2, label, role1))
                graph[p2].append((p1, label, role2))

    return graph, conn


# =========================================================
#  SECTION 3 — Pathfinding
#     - BFS shortest path (unfiltered)
#     - DFS all paths (filtered by allowed_types)
# =========================================================

def bfs_shortest_path(graph, start, target):
    """
    Unfiltered BFS: considers all relationship types.
    Returns a single shortest path [start, ..., target] or None.
    """
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


def _is_allowed(rel, allowed_types):
    """
    rel: full relationship label, e.g. 'association:Witness'
    allowed_types: dict like {'parent': True, 'association': False}
    """
    base = rel.split(":", 1)[0]
    return allowed_types.get(base, False)


def find_all_paths(graph, start, target, allowed_types, max_depth=20):
    """
    DFS: returns all simple paths from start → target,
    filtered by allowed_types, limited by max_depth.
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
        for neighbor, rel, role in graph[node]:
            if not _is_allowed(rel, allowed_types):
                continue
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor])
        visited.remove(node)

    dfs(start, [start])
    return all_paths


# =========================================================
#  SECTION 4 — Name Lookup
# =========================================================

def get_names(conn, person_ids):
    """
    Returns list of primary names for the given person_ids,
    in the same order as person_ids.
    """
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


# =========================================================
#  SECTION 5 — Relationship Table Builders
#     - Single path
#     - All paths
# =========================================================

def build_relationship_table(graph, path, names):
    """
    Build a relationship table for a single path.
    Each row:
      from_id, to_id, from_name, to_name,
      relationship, association_name, shared_fact_name, role
    """
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


def build_all_relationship_tables(graph, all_paths, conn):
    """
    For each path in all_paths, build:
      - names list
      - relationship table
    Returns a list of dicts:
      {
        "path": [...],
        "names": [...],
        "table": [...]
      }
    """
    results = []
    for path in all_paths:
        names = get_names(conn, path)
        table = build_relationship_table(graph, path, names)
        results.append({
            "path": path,
            "names": names,
            "table": table,
        })
    return results


# =========================================================
#  SECTION 6 — Main API
#     - find_paths(...)
# =========================================================

def find_paths(
    db_path,
    start_id,
    target_id,
    allowed_types=None,
    allpaths=False,
    max_depth=20,
):
    """
    Main entry point.

    Parameters:
      db_path      : path to RootsMagic DB
      start_id     : PersonID start
      target_id    : PersonID target
      allowed_types: dict of booleans for base relationship types
                     (parent, child, spouse, association, shared_fact)
                     If None, DEFAULT_ALLOWED_TYPES is used.
      allpaths     : False → shortest path only (BFS, unfiltered)
                     True  → shortest path + all DFS paths (filtered)
      max_depth    : max depth for DFS when allpaths=True

    Returns:
      {
        "shortest_path": {
            "path": [...],
            "names": [...],
            "table": [...]
        },
        "all_paths": [
            {
                "path": [...],
                "names": [...],
                "table": [...]
            },
            ...
        ]
      }
    """
    if allowed_types is None:
        allowed_types = DEFAULT_ALLOWED_TYPES.copy()

    graph, conn = load_graph(db_path)

    # --- Shortest path (BFS, unfiltered) ---
    shortest_path = bfs_shortest_path(graph, start_id, target_id)
    shortest_result = None

    if shortest_path:
        shortest_names = get_names(conn, shortest_path)
        shortest_table = build_relationship_table(graph, shortest_path, shortest_names)
        shortest_result = {
            "path": shortest_path,
            "names": shortest_names,
            "table": shortest_table,
        }

    # If only shortest path requested, return now
    if not allpaths:
        return {
            "shortest_path": shortest_result,
            "all_paths": [] if shortest_result is None else [shortest_result],
        }

    # --- All paths (DFS, filtered by allowed_types) ---
    dfs_paths = find_all_paths(graph, start_id, target_id, allowed_types, max_depth)

    # Ensure shortest path is included in all_paths, even if DFS filters it out
    all_paths_set = {tuple(p) for p in dfs_paths}
    if shortest_path and tuple(shortest_path) not in all_paths_set:
        dfs_paths.append(shortest_path)

    # Sort all paths by length (shortest first)
    dfs_paths.sort(key=len)

    all_paths_struct = build_all_relationship_tables(graph, dfs_paths, conn)

    return {
        "shortest_path": shortest_result,
        "all_paths": all_paths_struct,
    }


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
