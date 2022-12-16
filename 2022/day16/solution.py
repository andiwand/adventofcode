from pathlib import Path
import re

valves = {}
tunnels = {}
for l in open(Path(__file__).resolve().parent / 'simpleinput.txt'):
  m = re.match('Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)', l.strip())
  f,p,t = m.groups()
  valves[f] = int(p)
  tunnels[f] = tuple(t.split(', '))

working_valves = sum(1 for _,p in valves.items() if p > 0)

def solve(start, minutes, open_valves, dp, path):
  def pressure(open_valves):
    return sum(valves[s] for s in open_valves)

  fingerprint = (start, minutes, open_valves)

  if fingerprint in dp:
    return dp[fingerprint]

  current = pressure(open_valves)

  if len(open_valves) == working_valves:
    dp[fingerprint] = (current*minutes, path)
    return dp[fingerprint]

  if minutes == 0:
    return (0, path)

  options = []

  if valves[start] > 0 and start not in open_valves:
    next_open = frozenset(open_valves | set([start]))
    options.append(solve(start, minutes-1, next_open, dp, [f'open {start}']))

  for n in tunnels[start]:
    options.append(solve(n, minutes-1, open_valves, dp, [f'goto {n}']))

  best = max(options, key=lambda x: x[0])
  dp[fingerprint] = (best[0]+current, path+best[1])
  return dp[fingerprint]

s = solve('AA', 30, frozenset(), {}, ['start AA'])
print(s)
