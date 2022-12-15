from pathlib import Path
import re
import copy

f = open(Path(__file__).resolve().parent / 'input.txt')

stacks = None
for l in f:
  if l[1] == '1':
    break
  if stacks is None:
    stacks = [[] for _ in range(len(l)//4)]
  for i in range(len(l)//4):
    item = l[1+i*4]
    if item != ' ':
      stacks[i].append(item)
for i in range(len(stacks)):
  stacks[i] = stacks[i][::-1]
stacks2 = copy.deepcopy(stacks)

instructions = []
for l in f:
  if not l.strip():
    continue
  m = re.match('move (\d+) from (\d+) to (\d+)', l.strip())
  n,f,t = tuple(map(int, m.groups()))
  instructions.append((n,f-1,t-1))

for n,f,t in instructions:
  stacks[t] += stacks[f][-n:][::-1]
  stacks[f] = stacks[f][:-n]

print(''.join(s[-1] for s in stacks))

for n,f,t in instructions:
  stacks2[t] += stacks2[f][-n:]
  stacks2[f] = stacks2[f][:-n]

print(''.join(s[-1] for s in stacks2))
