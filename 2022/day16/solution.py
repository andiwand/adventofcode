from pathlib import Path
import re

valves = {}
tunnels = {}
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  m = re.match('Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)', l.strip())
  f,p,t = m.groups()
  valves[f] = int(p)
  tunnels[f] = tuple(t.split(', '))

working_valves = sum(1 for _,p in valves.items() if p > 0)

def pressure(open_valves):
  return sum(valves[s] for s in open_valves)

def solve(start, minutes, open_valves, dp, path):
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
    options.append(solve(start, minutes-1, next_open, dp, [f'open {start}'] if path is not None else None))

  for n in tunnels[start]:
    options.append(solve(n, minutes-1, open_valves, dp, [f'goto {n}'] if path is not None else None))

  best = max(options, key=lambda x: x[0])
  dp[fingerprint] = (best[0]+current, path+best[1] if path is not None else None)
  return dp[fingerprint]

dp = {}
s = solve('AA', 30, frozenset(), dp, ['start AA'])
print(s, len(dp))

def solve2(start, start2, minutes, open_valves, dp, path):
  if minutes == 0:
    return (0, path)

  fingerprint = (frozenset([start, start2]), minutes, open_valves)

  if fingerprint in dp:
    return dp[fingerprint]

  current = pressure(open_valves)

  if len(open_valves) == working_valves:
    dp[fingerprint] = (current*minutes, path)
    return dp[fingerprint]

  def options_args(start):
    result = []

    if valves[start] > 0 and start not in open_valves:
      result.append((start, start, f'open {start}'))

    for n in tunnels[start]:
      result.append((n, None, f'goto {n}'))

    return result

  options = []

  for n,o,m in options_args(start):
    for n2,o2,m2 in options_args(start2):
      if o is not None and o == o2:
        continue
      next_open = frozenset(open_valves | set(i for i in [o,o2] if i is not None))
      options.append(solve2(n, n2, minutes-1, next_open, dp, [f'{m} {m2}'] if path is not None else None))

  best_score, best_path = max(options, key=lambda x: x[0])
  dp[fingerprint] = (current+best_score, path+best_path if path is not None else None)
  return dp[fingerprint]

dp = {}
s = solve2('AA', 'AA', 26, frozenset(), dp, None)
print(s, len(dp))
