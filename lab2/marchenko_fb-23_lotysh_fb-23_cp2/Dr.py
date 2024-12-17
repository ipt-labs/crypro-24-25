#This script helps us find the key's length

import matplotlib.pyplot as plt

file=open('./input.txt', 'r', encoding="utf-8")
data=file.read().replace('\n', '').lower()

D=[0]

for r in range(1, 40):
    D.append(0)
    for i in range(0, len(data)-r):
        if data[i]==data[i+r]:
            D[r]+=1
    print("D%d: %d" % (r, D[r]))

fig, ax = plt.subplots()
ax.bar(range(len(D)), D)
plt.xlabel("r")
plt.ylabel("Dr")
plt.show()
