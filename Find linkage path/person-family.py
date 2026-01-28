# =========================================================
#  SECTION 0 — Main Function Entry Point
# =========================================================

import sqlite3
from collections import deque, defaultdict


def main():
    """
    Simple entry point for running a relationship search.
    Adjust parameters here as needed.
    """
    db_path = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Find linkage path\DB\TEST-Find linkage path.rmtree"

    start_id = 1
    target_id = 17

    allowed_types = {
        "parent": True,
        "child": True,
        "spouse": True,       # kept for future use; no direct spouse edges now
        "association": False,
        "shared_fact": False,
    }

    prune_rules = {
        "block_spouse_chains": True,   # mostly relevant if you later re-enable spouse edges
        "block_parent_chains": True,
        "block_child_chains": True,
        "max_generation_distance": 3,
    }

    result = find_paths(
        db_path=db_path,
        start_id=start_id,
        target_id=target_id,
        allowed_types=allowed_types,
        allpaths=True,
        max_depth=12,
        prune_rules=prune_rules,
    )

    shortest = result["shortest_path"]
    all_paths = result["all_paths"]

    print("=== SHORTEST PATH ===")
    if shortest:
        print("IDs   :", shortest["path"])
        print("Names :", " → ".join(shortest["names"]))
        print("Table :")
        print(f"{'from':>20} {'to':>20}  {'relationship':>22}  {'assoc_name':>15}  {'shared_fact':>15}  {'role':>12}")
        for row in shortest["table"]:
            print(
                f"{str(row['from_name']):>20} {str(row['to_name']):>20}  {row['relationship']:>22}  "
                f"{str(row['association_name']):>15}  {str(row['shared_fact_name']):>15}  {str(row['role']):>12}"
            )
    else:
        print("No shortest path found.")

    print("\n=== ALL PATHS (sorted by length, pruned) ===")
    print(f"Total paths: {len(all_paths)}\n")

    for idx, item in enumerate(all_paths, start=1):
        path = item["path"]
        names = item["names"]
        table = item["table"]

        print(f"Path #{idx}: IDs   :", path)
        print(f"Path #{idx}: Names :", " → ".join(names))
        print(f"Path #{idx}: Relationship table:")
        if table:
            print(f"{'from':>20} {'to':>20}  {'relationship':>22}  {'assoc_name':>15}  {'shared_fact':>15}  {'role':>12}")
            for row in table:
                print(
                    f"{str(row['from_name']):>20} {str(row['to_name']):>20}  {row['relationship']:>22}  "
                    f"{str(row['association_name']):>15}  {str(row['shared_fact_name']):>15}  {str(row['role']):>12}"
                )
        else:
            print("  (no edges?)")
        print()


# =========================================================
#  SECTION 1 — Defaults and Pruning Rules
# =========================================================

# Default: genealogical edges only
DEFAULT_ALLOWED_TYPES = {
    "parent": True,
    "child": True,
    "spouse": True,       # no direct spouse edges now, but kept for compatibility
    "association": False,
    "shared_fact": False,
}

# Default pruning rules for DFS (all paths)
DEFAULT_PRUNE_RULES = {
    "block_spouse_chains": True,   # mostly relevant if spouse edges are reintroduced
    "block_parent_chains": True,
    "block_child_chains": True,
    "max_generation_distance": 3,  # good for uncle/nephew, cousins, etc.
}


# =========================================================
#  SECTION 2 — Name Helpers
# =========================================================

def get_primary_name_row(conn, person_id):
    """
    Return (Given, Surname) for the primary name of a person, or (None, None).
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT Given, Surname
        FROM NameTable
        WHERE OwnerID = ? AND IsPrimary = 1
        LIMIT 1
    """, (person_id,))
    row = cur.fetchone()
    if row:
        return row[0], row[1]
    return None, None


def format_person_display_name(given, surname):
    """
    Build a display name from Given and Surname.
    If both missing, return 'Unknown'.
    """
    given = (given or "").strip()
    surname = (surname or "").strip()

    if surname:
        if given:
            return f"{given} {surname}"
        return surname
    if given:
        return given
    return "Unknown"


