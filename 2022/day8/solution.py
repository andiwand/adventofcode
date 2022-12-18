from pathlib import Path

trees = []
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  l = l.strip()
  trees.append([int(i) for i in l])

def isVisible(trees, p):
  return (
    all(trees[p[0]][x]<trees[p[0]][p[1]] for x in range(p[1])) or
    all(trees[p[0]][x]<trees[p[0]][p[1]] for x in range(p[1]+1,len(trees[0]))) or
    all(trees[y][p[1]]<trees[p[0]][p[1]] for y in range(p[0])) or
    all(trees[y][p[1]]<trees[p[0]][p[1]] for y in range(p[0]+1,len(trees)))
  )

print(sum(1 for y in range(len(trees)) for x in range(len(trees[0])) if isVisible(trees, (y,x))))

def count(it, offset):
  result = 0
  try:
    while True:
      if not next(it):
        return result+offset
      result += 1
  except StopIteration:
    return result

def scenicScore(trees, p):
  return (
    count((trees[p[0]][p[1]-x]<trees[p[0]][p[1]] for x in range(1,p[1]+1)), 1) *
    count((trees[p[0]][p[1]+x]<trees[p[0]][p[1]] for x in range(1,len(trees[0])-p[1])), 1) *
    count((trees[p[0]-y][p[1]]<trees[p[0]][p[1]] for y in range(1,p[0]+1)), 1) *
    count((trees[p[0]+y][p[1]]<trees[p[0]][p[1]] for y in range(1,len(trees)-p[0])), 1)
  )

print(max(scenicScore(trees, (y,x)) for y in range(len(trees)) for x in range(len(trees[0]))))
