from pathlib import Path

droplet = frozenset(tuple(map(int, l.strip().split(','))) for l in open(Path(__file__).resolve().parent / 'input.txt'))

def next_neighbours(p):
  return frozenset(
    [(p[0]+i,p[1],p[2]) for i in [-1,1]] +
    [(p[0],p[1]+i,p[2]) for i in [-1,1]] +
    [(p[0],p[1],p[2]+i) for i in [-1,1]]
  )

def surface(o):
  touching = sum(len(o & next_neighbours(p)) for p in o)
  return len(o)*6-touching

print(surface(droplet))

def dimensions(o):
  return (
    (min(x for x,_,_ in o), max(x for x,_,_ in o)),
    (min(y for _,y,_ in o), max(y for _,y,_ in o)),
    (min(z for _,_,z in o), max(z for _,_,z in o))
  )

def invert(o, d):
  result = set()
  for x in range(d[0][0], d[0][1]+1):
    for y in range(d[1][0], d[1][1]+1):
      for z in range(d[2][0], d[2][1]+1):
        if (x,y,z) not in o:
          result.add((x,y,z))
  return frozenset(result)

def submerge(o, d):
  result = set()
  queue = [(d[0][0]-1,d[1][0]-1,d[2][0]-1)]
  while queue:
    c = queue.pop()
    for n in next_neighbours(c):
      if n not in result and n not in o and (
        d[0][0]-1<=n[0]<=d[0][1]+1 and
        d[1][0]-1<=n[1]<=d[1][1]+1 and
        d[2][0]-1<=n[2]<=d[2][1]+1):
        queue.append(n)
        result.add(n)
  return result

droplet_dim = dimensions(droplet)
droplet_outside = submerge(droplet, droplet_dim)
print(surface(invert(droplet_outside, dimensions(droplet_outside))))
