from pathlib import Path

input = []
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  d,l = l.strip().split(' ')
  input.append((d,int(l)))

def sign(x):
  if x == 0:
    return 0
  return 1 if x > 0 else -1

def sim(init, input):
  def step(state,d):
    result = []

    head = state[0]
    if d == 'R':
      new_head = (head[0]+1, head[1])
    elif d == 'L':
      new_head = (head[0]-1, head[1])
    elif d == 'U':
      new_head = (head[0], head[1]+1)
    elif d == 'D':
      new_head = (head[0], head[1]-1)
    else:
      raise RuntimeError('dafuq')
    result.append(new_head)

    def step_tail(new_front, old_tail):
      dist = tuple(new_front[i]-old_tail[i] for i in range(len(new_front)))
      absdist = tuple(abs(d) for d in dist)
      if max(absdist) <= 1:
        new_tail = old_tail
      else:
        new_tail = tuple(old_tail[i]+sign(dist[i]) for i in range(len(new_front)))
      return new_tail

    for i in range(1,len(state)):
      result.append(step_tail(result[i-1], state[i]))

    return tuple(result)

  state = init
  result = [state]
  for d,l in input:
    for _ in range(l):
      state = step(state,d)
      result.append(state)

  return result

def print_points(points, width, height):
  for y in range(height,-1,-1):
    for x in range(0,width+1):
      print('#' if (x,y) in points else '.',end='')
    print()

print(len(set(t for _,t in sim(((0,0),(0,0)), input))))

print(len(set(s[-1] for s in sim(tuple((0,0) for _ in range(10)), input))))
