from pathlib import Path

cals = []

batch = []
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  l = l.strip()
  if not l:
    cals.append(sum(map(int, batch)))
    batch = []
  else:
    batch.append(l)

print(max(cals))

print(sum(sorted(cals)[-3:]))
