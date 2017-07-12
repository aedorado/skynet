import bisect

leaf = []

nodeid = 5
nodes_on_path = [2,3,4,6,7,8]

for node in nodes_on_path:
	bisect.insort(leaf,node)
	if(len(leaf)>4):
		if(nodeid > node):
			leaf = leaf[1:]
		else:
			leaf = leaf[:-1]

print leaf