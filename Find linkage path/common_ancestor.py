#!/usr/bin/env python3
"""
common_ancestor.py - Find the nearest common ancestor and relationship between
two or more people in a RootsMagic .rmtree file.

Usage:
    common_ancestor.py myfile.rmtree 42 99
    common_ancestor.py myfile.rmtree 42 99 150       # 3+ people
    common_ancestor.py myfile.rmtree 42 99 --top 5   # nearest 5 ancestors
    common_ancestor.py myfile.rmtree 42 99 --all     # show all common ancestors
"""

import argparse
import os
import sqlite3
import sys
from collections import deque

# Sex: 0=Male, 1=Female, 2=Unknown


def rmnocase(a, b):
    a, b = a.casefold(), b.casefold()
    return (a > b) - (a < b)


import re


def parse_year(date_str):
    """Extract year from RootsMagic Date field (e.g. 'D.+14490000..+00000000..')."""
    if not date_str:
        return None
    m = re.search(r'[+-](\d{4})', date_str)
    if m:
        return int(m.group(1))
    return None


def load_data(cur):
    """Load persons and parent relationships into memory."""
    cur.execute("""
        SELECT p.PersonID, n.Given, n.Surname, p.Sex
        FROM PersonTable p
        LEFT JOIN NameTable n ON n.OwnerID = p.PersonID AND n.IsPrimary = 1
    """)
    persons = {}
    for row in cur.fetchall():
        persons[row[0]] = (row[1] or "", row[2] or "", row[3])

    # Load birth years: PersonID -> year
    birth_years = {}
    cur.execute("""
        SELECT OwnerID, Date FROM EventTable
        WHERE EventType = 1 AND OwnerType = 0 AND Date != ''
    """)
    for owner_id, date_str in cur.fetchall():
        year = parse_year(date_str)
        if year:
            birth_years[owner_id] = year

    # ChildID -> [(FatherID, MotherID), ...]
    cur.execute("""
        SELECT c.ChildID, f.FatherID, f.MotherID
        FROM ChildTable c
        JOIN FamilyTable f ON c.FamilyID = f.FamilyID
    """)
    parents_map = {}
    for child_id, father_id, mother_id in cur.fetchall():
        if child_id not in parents_map:
            parents_map[child_id] = set()
        if father_id and father_id > 0:
            parents_map[child_id].add(father_id)
        if mother_id and mother_id > 0:
            parents_map[child_id].add(mother_id)

    return persons, parents_map, birth_years


def get_all_ancestors(person_id, parents_map):
    """BFS to get all ancestors with their generation distance.
    Returns {ancestor_id: (distance, path)}."""
    ancestors = {}
    queue = deque([(person_id, 0, [person_id])])
    visited = set()

    while queue:
        current, gen, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        ancestors[current] = (gen, path)

        for parent_id in parents_map.get(current, set()):
            if parent_id not in visited:
                queue.append((parent_id, gen + 1, path + [parent_id]))

    return ancestors


def format_person(person_id, persons, birth_years=None):
    if person_id not in persons:
        return f"(ID={person_id}, not found)"
    given, surname, _ = persons[person_id]
    year = birth_years.get(person_id) if birth_years else None
    year_str = f" ({year})" if year else ""
    return f"{given} {surname}{year_str}"


def ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def describe_relationship(gen_a, gen_b, sex_ancestor):
    """Describe the relationship given generations from each person to the common ancestor."""
    if gen_a == 0 and gen_b == 0:
        return "same person"

    if gen_a == 0 or gen_b == 0:
        # Direct ancestor/descendant
        child_gen = max(gen_a, gen_b)
        # Person with gen=0 is the ancestor
        is_ancestor_male = sex_ancestor if min(gen_a, gen_b) == 0 else None
        if child_gen == 1:
            if gen_a == 0:
                return "parent" if is_ancestor_male is None else ("father" if is_ancestor_male == 0 else "mother")
            else:
                return "child" if is_ancestor_male is None else ("son" if is_ancestor_male == 0 else "daughter")
        prefix = "great-" * (child_gen - 2) + "grand" if child_gen >= 2 else ""
        if gen_a == 0:
            return f"{prefix}{'father' if sex_ancestor == 0 else 'mother' if sex_ancestor == 1 else 'parent'}"
        else:
            return f"{prefix}child"

    if gen_a == 1 and gen_b == 1:
        return "siblings"

    if gen_a == 1 or gen_b == 1:
        # Aunt/uncle or niece/nephew
        cousin_gen = max(gen_a, gen_b)
        if min(gen_a, gen_b) == 1:
            prefix = "great-" * (cousin_gen - 2) if cousin_gen > 2 else ""
            if gen_a == 1:
                return f"{prefix}{'uncle' if sex_ancestor == 0 else 'aunt' if sex_ancestor == 1 else 'uncle/aunt'}"
            else:
                return f"{prefix}{'nephew' if sex_ancestor == 0 else 'niece' if sex_ancestor == 1 else 'nephew/niece'}"

    if gen_a == gen_b:
        return f"{ordinal(gen_a - 1)} cousins"

    # Different generations = cousins removed
    cousin_degree = min(gen_a, gen_b) - 1
    times_removed = abs(gen_a - gen_b)
    removed_str = f"{times_removed}x removed" if times_removed > 1 else "once removed"
    return f"{ordinal(cousin_degree)} cousins, {removed_str}"


