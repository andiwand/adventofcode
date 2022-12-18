from pathlib import Path

instructions = [l.strip() for l in open(Path(__file__).resolve().parent / 'input.txt').readlines()]

def sim(instructions, X):
  result = [X]
  for i in instructions:
    i = i.split(' ')
    if i[0] == 'noop':
      result.append(X)
    elif i[0] == 'addx':
      result.append(X)
      X += int(i[1])
      result.append(X)
    else:
      raise RuntimeError('dafuq')
  return result

print(sim(['noop', 'addx 3', 'addx -5'], 1))

s = sim(instructions, 1)
print(sum(s[i-1]*i for i in [20, 60, 100, 140, 180, 220]))

def display(s):
  result = []
  crt_row = ''
  for i in s:
    if i-1<=len(crt_row)<=i+1:
      crt_row += '#'
    else:
      crt_row += '.'
    if len(crt_row) >= 40:
      result.append(crt_row)
      crt_row = ''
  return result

print('\n'.join(display(s)))
