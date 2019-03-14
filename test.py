def gen(c):
	somenumber = 5+c
	for i in range(5):
		yield somenumber

c=0
while c < 5:
	for i in gen(c):
		print(i)
		c+=1
