from pathlib import Path
from collections import defaultdict
import math

world = set()
wind = {}
for y,l in enumerate(open(Path(__file__).resolve().parent / 'input.txt')):
  for x,c in enumerate(l.strip()):
    p = (x,y)
    if c == '#':
      world.add(p)
    elif c in '><^v':
      wind[p] = c
world_dim = (max(x for x,_ in world)+1,max(y for _,y in world)+1)

directions = {' ':(0,0),'>':(1,0),'<':(-1,0),'^':(0,-1),'v':(0,1)}

def move(p,d):
  return tuple(p[i]+d[i] for i in range(len(p)))

def wind_evolution(wind,dim,time):
  result = defaultdict(list)
  for p,d in wind.items():
    new_p = tuple((p[i]-1+directions[d][i]*time)%(dim[i]-2)+1 for i in range(len(p)))
    result[new_p].append(d)
  return result

def wrap_wind_time(dim,time):
  return time % math.lcm(*[d-2 for d in dim])

def print_world(world,wind,dim):
  for y in range(0,dim[1]):
    for x in range(0,dim[0]):
      if (x,y) in world:
        print('#', end='')
      elif (x,y) in wind:
        v = wind[(x,y)]
        if isinstance(v,list):
          if len(v) == 1:
            v = v[0]
          elif len(v) > 1:
            v = len(v)
          else:
            raise RuntimeError('dafuq')
        print(v, end='')
      else:
        print('.', end='')
    print()

def solve(world,world_dim,wind,start,finish,wind_time,time_left,mem):
  if time_left <= 0:
    return math.inf,0
  if start == finish:
    return 0,wind_time

  fingerprint = (start,wind_time,time_left)
  if fingerprint in mem:
    return mem[fingerprint]

  next_wind_time = wrap_wind_time(world_dim,wind_time+1)
  next_wind = wind_evolution(wind,world_dim,next_wind_time)

  options = [(math.inf,0)]
  for d in directions.values():
    new_p = move(start,d)
    if any(not 0 <= new_p[i] < world_dim[i] for i in range(len(start))):
      continue
    if new_p in world or new_p in next_wind:
      continue
    options.append(solve(world,world_dim,wind,new_p,finish,next_wind_time,time_left-1,mem))

  best = min(options,key=lambda o: o[0])
  best = (1+best[0],best[1])
  mem[fingerprint] = best
  return mem[fingerprint]

import sys
sys.setrecursionlimit(10000)

start,finish = (1,0),(world_dim[0]-2,world_dim[1]-1)
s = solve(world,world_dim,wind,start,finish,0,350,{})
print(s)
s = solve(world,world_dim,wind,finish,start,s[1],350,{})
print(s)
s = solve(world,world_dim,wind,start,finish,s[1],350,{})
print(s)
