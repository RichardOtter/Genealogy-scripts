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
    # Load FANTypeTable (for association labels and roles)
    # -----------------------------------------------------
    cur.execute("""
        SELECT FANTypeID, Name, Role1, Role2
        FROM FANTypeTable
    """)

    fan_types = {
        ftid: {
            "name": name,
            "role1": role1,
            "role2": role2
        }
        for ftid, name, role1, role2 in cur.fetchall()
    }

    # -----------------------------------------------------
    # Parent-child + spouse edges via FamilyTable / ChildTable
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
    # FANTable associations
    # -----------------------------------------------------
    cur.execute("""
        SELECT ID1, ID2, FanTypeID
        FROM FANTable
        WHERE ID1 > 0 AND ID2 > 0
    """)

    for id1, id2, fan_type_id in cur.fetchall():
        info = fan_types.get(fan_type_id, None)

        if info:
            assoc_name = info["name"]
            role1 = info["role1"]
            role2 = info["role2"]
        else:
            assoc_name = f"Type {fan_type_id}"
            role1 = None
            role2 = None

        label = f"association:{assoc_name}"

        # id1 → id2 (Owner plays Role1)
        graph[id1].append((id2, label, role1))

        # id2 → id1 (Assoc plays Role2)
        graph[id2].append((id1, label, role2))

    return graph, conn


# ---------------------------------------------------------
# BFS shortest path
# ---------------------------------------------------------

def bfs_shortest_path(graph, start, target):
    if start == target:
        return [start]

    visited = set([start])
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
# Name lookup (primary name)
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
# Relationship table builder
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
        if rel.startswith("association:"):
            assoc_name = rel.split(":", 1)[1]

        table.append({
            "from_id": a,
            "to_id": b,
            "from_name": names[i],
            "to_name": names[i + 1],
            "relationship": rel,
            "association_name": assoc_name,
            "role": role
        })

    return table


# ---------------------------------------------------------
# Main API
# ---------------------------------------------------------

def find_relationship_path(db_path, start_id, target_id):
    graph, conn = load_graph(db_path)
    path = bfs_shortest_path(graph, start_id, target_id)

    if not path:
        return None, None, None

    names = get_names(conn, path)
    table = build_relationship_table(graph, path, names)

    return path, names, table


# ---------------------------------------------------------
# Run against your test DB
# ---------------------------------------------------------

DB_PATH = r"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\Find linkage path\DB\TEST-Find linkage path.rmtree"
path, names, table = find_relationship_path(DB_PATH, 1, 14378)

print("Path IDs:", path)
print("Names:", " → ".join(names) if names else None)
print("\nRelationship Table:")
if table:
    print(f"{'from':>6} {'to':>6}  {'relationship':>18}  {'assoc_name':>15}  {'role':>12}  from_name → to_name")
    for row in table:
        print(f"{row['from_id']:6} {row['to_id']:6}  {row['relationship']:>18}  "
              f"{str(row['association_name']):>15}  {str(row['role']):>12}  "
              f"{row['from_name']} → {row['to_name']}")
else:
    print("No relationship found.")

