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

def solve_bfs(world,world_dim,wind,start,finish):
  def step(states,wind):
    new_states = set()
    for p,g in states:
      for d in directions.values():
        new_p = move(p,d)
        if any(not 0 <= new_p[i] < world_dim[i] for i in range(len(start))):
          continue
        if new_p in world or new_p in wind:
          continue
        new_g = g + (1 if new_p == finish[g] else 0)
        new_states.add((new_p,new_g))
    return new_states

  states = [(start,0)]
  time = 1
  while True:
    next_wind = wind_evolution(wind,world_dim,time)
    states = step(states,next_wind)
    if (finish[-1],len(finish)) in states:
      return time
    time += 1

start,finish = (1,0),(world_dim[0]-2,world_dim[1]-1)
print(solve_bfs(world,world_dim,wind,start,[finish]))
print(solve_bfs(world,world_dim,wind,start,[finish,start,finish]))
