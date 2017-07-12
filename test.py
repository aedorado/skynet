msg = "& 2345 5677 #Routing 6458 9846 ^ 7674 Routing 7387 9849 ^ 8990 Routing 7822 4090 ^ 9203$ 748 4549@4"

leaf = msg[msg.rfind('&')+1:msg.rfind('#')]

leaf = leaf.strip()
leaf = leaf.split()
print "leaf is : ",leaf

routing = msg[msg.rfind('#')+1:msg.rfind('$')]
#print routing
routing = routing.strip()
#print routing
routing = routing.split('Routing')
print routing

for i in range(1,len(routing)):
	x = routing[i].strip()
	row = x[:x.rfind('^')].strip()
	node = x[x.rfind('^')+1:].strip()
	entries = row.split()
	print "hey ",i+1
	print node, " ",row," ",entries

nei = msg[msg.rfind('$')+1:msg.rfind('@')]
nei = nei.split()

step = msg[msg.rfind('@')+1:]
print nei
print step