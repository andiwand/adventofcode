from pathlib import Path

f = open(Path(__file__).resolve().parent / 'input.txt')

rounds = []
for l in f:
  l = l.strip()
  s = l.split(' ')
  rounds.append((ord(s[0])-ord('A'), ord(s[1])-ord('X')))

def score(a,b):
  if a==b:
    return 3+a+1
  if a==(b+1)%3:
    return 6+a+1
  return 0+a+1

print(sum(score(r[1],r[0]) for r in rounds))

def rotate(a,b):
  if a==0:
    return b-1 if b>0 else 2
  if a==1:
    return b
  return (b+1)%3

print(sum(score(rotate(r[1],r[0]),r[0]) for r in rounds))
