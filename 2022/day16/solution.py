from pathlib import Path
import re

valves = {}
tunnels = {}
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  m = re.match('Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)', l.strip())
  f,p,t = m.groups()
  valves[f] = int(p)
  tunnels[f] = tuple(t.split(', '))

def pressure(open_valves):
  return sum(valves[s] for s in open_valves)

def solve(valves, working_valves, tunnels, start, minutes, open_valves, dp, path):
  if minutes == 0:
    return (0, path)

  fingerprint = (start, minutes, open_valves)

  if fingerprint in dp:
    return dp[fingerprint]

  current = pressure(open_valves)

  if len(open_valves) == working_valves:
    dp[fingerprint] = (current*minutes, path)
    return dp[fingerprint]

  options = []

  if valves[start] > 0 and start not in open_valves:
    next_open = frozenset(open_valves | set([start]))
    options.append(solve(valves, working_valves, tunnels, start, minutes-1, next_open, dp, [f'open {start}'] if path is not None else None))

  for n in tunnels[start]:
    options.append(solve(valves, working_valves, tunnels, n, minutes-1, open_valves, dp, [f'goto {n}'] if path is not None else None))

  best = max(options, key=lambda x: x[0])
  dp[fingerprint] = (best[0]+current, path+best[1] if path is not None else None)
  return dp[fingerprint]

working_valves = sum(1 for _,p in valves.items() if p > 0)

dp = {}
s = solve(valves, working_valves, tunnels, 'AA', 30, frozenset(), dp, ['start AA'])
print(s, len(dp))

import itertools

s = 0
for i in range(working_valves//2-4, working_valves//2+1):
  for new_valves in itertools.combinations([v for v in valves if valves[v] > 0], i):
    new_valves1 = {v:0 for v in valves} | {v:valves[v] for v in new_valves}
    new_valves2 = {v:0 for v in valves} | {v:valves[v] for v in set(valves)-set(new_valves)}
    a = solve(new_valves1, i, tunnels, 'AA', 26, frozenset(), {}, None)
    b = solve(new_valves2, working_valves-i, tunnels, 'AA', 26, frozenset(), {}, None)
    if a[0]+b[0] > s:
      s = a[0]+b[0]
print(s)
