from pathlib import Path

f = open(Path(__file__).resolve().parent / 'input.txt')

hill = {}
start = None
end = None
for i,l in enumerate(f):
  for j,c in enumerate(l.strip()):
    if c == 'S':
      start = (i,j)
      c = 'a'
    if c == 'E':
      end = (i,j)
      c = 'z'
    hill[(i,j)] = ord(c)

def neighbors(hill, p):
  return [nn for nn in [(p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1)] if nn in hill]

def solve(hill, start, end):
  dp = {start:0}
  options = {}
  curr = start
  while True:
    if curr == end:
      break

    for nn in neighbors(hill, curr):
      if hill[nn] > hill[curr]+1:
        continue
      if nn not in dp:
        if nn not in options or options[nn] > dp[curr]+1:
          options[nn] = dp[curr]+1

    if len(options) == 0:
      break

    next = None
    for p,c in options.items():
      if next is None or options[next] > c:
        next = p
    dp[next] = options[next]
    del options[next]
    curr = next
  return dp[end] if end in dp else None

print(solve(hill, start, end))

ss = []
for p,e in hill.items():
  if e == ord('a'):
    s = solve(hill, p, end)
    if s:
      ss.append(s)
print(min(ss))
# would be more optimal if we start at the and and decent until we find the first 'a'
