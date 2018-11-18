import heapq
d = {'first': 3, 'second': 4, 'third': 5}

for i in d.items():
    print(type(i))

print(heapq.nlargest(2,d.items(),lambda x: x[1]))