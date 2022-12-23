from pathlib import Path
from collections import Counter

elves = set()
for y,l in enumerate(open(Path(__file__).resolve().parent / 'input.txt')):
  for x,c in enumerate(l.strip()):
    if c == '#':
      elves.add((x,y))

directions = {
  'n': (0,-1),
  's': (0,1),
  'w': (-1,0),
  'e': (1,0),
  'ne': (1,-1),
  'nw': (-1,-1),
  'se': (1,1),
  'sw': (-1,1),
}

def move(p,d):
  if d is None:
    return p
  d = directions[d]
  return (p[0]+d[0],p[1]+d[1])

def valid_direction(ds):
  def do(state,p,ds=ds):
    ps = tuple(move(p,d) for d in ds)
    return all(p not in state for p in ps)
  return do

checks = {
  'n': valid_direction(['n','ne','nw']),
  's': valid_direction(['s','se','sw']),
  'w': valid_direction(['w','nw','sw']),
  'e': valid_direction(['e','ne','se'])
}

def decide_moves(state):
  def next_move(e,l,state):
    if all(move(e,d) not in state for d in directions):
      return None
    return next((d for d in l if checks[d](state,e)), None)
  return {e:next_move(e,l,state) for e,l in state.items()}

def update_state(state):
  return state[1:] + state[:1]

def world_range(state):
  return (
    (min(x for x,_ in state),max(x for x,_ in state)),
    (min(y for _,y in state),max(y for _,y in state)),
  )

def solve(state, maxsteps):
  for i in range(1,maxsteps+1):
    moves = decide_moves(state)
    dest = {e:move(e,d) for e,d in moves.items()}
    counts = Counter(dest.values())
    new_state = {}
    for e in state:
      if counts[dest[e]] != 1:
        new_state[e] = update_state(state[e])
        continue
      new_state[dest[e]] = update_state(state[e])
    if new_state.keys() == state.keys():
      break
    state = new_state
  return state,i

def answer(state):
  r = world_range(state)
  return (r[0][1]-r[0][0]+1)*(r[1][1]-r[1][0]+1)-len(state)

init_state = {e:['n','s','w','e'] for e in elves}
print(answer(solve(init_state,10)[0]))

print(solve(init_state,10000)[1])
