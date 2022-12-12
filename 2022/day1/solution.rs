use std::fs;

fn main() {
  let contents = fs::read_to_string("input.txt").expect("fail");

  let mut cals = Vec::<i32>::new();
  for block in contents.split("\n\n") {
    let mut sum = 0;
    for c in block.split("\n") {
      if c.is_empty() {
        continue;
      }
      sum += c.parse::<i32>().unwrap();
    }
    cals.push(sum);
  }

  cals.sort();

  println!("{}", cals.last().expect("please"));

  println!("{}", cals.iter().rev().take(3).sum::<i32>());
}
