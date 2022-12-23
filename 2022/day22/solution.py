from pathlib import Path
import re

world = {}
f = open(Path(__file__).resolve().parent / 'input.txt')
y = 0
while True:
  l = next(f)
  if not l.strip():
    break
  for x,c in enumerate(l):
    if c.isspace():
      continue
    world[(x,y)] = c
  y += 1
instructions = [int(s) if s.isdigit() else s for s in re.split(r'(\d+)',next(f).strip()) if s]

world_dim = (
  max(x for x,_ in world)+1,
  max(y for _,y in world)+1
)
world_range = (
  {y: (min(xx for xx,yy in world if yy==y),max(xx for xx,yy in world if yy==y)) for y in range(world_dim[1])},
  {x: (min(yy for xx,yy in world if xx==x),max(yy for xx,yy in world if xx==x)) for x in range(world_dim[0])}
)

def wrap(s):
  s = list(s)
  i = 0 if s[2] in (0,180) else 1
  i_min,i_max = world_range[i][s[1-i]][0],world_range[i][s[1-i]][1]
  if not i_min <= s[i] <= i_max:
    s[i] = (s[i]-i_min)%(i_max-i_min+1)+i_min
  return tuple(s)

def step(s,wrap):
  delta = {0:(1,0),90:(0,1),180:(-1,0),270:(0,-1)}[s[2]]
  new_s = tuple([s[i]+delta[i] for i in range(2)] + [s[2]])
  return wrap(new_s)

def clip(a):
  if a < 0:
    return clip(a+360)
  if a >= 360:
    return clip(a-360)
  return a

def turn(s,d):
  a = {'R':90,'L':-90}[d]
  return (s[0],s[1],clip(s[2]+a))

def walk(s,d,wrap):
  for _ in range(d):
    new_s = step(s,wrap)
    if new_s[:2] not in world:
      raise RuntimeError('dafuq')
    if world[tuple(new_s[i] for i in range(2))] == '#':
      break
    s = new_s
  return s

def path(start,instructions,wrap):
  s = start
  for i in instructions:
    if isinstance(i,int):
      s = walk(s,i,wrap)
    else:
      s = turn(s,i)
  return s

def pw(p):
  return 1000*(p[1]+1)+4*(p[0]+1)+({0:0,90:1,180:2,270:3}[p[2]])

start = (next(x for x in range(*world_range[0][0]) if world[(x,0)] == '.'),0,0)
print(pw(path(start,instructions,wrap)))

def fold_portals(world, world_dim):
  if max(*world_dim)*3 == min(*world_dim)*4:
    max_pieces = 4
  elif max(*world_dim)*2 == min(*world_dim)*5:
    max_pieces = 5
  else:
    raise RuntimeError('dafuq')
  side = max(*world_dim)//max_pieces
  sides = frozenset((x,y) for x in range(max_pieces) for y in range(max_pieces) if (x*side,y*side) in world)

  def next_neighbours(p):
    return [
      (p[0]+1,p[1]),
      (p[0]-1,p[1]),
      (p[0],p[1]+1),
      (p[0],p[1]-1),
    ]

  def sign(x):
    return 1 if x >= 0 else -1

  def transform(t,p):
    return tuple(p[abs(i)-1]*sign(i) for i in t)

  nn_transforms = [(3,2,-1),(-3,2,1),(1,3,-2),(1,-3,2)]

  transforms = {}
  queue = [(next(iter(sides)),(1,2,3))]
  while queue:
    c,t = queue.pop()
    for n,nt in zip(next_neighbours(c),nn_transforms):
      if n not in sides or n in transforms:
        continue
      transforms[n] = transform(t,nt)
      queue.append((n,transforms[n]))

  vertices3d = [(1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)]
  edges3d = list(zip(vertices3d,vertices3d[1:]+vertices3d[:-1]))

  def edges(s,shift=0):
    x1,x2 = s[0]*side,(s[0]+1)*side-1
    y1,y2 = s[1]*side,(s[1]+1)*side-1
    return [
      ((x2,y2+shift),(x1,y2+shift)),
      ((x1-shift,y2),(x1-shift,y1)),
      ((x1,y1-shift),(x2,y1-shift)),
      ((x2+shift,y1),(x2+shift,y2)),
    ]

  def line(a,b):
    delta = (b[0]-a[0],b[1]-a[1])
    if (delta[0] == 0) == (delta[1] == 0):
      raise RuntimeError('dafuq')
    distance = max(abs(d) for d in delta)
    delta = (delta[0]//distance,delta[1]//distance)
    return [(a[0]+delta[0]*d,a[1]+delta[1]*d) for d in range(distance+1)]

  def connect(edge1,edge2,a1,a2):
    return {tuple(list(a)+[a1]):tuple(list(b)+[a2]) for a,b in zip(line(*edge1),line(*edge2)) if a != b}

  angels = [90,180,270,0]

  portals = {}
  for s1,t1 in transforms.items():
    for s2,t2 in transforms.items():
      if s1 == s2:
        continue
      for i1,(a1,b1) in enumerate(edges3d):
        for i2,(a2,b2) in enumerate(edges3d):
          ta1,tb1 = transform(t1,a1),transform(t1,b1)
          ta2,tb2 = transform(t2,a2),transform(t2,b2)
          if (ta1,tb1) == (ta2,tb2):
            portals.update(connect(edges(s1,1)[i1],edges(s2)[i2],angels[i1],clip(angels[i2]+180)))
          elif (ta1,tb1) == (tb2,ta2):
            portals.update(connect(edges(s1,1)[i1],edges(s2)[i2][::-1],angels[i1],clip(angels[i2]+180)))

  return portals

portals = fold_portals(world, world_dim)
def wrap2(s):
  return portals[s] if s in portals else s
print(pw(path(start,instructions,wrap2)))
