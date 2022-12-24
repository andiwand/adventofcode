from pathlib import Path

f = open(Path(__file__).resolve().parent / 'input.txt')

def parse_monkey(it):
  try:
    next(it)
  except StopIteration:
    return None
  items = list(map(int, next(it).strip()[len('Starting items: '):].split(', ')))
  operation, operand = next(it).strip()[len('Operation: new = old '):].split(' ')
  if operand == 'old':
    operation = lambda x: x*x
  else:
    operand = int(operand)
    operation = (lambda x: x+operand) if operation=='+' else (lambda x: x*operand)
  check = int(next(it).strip()[len('Test: divisible by '):])
  throwTrue = int(next(it).strip()[len('If true: throw to monkey '):])
  throwFalse = int(next(it).strip()[len('If false: throw to monkey '):])
  try:
    next(it)
  except StopIteration:
    pass
  return {
    'items': items,
    'operation': operation,
    'check': check,
    'throw_true': throwTrue,
    'throw_false': throwFalse,
    'inspections': 0,
  }

monkeys = []
it = iter(f)
while True:
  m = parse_monkey(it)
  if m is None:
    break
  monkeys.append(m)
import copy
monkeys2 = copy.deepcopy(monkeys)

def play_round(monkeys, divider, mod):
  def turn(m):
    for i in m['items']:
      m['inspections'] += 1
      w = m['operation'](i)
      w = w//divider
      w = w % mod
      if w % m['check'] == 0:
        monkeys[m['throw_true']]['items'].append(w)
      else:
        monkeys[m['throw_false']]['items'].append(w)
    m['items'] = []
  for m in monkeys:
    turn(m)

import math

mod = math.prod(m['check'] for m in monkeys)

for _ in range(20):
  play_round(monkeys, 3, mod)

s = math.prod(sorted(m['inspections'] for m in monkeys)[-2:])
print(s)

for _ in range(10000):
  play_round(monkeys2, 1, mod)
s = math.prod(sorted(m['inspections'] for m in monkeys2)[-2:])
print(s)
