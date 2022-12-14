from pathlib import Path
from itertools import zip_longest

f = open(Path(__file__).resolve().parent / 'input.txt')

# eval would have been easier ...
def readPacket(s):
  def read(s,p):
    if s[p] == '[':
      return readList(s,p)
    return readNumber(s,p)
  def readNumber(s,p):
    e = p
    while s[e].isdigit():
      e += 1
    return int(s[p:e]),e
  def readList(s,p):
    l = []
    p += 1
    while True:
      if s[p] == ',':
        p += 1
        continue
      if s[p] == ']':
        p += 1
        break
      i,p = read(s,p)
      l.append(i)
    return l,p
  return readList(s,0)[0]

input = []
i = iter(f)
while True:
  n = next(i)
  a = readPacket(n.strip())
  n = next(i)
  b = readPacket(n.strip())
  input.append((a,b))
  try:
    next(i)
  except:
    break

def cmp(a,b):
  if isinstance(a,int) and isinstance(b,int):
    if a < b:
      return True
    if a > b:
      return False
    return None
  if isinstance(a,list) and isinstance(b,list):
    for aa,bb in zip_longest(a,b):
      if aa is None:
        return True
      if bb is None:
        return False
      c = cmp(aa,bb)
      if c is not None:
        return c
    return None
  if isinstance(a,int):
    return cmp([a],b)
  return cmp(a,[b])

sum = 0
for i,(a,b) in enumerate(input):
  if cmp(a,b):
    sum += i+1
print(sum)

from functools import cmp_to_key

div1,div2 = [[2]],[[6]]
input = [a for a,b in input] + [b for a,b in input] + [div1,div2]

def cmp2(a,b):
  c = cmp(a,b)
  if c is None:
    raise RuntimeError('dafuq')
  return -1 if c else 1

s = sorted(input, key=cmp_to_key(cmp2))
print((s.index(div1)+1) * (s.index(div2)+1))
