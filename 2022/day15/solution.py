from pathlib import Path
import re

f = open(Path(__file__).resolve().parent / 'input.txt')

input = []
for l in f:
  m = re.match('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', l.strip())
  n = tuple(map(int, m.groups()))
  input.append((n[0:2], n[2:4]))

def distance(a,b):
  return sum(abs(a[i]-b[i]) for i in range(len(a)))

input = [(s,b,distance(s,b)) for s,b in input]

def solve1(input, y):
  def slice(s,r,y):
    dy = abs(s[1]-y)
    return [(s[0]+dx,y) for dx in range(-r+dy,r-dy+1)]
  covered = set()
  for s,b,r in input:
    covered.update(slice(s, r, y))
  for s,b,r in input:
    covered.discard(s)
    covered.discard(b)
  return len(covered)

print(solve1(input,10))
print(solve1(input,2000000))

def solve2(input,c):
  def outline(s,r):
    result=[]
    for x in range(-r,r+1):
      result.append((s[0]+x,s[1]+r-abs(x)))
    for x in range(-r+1,r):
      result.append((s[0]+x,s[1]+abs(x)-r))
    return result
  for s,b,r in input:
    o=outline(s,r+1)
    print('progress', s, len(o))
    for p in o:
      if not (c[0][0] <= p[0] <= c[0][1]) or not (c[1][0] <= p[1] <= c[1][1]):
        continue
      covered = any(distance(s,p)<=r for s,_,r in input)
      if not covered:
        return p
  raise RuntimeError('dafuq')

def freq(p):
  return 4000000*p[0]+p[1]

try:
  s = solve2(input,((0,20),(0,20)))
  print(s, freq(s))
except RuntimeError as e:
  print(e)
try:
  s = solve2(input,((0,4000000),(0,4000000)))
  print(s, freq(s))
except RuntimeError as e:
  print(e)
