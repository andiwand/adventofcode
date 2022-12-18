from pathlib import Path
import itertools

droplet = frozenset(tuple(map(int, l.strip().split(','))) for l in open(Path(__file__).resolve().parent / 'input.txt'))

def next_neighbours(p):
  result = []
  for i in range(len(p)):
    result.extend([
      tuple(p[j] if j!=i else p[j]-1 for j in range(len(p))),
      tuple(p[j] if j!=i else p[j]+1 for j in range(len(p)))
    ])
  return frozenset(result)

def surface(o):
  touching = sum(len(o & next_neighbours(p)) for p in o)
  return len(o)*6-touching

print(surface(droplet))

def dimensions(o):
  return tuple((min(p[i] for p in o), max(p[i] for p in o)) for i in range(len(next(iter(o)))))

def inside(p, d):
  return all(d[i][0]<=p[i]<=d[i][1] for i in range(len(p)))

def invert(o, d):
  result = set()
  for p in itertools.product(*[range(r[0],r[1]+1) for r in d]):
    if p not in o:
      result.add(p)
  return frozenset(result)

def submerge(o, d):
  d = tuple((r[0]-1,r[1]+1) for r in d)
  result = set()
  queue = [tuple(r[0] for r in d)]
  while queue:
    c = queue.pop()
    for n in next_neighbours(c):
      if n not in result and n not in o and inside(n, d):
        queue.append(n)
        result.add(n)
  return frozenset(result)

droplet_dim = dimensions(droplet)
droplet_outside = submerge(droplet, droplet_dim)
print(surface(invert(droplet_outside, dimensions(droplet_outside))))
