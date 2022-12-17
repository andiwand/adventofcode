from pathlib import Path
import re

valves = {}
tunnels = {}
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  m = re.match('Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)', l.strip())
  f,p,t = m.groups()
  valves[f] = int(p)
  tunnels[f] = tuple(t.split(', '))

def shortest_paths(start, tunnels):
  result = {start: 0}
  queue = [start]
  while queue:
    c = queue.pop()
    for n in tunnels[c]:
      if n not in result or result[c]+1<result[n]:
        result[n]=result[c]+1
        queue.append(n)
  return result

working_valves = set(v for v in valves if valves[v] > 0)
shortest = {v:shortest_paths(v,tunnels) for v in ['AA'] + list(working_valves)}

def pressure(open_valves):
  return sum(valves[s] for s in open_valves)

def solve(start, minutes, available_valves, dp):
  if minutes == 0:
    return 0
  if len(available_valves) == 0:
    return 0

  fingerprint = (start, minutes, available_valves)

  if fingerprint in dp:
    return dp[fingerprint]

  options = [0]

  for v in available_valves:
    d = shortest[start][v]
    minutes_remaining = minutes-d-1
    if minutes_remaining < 0:
      continue
    s = solve(v, minutes_remaining, frozenset(available_valves-set([v])), dp)
    options.append(s+valves[v]*minutes_remaining)

  best = max(options)
  dp[fingerprint] = best
  return dp[fingerprint]

dp = {}
s = solve('AA', 30, frozenset(working_valves), dp)
print(s, len(dp))

import itertools

s = 0
for i in range(0, len(working_valves)//2+1):
  for available_valves1 in itertools.combinations(working_valves, i):
    available_valves1 = frozenset(available_valves1)
    s1 = solve('AA', 26, available_valves1, dp)
    s2 = solve('AA', 26, frozenset(working_valves - available_valves1), dp)
    if s1+s2 > s:
      s = s1+s2
print(s, len(dp))
