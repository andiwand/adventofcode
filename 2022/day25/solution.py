from pathlib import Path

snafu_d = {'2':2,'1':1,'0':0,'-':-1,'=':-2}
snafu_id = {v:k for k,v in snafu_d.items()}
snafu_b = lambda i: 5**i

def from_snafu(x):
  return sum(snafu_d[c]*snafu_b(i) for i,c in enumerate(x[::-1]))

def to_snafu(x):
  def digit_gen(x):
    while x != 0:
      d = x % 5
      if d >= 3:
        d = d-5
        x -= d
      x = x // 5
      yield d
  return ''.join(snafu_id[d] for d in digit_gen(x))[::-1]

numbers = [l.strip() for l in open(Path(__file__).resolve().parent / 'input.txt')]

print(to_snafu(sum(from_snafu(n) for n in numbers)))
