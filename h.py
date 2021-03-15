#найти диаметр множества точек, взятых случайно
import random 
OGR = 10
n = random.randint(1,OGR)
m = 0
max_r = 0
min_r = 0
b = []
e = []
f = []
for i in range(n):
  c = (int(random.random() * OGR), int(random.random() * OGR))
  e.append(((c[0])**2 + (c[1])**2)**0.5)
  b.append(c)
for i in range(0, n):
  for j in range(i, n):
    d =((b[i][0]-b[j][0])**2 + (b[i][1]-b[j][1])**2)**0.5
    if d > m:
      m = d
      max_r = b[i]
      min_r = b[j]
if  min_r > max_r:
  min_r, max_r = max_r, min_r
for i in range (0, n):
  if e[i] == max(e):
    f.append(b[i])
print(*b)
print("Максимальные точки :", *f)
print("Минимальная точка", min_r)
print("Минимальная точка", max_r)
print("Максимальный диаметр:", m)


