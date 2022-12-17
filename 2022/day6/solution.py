from pathlib import Path

def solve(s,length):
  for i,s in enumerate(zip(*[l[k:] for k in range(length)])):
    if len(set(s)) == length:
      return i+length
  raise RuntimeError('dafuq')

for l in open(Path(__file__).resolve().parent / 'input.txt'):
  print(solve(l.strip(), 4), solve(l.strip(), 14))