def get_person_display_name(conn, person_id):
    """
    Convenience: get formatted display name for a person_id.
    """
    given, surname = get_primary_name_row(conn, person_id)
    return format_person_display_name(given, surname)


def get_person_surname_or_unknown(conn, person_id):
    """
    Return surname if present, otherwise 'Unknown'.
    """
    given, surname = get_primary_name_row(conn, person_id)
    surname = (surname or "").strip()
    if surname:
        return surname
    return "Unknown"


# =========================================================
#  SECTION 3 — Graph Construction (Person → Family → Person)
#     - Family relationships via Family nodes
#     - FAN associations (person ↔ person)
#     - Shared facts (person ↔ person)
# =========================================================

def build_family_node_label(conn, family_id, father_id, mother_id):
    """
    Build a label like:
      'FAM: Smith–Johnson [FamilyID=17]'
    using surnames where possible, falling back to 'Unknown'.
    """
    surnames = []

    if father_id and father_id > 0:
        surnames.append(get_person_surname_or_unknown(conn, father_id))
    if mother_id and mother_id > 0:
        surnames.append(get_person_surname_or_unknown(conn, mother_id))

    if not surnames:
        base = "Unknown"
    elif len(surnames) == 1:
        base = surnames[0]
    else:
        base = f"{surnames[0]}–{surnames[1]}"

    return f"FAM: {base} [FamilyID={family_id}]"


