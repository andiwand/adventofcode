from pathlib import Path

wind = open(Path(__file__).resolve().parent / 'input.txt').readlines()[0].strip()
proto_blocks = [b.split('\n') for b in '\n'.join(l.strip() for l in open(Path(__file__).resolve().parent / 'blocks.txt').readlines()).split('\n\n')]

class Cycle:
  def __init__(self, list, i=0):
    self._list = list
    self._i = i
  def __next__(self):
    result = self._list[self._i]
    self._i += 1
    if self._i >= len(self._list):
      self._i = 0
    return result
  def index(self):
    return self._i

def spawn(proto_block, pos):
  result = {}
  for y,row in enumerate(proto_block[::-1]):
    for x,c in enumerate(row):
      if c != '.':
        result[(x+pos[0],y+pos[1])] = c
  return result

def move(block, delta_x, delta_y):
  return {(x+delta_x,y+delta_y):i for (x,y),i in block.items()}

def intersect(world, width, block):
  return any(((x,y) in world or x < 0 or x >= width or y < 0) for x,y in block)

def fall(world, width, wind_iter, block):
  delta_x = 1 if next(wind_iter) == '>' else -1
  tmp_block = move(block, delta_x, 0)
  if not intersect(world, width, tmp_block):
    block = tmp_block

  tmp_block = move(block, 0, -1)
  if intersect(world, width, tmp_block):
    return (block, True)

  return (tmp_block, False)

def height(world):
  if not world:
    return 0
  return max(y for _,y in world)+1

def topWorld(world, height):
  return frozenset((x,y-height) for (x,y) in world if y >= height)

def printWorld(world, block, width, height):
  for y in range(height-1, -1, -1):
    for x in range(0, width):
      if (x,y) in world:
        print(world[(x,y)],end='')
      elif (x,y) in block:
        print(block[(x,y)],end='')
      else:
        print('.',end='')
    print()

def spawnAndDrop(world, width, wind_iter, proto_blocks_iter):
  block = spawn(next(proto_blocks_iter), (2,height(world)+3))
  while True:
    block, done = fall(world, width, wind_iter, block)
    if done:
      world.update(block)
      break

def solve(world, width, wind_iter, proto_blocks_iter, n):
  offset = height(world)

  for _ in range(n):
    spawnAndDrop(world, width, wind_iter, proto_blocks_iter)

  #printWorld(world, block, width, max(h,height(block)))
  return height(world)-offset

width = 7
print(solve({}, width, Cycle(wind), Cycle(proto_blocks), 2022))

def solve2(world, width, wind_iter, proto_blocks_iter, blocks, depth):
  def find_period(world, width, wind_iter, proto_blocks_iter, depth):
    mem = {}
    i = 0
    while True:
      fingerprint = (proto_blocks_iter.index(), wind_iter.index(), topWorld(world, height(world)-depth))
      if fingerprint in mem:
        return mem[fingerprint],(i,height(world))
      mem[fingerprint] = i,height(world)
      spawnAndDrop(world, width, wind_iter, proto_blocks_iter)
      i += 1

  (b1,h1),(b2,h2) = find_period(world, width, wind_iter, proto_blocks_iter, depth)

  period_blocks = b2-b1
  period_height = h2-h1
  missing_blocks = blocks-b1
  cycles, remainder_blocks = missing_blocks//period_blocks, missing_blocks%period_blocks

  h3 = solve(world, width, wind_iter, proto_blocks_iter, remainder_blocks)

  return h1 + period_height*cycles + h3

blocks = 1000000000000
depth = 5
print(solve2({}, width, Cycle(wind), Cycle(proto_blocks), blocks, depth))
