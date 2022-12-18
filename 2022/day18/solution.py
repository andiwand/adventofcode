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

def is_inside(o, d, p):
  if p in o:
    return True

  i_x_n = sum(1 for x in range(d[0][0]-1,p[0]) if ((x,p[1],p[2]) in o) != ((x+1,p[1],p[2]) in o))
  i_x_p = sum(1 for x in range(p[0],d[0][1]+1) if ((x,p[1],p[2]) in o) != ((x+1,p[1],p[2]) in o))

  i_y_n = sum(1 for y in range(d[1][0]-1,p[1]) if ((p[0],y,p[2]) in o) != ((p[0],y+1,p[2]) in o))
  i_y_p = sum(1 for y in range(p[1],d[1][1]+1) if ((p[0],y,p[2]) in o) != ((p[0],y+1,p[2]) in o))

  i_z_n = sum(1 for z in range(d[2][0]-1,p[2]) if ((p[0],p[1],z) in o) != ((p[0],p[1],z+1) in o))
  i_z_p = sum(1 for z in range(p[2],d[2][1]+1) if ((p[0],p[1],z) in o) != ((p[0],p[1],z+1) in o))

  return all(i>0 and i%2==0 for i in [i_x_n, i_x_p, i_y_n, i_y_p, i_z_n, i_z_p])

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
air = frozenset(a for a in invert(droplet, droplet_dim) if is_inside(droplet, droplet_dim, a))

print(len(droplet), len(air), surface(air))

print(surface(droplet)-surface(air))

count = 0
for d in droplet:
  for n in next_neighbours(d):
    if n not in droplet and not is_inside(droplet, droplet_dim, n):
      count += 1
print(count)

droplet_outside = submerge(droplet, droplet_dim)
print(len(droplet_outside))
print(dimensions(droplet), dimensions(droplet_outside), dimensions(invert(droplet_outside, dimensions(droplet_outside))))
print(surface(invert(droplet_outside, dimensions(droplet_outside))))
