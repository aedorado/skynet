import bisect

n = 3
node = 8
a = [1,2,11,12]
bisect.insort(a,n)

if(node>n):
	a = a[1:]
else:
	a = a[:-1]

print a