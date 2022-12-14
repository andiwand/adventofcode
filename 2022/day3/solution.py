from pathlib import Path

f = open(Path(__file__).resolve().parent / 'input.txt')

rucksacks = []
for l in f:
  l = l.strip()
  rucksacks.append(l)

def prio(i):
  if ord('a') <= ord(i) <= ord('z'):
    return ord(i) - ord('a') + 1
  if ord('A') <= ord(i) <= ord('Z'):
    return ord(i) - ord('A') + 27
  raise RuntimeError('dafuq')

sol = 0
for r in rucksacks:
  a,b = r[:len(r)//2], r[len(r)//2:]
  s = set(a).intersection(set(b))
  sol += sum(prio(i) for i in s)
print(sol)

sol = 0
for i in range(0,len(rucksacks),3):
  a,b,c = rucksacks[i:i+3]
  s = set(a).intersection(set(b)).intersection(set(c))
  sol += sum(prio(i) for i in s)
print(sol)
