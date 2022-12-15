from pathlib import Path
import re

f = open(Path(__file__).resolve().parent / 'input.txt')

pairs = []
for l in f:
  m = re.match('(\d+)-(\d+),(\d+)-(\d+)',l.strip())
  pair = tuple(map(int, m.groups()))
  pairs.append((pair[0:2], pair[2:4]))

def contains(a,b):
  return a[0] <= b[0] <= b[1] <= a[1]

s = sum(1 for a,b in pairs if contains(a,b) or contains(b,a))
print(s)

def overlap(a,b):
  return a[0] <= b[0] <= a[1]

s = sum(1 for a,b in pairs if overlap(a,b) or overlap(b,a))
print(s)
