a = list(map(int, input().split()))

for i in range(len(a)):
    for j in range(i):
        if a[j] > a[j+1]:
            temp = a[j]
            a[j] = a[j+1]
            a[j+1] = temp

b = {}

for i in set(a):
    b[i] = a.count(i)

for key, value in b.items():
    print(str(key) + ":" + str(value), end = " ")
    print()