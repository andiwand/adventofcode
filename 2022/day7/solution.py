from pathlib import Path

tree = {}

cwd = None
last_cmd = None
for l in open(Path(__file__).resolve().parent / 'input.txt'):
  l = l.strip()
  if l.startswith('$ '):
    last_cmd = l[2:]
    if last_cmd.startswith('cd '):
      path = l[5:]
      if path == '/':
        cwd = tree
      elif path == '..':
        cwd = cwd['..']
      else:
        cwd[path] = {'..': cwd}
        cwd = cwd[path]
    elif last_cmd.startswith('ls'):
      pass
    else:
      raise RuntimeError(f'dafuq unknown cmd {last_cmd}')
  else:
    if last_cmd.startswith('ls'):
      ts,n = l.split(' ')
      if ts == 'dir' and n not in cwd:
        cwd[n] = ts
      else:
        cwd[n] = int(ts)
    else:
      raise RuntimeError('dafuq')

def solve(tree):
  result = {}
  def foo(f,path):
    result[path] = ('f',f)
    if isinstance(f, dict):
      result[path] = ('d',sum(foo(f[c],f'{path}/{c}') for c in f if c != '..'))
    return result[path][1]
  foo(tree,'/')
  return result

s = solve(tree)

print(sum(s for t,s in s.values() if t == 'd' and s <= 100000))

total = 70000000
free = total - s['/'][1]
delete = 30000000 - free
print(min(s for t,s in s.values() if t == 'd' and s >= delete))
