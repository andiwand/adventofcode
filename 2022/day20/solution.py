from pathlib import Path

numbers = [int(l.strip()) for l in open(Path(__file__).resolve().parent / 'input.txt')]

def move(l,i,d):
  j = (i+d)%(len(l)-1)
  tmp = l[:i] + l[i+1:]
  return tmp[:j] + [l[i]] + tmp[j:]

def mixing(numbers,times=1):
  result = numbers
  for _ in range(times):
    for n,i in numbers:
      j = result.index((n,i))
      result = move(result,j,n)
  return result

def coordinates(m):
  i0 = [i for i,(n,_) in enumerate(m) if n == 0][0]
  return sum(m[(i0+i)%len(numbers)][0] for i in [1000,2000,3000])

numbers = [(n,i) for i,n in enumerate(numbers)]

print(coordinates(mixing(numbers)))

key = 811589153
numbers2 = [(n*key,i) for n,i in numbers]
print(coordinates(mixing(numbers2, 10)))