def load_graph(db_path):
    """
    Build the relationship graph from the RootsMagic DB.

    Nodes:
      - Person nodes: integer PersonID
      - Family nodes: string labels like 'FAM: Smith–Johnson [FamilyID=17]'

    Edges:
      - Person ↔ Family for parent/child relationships
      - Person ↔ Person for associations (FANTable)
      - Person ↔ Person for shared facts (Event/Witness)

    graph[node] = list of (neighbor_node, relationship_label, role)
      relationship_label examples:
        'parent'        (Family → Person)
        'child'         (Person → Family)
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
    # FamilyTable + ChildTable: parent/child via Family nodes
    # -----------------------------------------------------
    # Build a mapping of FamilyID → (FatherID, MotherID)
    cur.execute("""
        SELECT FamilyID, FatherID, MotherID
        FROM FamilyTable
    """)
    family_parents = {
        fid: (father_id, mother_id)
        for fid, father_id, mother_id in cur.fetchall()
    }

    # Build FamilyID → FamilyNodeLabel
    family_nodes = {}
    for fid, (father_id, mother_id) in family_parents.items():
        family_nodes[fid] = build_family_node_label(conn, fid, father_id, mother_id)

    # Link children to families
    cur.execute("""
        SELECT FamilyID, ChildID
        FROM ChildTable
        WHERE ChildID > 0
    """)
    for family_id, child_id in cur.fetchall():
        if family_id not in family_nodes:
            continue
        fam_node = family_nodes[family_id]

        # Person → Family (child edge)
        graph[child_id].append((fam_node, "child", None))
        # Family → Person (parent edge, but from the family's perspective it's "parent")
        graph[fam_node].append((child_id, "parent", None))

    # Link parents to families
    for family_id, (father_id, mother_id) in family_parents.items():
        fam_node = family_nodes.get(family_id)
        if not fam_node:
            continue

        # Father
        if father_id and father_id > 0:
            # Person → Family (parent participates in family)
            graph[father_id].append((fam_node, "parent", None))
            # Family → Person (parent)
            graph[fam_node].append((father_id, "parent", None))

        # Mother
        if mother_id and mother_id > 0:
            graph[mother_id].append((fam_node, "parent", None))
            graph[fam_node].append((mother_id, "parent", None))

    # NOTE: No direct spouse edges now. Spouses are connected via shared Family node.

    # -----------------------------------------------------
    # FANTable: associations with roles from FANTypeTable (person ↔ person)
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

    # Add shared-fact edges (person ↔ person)
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
#  SECTION 4 — Pathfinding
#     - BFS shortest path (unfiltered)
#     - DFS all paths (filtered + pruning)
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


def find_all_paths(graph, start, target, allowed_types, max_depth=20, prune_rules=None):
    """
    DFS: returns all simple paths from start → target,
    filtered by allowed_types, limited by max_depth,
    with genealogical pruning rules.
    """

    if prune_rules is None:
        prune_rules = DEFAULT_PRUNE_RULES.copy()

    all_paths = []
    visited = set()

    # generation distance: parent = +1, child = -1, spouse = 0, others = 0
    def rel_gen_delta(rel):
        base = rel.split(":", 1)[0]
        if base == "parent":
            return +1
        if base == "child":
            return -1
        return 0  # spouse, association, shared_fact, etc.

    def dfs(node, path, last_rel, gen_dist):
        # depth limit
        if len(path) > max_depth:
            return

        # generation-distance pruning
        if abs(gen_dist) > prune_rules["max_generation_distance"]:
            return

        # reached target
        if node == target:
            all_paths.append(path.copy())
            return

        visited.add(node)

        for neighbor, rel, role in graph[node]:
            # allowed-type filtering
            if not _is_allowed(rel, allowed_types):
                continue

            base_rel = rel.split(":", 1)[0]

            # spouse-chain suppression (mostly relevant if spouse edges reintroduced)
            if prune_rules["block_spouse_chains"]:
                if last_rel == "spouse" and base_rel == "spouse":
                    continue

            # parent-chain suppression
            if prune_rules["block_parent_chains"]:
                if last_rel == "parent" and base_rel == "parent":
                    continue

            # child-chain suppression
            if prune_rules["block_child_chains"]:
                if last_rel == "child" and base_rel == "child":
                    continue

            if neighbor not in visited:
                dfs(
                    neighbor,
                    path + [neighbor],
                    base_rel,
                    gen_dist + rel_gen_delta(rel)
                )

        visited.remove(node)

    dfs(start, [start], last_rel=None, gen_dist=0)
    return all_paths


# =========================================================
#  SECTION 5 — Name Lookup for Paths
# =========================================================

def get_names_for_path(conn, path):
    """
    Return a list of display names for each node in the path.
    - For person nodes (int): use primary name.
    - For family nodes (str): use the family label itself.
    """
    names = []
    for node in path:
        if isinstance(node, int):
            names.append(get_person_display_name(conn, node))
        else:
            # family node label is already human-readable
            names.append(str(node))
    return names


# =========================================================
#  SECTION 6 — Relationship Table Builders
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
        names = get_names_for_path(conn, path)
        table = build_relationship_table(graph, path, names)
        results.append({
            "path": path,
            "names": names,
            "table": table,
        })
    return results


# =========================================================
#  SECTION 7 — Main API
#     - find_paths(...)
# =========================================================

def find_paths(
    db_path,
    start_id,
    target_id,
    allowed_types=None,
    allpaths=False,
    max_depth=20,
    prune_rules=None,
):
    """
    Main entry point.

    Parameters:
      db_path      : path to RootsMagic DB
      start_id     : PersonID start (int)
      target_id    : PersonID target (int)
      allowed_types: dict of booleans for base relationship types
                     (parent, child, spouse, association, shared_fact)
                     If None, DEFAULT_ALLOWED_TYPES is used.
      allpaths     : False → shortest path only (BFS, unfiltered)
                     True  → shortest path + all DFS paths (filtered + pruned)
      max_depth    : max depth for DFS when allpaths=True
      prune_rules  : dict of pruning options; if None, DEFAULT_PRUNE_RULES used

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
    if prune_rules is None:
        prune_rules = DEFAULT_PRUNE_RULES.copy()

    graph, conn = load_graph(db_path)

    # --- Shortest path (BFS, unfiltered) ---
    shortest_path = bfs_shortest_path(graph, start_id, target_id)
    shortest_result = None

    if shortest_path:
        shortest_names = get_names_for_path(conn, shortest_path)
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

    # --- All paths (DFS, filtered by allowed_types + pruned) ---
    dfs_paths = find_all_paths(
        graph,
        start_id,
        target_id,
        allowed_types,
        max_depth=max_depth,
        prune_rules=prune_rules,
    )

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

# Standard Python entry point
if __name__ == "__main__":
    main()
