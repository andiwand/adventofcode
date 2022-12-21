from pathlib import Path
import operator

monkeys = {}
for l in open(Path(__file__).resolve().parent / 'simpleinput.txt'):
  m,i = l.strip().split(': ')
  a,b = None,None
  for o in ['+','-','*','/']:
    try:
      a,b = i.split(f' {o} ')
      break
    except:
      pass
  if a is None:
    o = 'int'
    a = int(i)
  monkeys[m] = {'o': o, 'a': a, 'b': b}

def create_eval_functions(monkeys):
  result = {}
  def fun(o,a,b):
    if o == 'int':
      return lambda a=a: a
    op = {
      '+': operator.add,
      '-': operator.sub,
      '*': operator.mul,
      '/': operator.floordiv,
    }
    return lambda a=a,b=b,f=result: op[o](f[a](),f[b]())
  for m,a in monkeys.items():
    result[m] = fun(**a)
  return result

fns = create_eval_functions(monkeys)
print(fns['root']())

def create_inverse_functions(monkeys, fns):
  result = {}
  def fun(m,o,a,b):
    op = {
      '+': (lambda r,b: r-b, lambda r,a: r-a),
      '-': (lambda r,b: r+b, lambda r,a: a-r),
      '*': (lambda r,b: r//b, lambda r,a: r//a),
      '/': (lambda r,b: r*b, lambda r,a: a//r),
    }
    return (lambda b=b,f=fns,fi=result: op[o][0](fi[m](),f[b]()), lambda a=a,f=fns,fi=result: op[o][1](fi[m](),f[a]()))
  for m,a in monkeys.items():
    if a['o'] == 'int':
      continue
    result[a['a']],result[a['b']] = fun(m,**a)
  return result

inv = create_inverse_functions(monkeys,fns)
inv[monkeys['root']['a']] = fns[monkeys['root']['b']]
inv[monkeys['root']['b']] = fns[monkeys['root']['a']]
print(inv['humn']())
