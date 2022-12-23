from pathlib import Path
import re
import numpy as np

world = {}
f = open(Path(__file__).resolve().parent / 'simpleinput.txt')
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
  new_s = [s[i]+delta[i] for i in range(2)] + [s[2]]
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
  return 1000*(p[1]+1)+4*(p[0]+1)+({0:0,90:3,180:2,270:1}[p[2]])

start = (next(x for x in range(*world_range[0][0]) if world[(x,0)] == '.'),0,0)
print(pw(path(start,instructions,wrap)))

def fold(world, world_dim):
  # this does not handle the 5:2 case
  side = max(*world_dim)//4
  sides = frozenset((x,y) for x in range(4) for y in range(4) if (x*side,y*side) in world)

  def next_neighbours(p):
    return [
      (p[0]+1,p[1]),
      (p[0]-1,p[1]),
      (p[0],p[1]+1),
      (p[0],p[1]-1),
    ]
  nn_transforms = [
    np.array([[0,0,1],[0,1,0],[-1,0,0]]),
    np.array([[0,0,-1],[0,1,0],[1,0,0]]),
    np.array([[1,0,0],[0,0,1],[0,-1,0]]),
    np.array([[1,0,0],[0,0,-1],[0,1,0]]),
  ]

  transforms = {}
  queue = [(next(iter(sides)),np.eye(3))]
  while queue:
    c,t = queue.pop()
    for n,nt in zip(next_neighbours(c),nn_transforms):
      if n not in sides or n in transforms:
        continue
      transforms[n] = t.dot(nt)
      queue.append((n,transforms[n]))

  vertices3d = [
    np.array([1,1,1]),
    np.array([-1,1,1]),
    np.array([-1,-1,1]),
    np.array([1,-1,1]),
  ]
  edges3d = list(zip(vertices3d,vertices3d[1:]+vertices3d[:-1]))

  portals = {}
  for s1,t1 in transforms.items():
    for s2,t2 in transforms.items():
      if s1 == s2:
        continue
      for i1,(a1,b1) in enumerate(edges3d):
        for i2,(a2,b2) in enumerate(edges3d):
          ta1,tb1 = tuple(t1.dot(a1)),tuple(t1.dot(b1))
          ta2,tb2 = tuple(t2.dot(a2)),tuple(t2.dot(b2))

          if (ta1,tb1) == (ta2,tb2):
            print(ta1,tb1)
          elif (ta1,tb1) == (tb2,ta2):
            print(ta1,tb1)

  return portals

print(fold(world, world_dim))
import sys; sys.exit()

def wrap2(s):
  return s

start = (next(x for x in range(*world_range[0][0]) if world[(x,0)] == '.'),0,0)
print(pw(path(start,instructions,wrap2)))
