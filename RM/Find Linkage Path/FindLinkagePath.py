import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

# ===============================
# 1. Connect to the RootsMagic Database
# ===============================
db_path = "test.rmtree.sqlite"  # update your file path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# -------------------------------
# 2. Query individuals from PersonTable
# Assumed columns: PersonID, Name, FamilyChildID (the family where the person is a child)
# -------------------------------
# works only with primary parent familt
cursor.execute(
"""
  SELECT PersonID, nt.Given || ' ' || nt.Surname as Name, ParentID
  FROM PersonTable as pt
  JOIN NameTable as nt on PersonID = nt.ownerID
  WHERE nt.IsPrimary == 1
""")
persons = cursor.fetchall()

# Create a mapping from PersonID to Name for labeling family relationships later
person_dict = {}
# We will also add each person as a node in our graph.
G = nx.DiGraph()  # directed graph (for parent-to-child relationships)

for person in persons:
    person_id, name, family_child_id = person
    person_dict[person_id] = name
    # Mark node type 'person'
    G.add_node(person_id, label=name, type='person', family_child_id=family_child_id)

# -------------------------------
# 3. Query families from FamilyTable
# Assumed columns: FamilyID, HusbandID, WifeID
# -------------------------------
cursor.execute("SELECT FamilyID, FatherID, MotherID FROM FamilyTable")
families = cursor.fetchall()

conn.close()  # We're done with querying the database

# -------------------------------
# 4. Add family nodes to the graph
# We'll create a separate node for each family (marriage) and label it with the spouses' names.
# Family nodes are stored with a prefix (e.g., "F") to distinguish them from person IDs.
# -------------------------------
for family in families:
    family_id, husband_id, wife_id = family
    # Build a label using the names of the spouses (if available)
    label_parts = []
    if husband_id:
        label_parts.append(person_dict.get(husband_id, f"Unknown({husband_id})"))
    if wife_id:
        label_parts.append(person_dict.get(wife_id, f"Unknown({wife_id})"))
    label = " & ".join(label_parts)
    # Use a prefix for the family node (e.g., "F" + family_id)
    family_node = f"F{family_id}"
    G.add_node(family_node, label=label, type='family')
    
    # -------------------------------
    # 5. Add edges from spouses (person nodes) to this family node.
    # This denotes the marriage or partnership.
    # -------------------------------
    if husband_id:
        G.add_edge(husband_id, family_node)
    if wife_id:
        G.add_edge(wife_id, family_node)

# -------------------------------
# 6. Link children to their parent family nodes.
# For each person, if they have an associated FamilyChildID,
# add an edge from the corresponding family node to the person node.
# -------------------------------
for person in persons:
    person_id, name, family_child_id = person
    if family_child_id is not None:
        family_node = f"F{family_child_id}"
        # If the family node doesn't exist (it should if the data is consistent),
        # create a placeholder family node.
        if family_node not in G.nodes():
            G.add_node(family_node, label="Unknown Family", type='family')
        G.add_edge(family_node, person_id)

# ===============================
# 7. Visualize the Family Tree with NetworkX and Matplotlib
# ===============================
# Compute a layout for the graph
pos = nx.spring_layout(G, k=0.5)

# Prepare labels for drawing. We use the 'label' attribute saved on each node.
labels = nx.get_node_attributes(G, 'label')

# Define node colors based on node type:
# - Person nodes: lightblue
# - Family nodes: lightgreen
node_colors = []
for node in G.nodes():
    if G.nodes[node]['type'] == 'person':
        node_colors.append("lightblue")
    else:
        node_colors.append("lightgreen")

# Draw the graph
plt.figure(figsize=(12, 8))
nx.draw(
    G, pos,
    with_labels=True,
    labels=labels,
    node_color=node_colors,
    node_size=2000,
    font_size=9,
    edge_color="gray",
    arrows=True,
)
plt.title("Family Tree from RootsMagic SQLite Database")
plt.axis("off")
plt.show()


# https://www.google.com/search?q=how+to+walk+a+family+tree+in+pseudo+code+to+find+linkage+between+two+people+in+python&sca_esv=9f05e2405697a5fa&sxsrf=AE3TifOgT98uQx2SHBU8pKQhYvYVvJi2Lg%3A1749135602655&ei=8rBBaLLUJ-3Gp84PoaGTwAk&ved=0ahUKEwiylYryxdqNAxVt48kDHaHQBJgQ4dUDCBA&uact=5&oq=how+to+walk+a+family+tree+in+pseudo+code+to+find+linkage+between+two+people+in+python&gs_lp=Egxnd3Mtd2l6LXNlcnAiVWhvdyB0byB3YWxrIGEgZmFtaWx5IHRyZWUgaW4gcHNldWRvIGNvZGUgdG8gZmluZCBsaW5rYWdlIGJldHdlZW4gdHdvIHBlb3BsZSBpbiBweXRob25IgSdQvAxYhiRwAXgBkAEAmAGbAaAB0QiqAQMwLjm4AQPIAQD4AQGYAgGgAgfCAgoQABiwAxjWBBhHmAMAiAYBkAYHkgcBMaAHxhOyBwC4BwDCBwMyLTHIBwQ&sclient=gws-wiz-serp

def breadth_first_search(family_tree, start_node):
    """
    Performs a Breadth-First Search traversal of a family tree.

    Args:
        family_tree (dict): A dictionary representing the family tree, where keys
                              are family member names and values are lists of their children.
        start_node (str): The name of the starting family member.

    Returns:
        list: A list containing the names of family members visited in BFS order.
    """
"""
    visited = []  # List to store visited family members
    queue = [start_node]  # Queue for nodes to explore

    while queue:
        current_node = queue.pop(0)  # Dequeue the first node
        if current_node not in visited:
            visited.append(current_node)  # Mark as visited
            # Enqueue all children of the current node
            if current_node in family_tree:
                for child in family_tree[current_node]:
                    queue.append(child)

    return visited



function find_linkage(tree, person1, person2):
    paths1 = find_paths(tree, person1)
    paths2 = find_paths(tree, person2)

    if paths1 is empty or paths2 is empty:
      return "No Linkage Found"

    for path1 in paths1:
        for path2 in paths2:
            common_ancestor = find_common_ancestor(path1, path2)
            if common_ancestor is not None:
                return build_relationship_string(path1, path2, common_ancestor)

    return "No Linkage Found"
"""

"""
function find_paths(tree, start_person):
    paths = []
    dfs(tree, start_person, [], paths)
    return paths

function dfs(tree, current_person, current_path, paths):
    current_path.append(current_person)

    if current_person not in tree:
        paths.append(current_path)
        return

    for child in tree[current_person]:
        dfs(tree, child, current_path[:], paths)

function find_common_ancestor(path1, path2):
    for person in reversed(path1):
        if person in path2:
            return person
    return None

function build_relationship_string(path1, path2, common_ancestor):
    # Logic to build a string describing the relationship based on the paths.
    # Example:
    # "Person1 is the descendant of common_ancestor, Person2 is the descendant of common_ancestor"
    # "Person1 is the cousin of Person2 through common_ancestor"
    return "Relationship Found"
"""