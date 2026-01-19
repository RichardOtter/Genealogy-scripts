import sqlite3
from collections import deque, defaultdict

def load_graph(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # graph[node] = list of (neighbor, relationship_type)
    graph = defaultdict(list)

    # Parent-child edges via FamilyID
    cur.execute("""
        SELECT f.FatherID, f.MotherID, c.ChildID
        FROM FamilyTable f
        JOIN ChildTable c ON c.FamilyID = f.FamilyID
    """)

    for father, mother, child in cur.fetchall():

        # father ↔ child
        if father and father > 0 and child and child > 0:
            graph[father].append((child, "parent"))
            graph[child].append((father, "child"))

        # mother ↔ child
        if mother and mother > 0 and child and child > 0:
            graph[mother].append((child, "parent"))
            graph[child].append((mother, "child"))

        # spouse ↔ spouse
        if father and father > 0 and mother and mother > 0:
            graph[father].append((mother, "spouse"))
            graph[mother].append((father, "spouse"))

    return graph, conn


def bfs_shortest_path(graph, start, target):
    if start == target:
        return [start]

    visited = set([start])
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        for neighbor, _rel in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                if neighbor == target:
                    return new_path
                queue.append(new_path)

    return None


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

    rows = {pid: f"{given} {surname}".strip()
            for pid, surname, given in cur.fetchall()}

    return [rows.get(pid, f"[{pid}]") for pid in person_ids]

def build_relationship_table(graph, path, names):
    table = []

    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]

        # find relationship type from graph
        rel = next((r for (nbr, r) in graph[a] if nbr == b), "unknown")

        table.append({
            "from_id": a,
            "to_id": b,
            "from_name": names[i],
            "to_name": names[i + 1],
            "relationship": rel
        })

    return table


def find_relationship_path(db_path, start_id, target_id):
    graph, conn = load_graph(db_path)
    path = bfs_shortest_path(graph, start_id, target_id)

    if not path:
        return None, None, None

    names = get_names(conn, path)
    table = build_relationship_table(graph, path, names)

    return path, names, table


# ---------------------------------------------------------
# Your requested lines
# ---------------------------------------------------------

DB_PATH = r"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\Find linkage path\DB\TEST-Find linkage path.rmtree"
path, names, table = find_relationship_path(DB_PATH, 1, 17)

print("Path IDs:", path)
print("Names:", " → ".join(names))
print("\nRelationship Table:")
for row in table:
    print(f"{row['from_id']:>5}  →  {row['to_id']:>5}   {row['relationship']:>7}   {row['from_name']} → {row['to_name']}")