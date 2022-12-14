from pathlib import Path

f = open(Path(__file__).resolve().parent / 'input.txt')

lines = []
for l in f:
  l = l.strip()
  if l:
    lines.append([tuple(map(int, p.split(','))) for p in l.split(' -> ')])

world = {}
for segments in lines:
  for a,b in zip(segments, segments[1:]):
    ab = (b[0]-a[0],b[1]-a[1])
    dist = abs(ab[0]+ab[1])
    sab = (ab[0]//dist,ab[1]//dist)
    for i in range(dist+1):
      p = (a[0]+sab[0]*i,a[1]+sab[1]*i)
      world[p] = '#'
source = (500,0)
world[source] = '+'

def printWorld(world,dim):
  for j in range(dim[1][0],dim[1][1]+1):
    for i in range(dim[0][0],dim[0][1]+1):
      if (i,j) in world:
        print(world[(i,j)], end='')
      else:
        print('.', end='')
    print()

def calcDim(world):
  return (
    (min(p[0] for p in world),max(p[0] for p in world)),
    (min(p[1] for p in world),max(p[1] for p in world))
  )

dim = calcDim(world)
eow = dim[1][1]
#printWorld(world,dim)
#print(dim)

def sim(world, source, eow):
  def fall(p):
    below=(p[0],p[1]+1)
    left=(p[0]-1,p[1]+1)
    right=(p[0]+1,p[1]+1)
    for n in [below,left,right]:
      if n not in world:
        return n
    return p
  p = source
  while True:
    n = fall(p)
    if n == p:
      break
    if n[1]>eow:
      return None
    p = n
  world[p] = 'o'
  return p

count = 0
while True:
  s = sim(world,source,eow)
  if s is None:
    break
  count += 1
print(count)

j = eow+2
for i in range(500-j-1,500+j+2):
  world[(i,j)] = '#'
dim = calcDim(world)
eow = dim[1][1]
#printWorld(world, dim)
#print(dim)

while True:
  count += 1
  s = sim(world,source,eow)
  if s is None:
    raise RuntimeError('dafuq')
  if s == source:
    break
#printWorld(world, dim)
print(count)
