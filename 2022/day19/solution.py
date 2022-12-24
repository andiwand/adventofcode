from pathlib import Path
import re
import math

blueprints = []
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  m = re.match('Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', l.strip())
  g = tuple(map(int, m.groups()))
  blueprints.append(((g[1],0,0,0), (g[2],0,0,0), (g[3],g[4],0,0), (g[5],0,g[6],0)))

def sim(blueprint, robots, material, minutes, mem, build_skipper):
  if minutes <= 0:
    return material

  fingerprint = (minutes, robots, material)
  if fingerprint in mem:
    return mem[fingerprint]

  end_material = tuple(m+r*minutes for m,r in zip(material,robots))
  options = [end_material]

  def time_to_mine(m,c,r):
    if m >= c:
      return 0
    if r == 0:
      return math.inf
    return math.ceil((c-m)/r)

  for i,costs in reversed(list(enumerate(blueprint))):
    # hack to reduce combinatorics
    if build_skipper(i,minutes):
      continue

    time = 1+max(time_to_mine(m,c,r) for m,c,r in zip(material,costs,robots))
    if time > minutes:
      continue
    new_robots = tuple(r+(1 if i==j else 0) for j,r in enumerate(robots))
    new_material = tuple(m+r*time-c for m,c,r in zip(material,costs,robots))
    options.append(sim(blueprint, new_robots, new_material, minutes-time, mem, build_skipper))

  result = max(options, key=lambda x: x[3])
  mem[fingerprint] = result
  return result

def build_skipper1(i, minutes):
  return (i == 0 and minutes < 16) or (i == 1 and minutes < 7)

#print(sum(sim(blueprint, (1,0,0,0), (0,0,0,0), 24, {}, build_skipper1)[3]*(i+1) for i,blueprint in enumerate(blueprints)))
ss = 0
for i,blueprint in enumerate(blueprints):
  s = sim(blueprint, (1,0,0,0), (0,0,0,0), 24, {}, build_skipper1)
  print(i, blueprint, s)
  ss += s[3]*(i+1)
print(ss)

def build_skipper2(i, minutes):
  return (i == 0 and minutes < 24) or (i == 1 and minutes < 15)

#print(math.prod(sim(blueprint, (1,0,0,0), (0,0,0,0), 32, {}, build_skipper2)[3] for blueprint in blueprints[:3]))
ss = 1
for i,blueprint in enumerate(blueprints[:3]):
  s = sim(blueprint, (1,0,0,0), (0,0,0,0), 32, {}, build_skipper2)
  print(i, blueprint, s)
  ss *= s[3]
print(ss)