def find_common_ancestors(person_ids, parents_map):
    """Find all common ancestors shared by all given persons."""
    all_ancestors = []
    for pid in person_ids:
        all_ancestors.append(get_all_ancestors(pid, parents_map))

    # Common ancestors = intersection of all ancestor sets
    common = set(all_ancestors[0].keys())
    for anc in all_ancestors[1:]:
        common &= set(anc.keys())

    # Remove the input persons themselves (unless one is ancestor of another)
    input_set = set(person_ids)
    for pid in input_set:
        if pid in common and all(a[pid][0] == 0 for a in all_ancestors):
            common.discard(pid)

    if not common:
        return []

    results = []
    for anc_id in common:
        gens = [a[anc_id][0] for a in all_ancestors]
        paths = [a[anc_id][1] for a in all_ancestors]
        total_dist = sum(gens)
        results.append((total_dist, gens, anc_id, paths))

    results.sort(key=lambda x: x[0])
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Find nearest common ancestor and relationship between two or more persons"
    )
    parser.add_argument("rmtree", type=str, help="Path to the .rmtree file")
    parser.add_argument("person_ids", type=int, nargs="+", metavar="ID",
                        help="PersonIDs to compare (2 or more)")
    parser.add_argument("--top", type=int, default=1, metavar="N",
                        help="Show nearest N common ancestors (default: 1, 0=all)")
    parser.add_argument("--all", action="store_true",
                        help="Show all common ancestors (same as --top 0)")
    parser.add_argument("--show-path", action="store_true",
                        help="Show the ancestor chain for each path")
    args = parser.parse_args()

    if len(args.person_ids) < 2:
        sys.exit("Error: Need at least 2 PersonIDs to compare")

    if not os.path.exists(args.rmtree):
        sys.exit(f"Error: File not found: {args.rmtree}")

    conn = sqlite3.connect(args.rmtree)
    conn.create_collation("RMNOCASE", rmnocase)
    cur = conn.cursor()

    persons, parents_map, birth_years = load_data(cur)
    conn.close()

    for pid in args.person_ids:
        if pid not in persons:
            sys.exit(f"Error: PersonID {pid} not found")

    results = find_common_ancestors(args.person_ids, parents_map)

    if not results:
        print(f"{'='*60}")
        for pid in args.person_ids:
            print(f"  {format_person(pid, persons, birth_years)}")
        print("  No common ancestor found.")
        return

    show_all = args.all or args.top == 0
    if not show_all:
        results = results[:args.top]

    two_person = len(args.person_ids) == 2

    for total_dist, gens, anc_id, paths in results:
        sex = persons[anc_id][2] if anc_id in persons else 2

        print(f"{'='*60}")
        for idx, (pid, gen) in enumerate(zip(args.person_ids, gens)):
            name = format_person(pid, persons, birth_years)
            print(f"  {name:<40} {gen} gens from ancestor")

        print(f"  {'Common ancestor:':<18} {format_person(anc_id, persons, birth_years)}")

        if two_person:
            rel = describe_relationship(gens[0], gens[1], sex)
            print(f"  {'Relationship:':<18} {rel}")

        if args.show_path:
            labels = [chr(65 + i) if i < 26 else str(i + 1) for i in range(len(args.person_ids))]
            for idx, (label, path) in enumerate(zip(labels, paths)):
                print(f"\n  Path from {label}:")
                for j, pid in enumerate(path):
                    print(f"    {'  ' * j}> {format_person(pid, persons, birth_years)}")



if __name__ == "__main__":
    main()
