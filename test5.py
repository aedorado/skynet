char_to_int = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}

def number_of_matching_digits(p1,p2):
	i = 0;
	l1 = len(p1)
	l2 = len(p2)
	while(i<min(l1,l2)):
		if(p1[i]!=p2[i]):
			break
		i += 1
	return str(i)	



p1 = '1242'
p2 = '1146'
p3 = '1338'

routing = []
step = number_of_matching_digits(p1,p2)
curr_size = len(routing)
for i in range(curr_size,int(step)+2):
	routing.append(["NULL"]*5)
routing[int(step)][char_to_int[p2[int(step)]]] = p2

step = number_of_matching_digits(p1,p3)
curr_size = len(routing)
for i in range(curr_size,int(step)+2):
	routing.append(["NULL"]*5)
routing[int(step)][char_to_int[p3[int(step)]]] = p3

print routing