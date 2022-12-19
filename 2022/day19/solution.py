from pathlib import Path
import re
import math

blueprints = []
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  m = re.match('Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', l.strip())
  g = tuple(map(int, m.groups()))
  blueprints.append(((g[1],0,0,0), (g[2],0,0,0), (g[3],g[4],0,0), (g[5],0,g[6],0)))

def sim(blueprint, robots, material, minutes, mem):
  if minutes <= 0:
    return material

  fingerprint = (minutes, robots, material)
  if fingerprint in mem:
    return mem[fingerprint]

  end_material = tuple(m+r*minutes for m,r in zip(material,robots))
  options = [end_material]

  def timeToMine(m,c,r):
    if m >= c:
      return 0
    if r == 0:
      return math.inf
    return math.ceil((c-m)/r)

  for i,costs in reversed(list(enumerate(blueprint))):
    # hack to reduce combinatorics
    if i == 0 and minutes < 16+8:
      continue
    if i == 1 and minutes < 7+8:
      continue

    time = 1+max(timeToMine(m,c,r) for m,c,r in zip(material,costs,robots))
    if time > minutes:
      continue
    new_robots = tuple(r+(1 if i==j else 0) for j,r in enumerate(robots))
    new_material = tuple(m+r*time-c for m,c,r in zip(material,costs,robots))
    options.append(sim(blueprint, new_robots, new_material, minutes-time, mem))

  result = max(options, key=lambda x: x[3])
  mem[fingerprint] = result
  return result

#print(sum(sim(blueprint, (1,0,0,0), (0,0,0,0), 24, {})[3]*(i+1) for i,blueprint in enumerate(blueprints)))
ss = 0
for i,blueprint in enumerate(blueprints):
  s = sim(blueprint, (1,0,0,0), (0,0,0,0), 24, {})
  print(i, blueprint, s)
  ss += s[3]*(i+1)
print(ss)

#print(math.prod(sim(blueprint, (1,0,0,0), (0,0,0,0), 32, {})[3] for blueprint in blueprints[:3]))
ss = 1
for i,blueprint in enumerate(blueprints[:3]):
  s = sim(blueprint, (1,0,0,0), (0,0,0,0), 32, {})
  print(i, blueprint, s)
  ss *= s[3]
print(ss)
