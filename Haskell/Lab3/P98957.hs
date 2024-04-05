import Data.List (group)

ones :: [Integer]
ones = repeat 1

nats :: [Integer]
nats = [0..]

ints :: [Integer]
ints = [0] ++ concat [[x, -x] | x <- [1..]]

triangulars :: [Integer]
triangulars = [y | x <- [0..],  let y =  div  (x * (x+1))  2]


factorials :: [Integer]
factorials = scanl (*) 1 [1..]

fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

primes :: [Integer]
primes = sieve [2..]
  where
    sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p > 0]


hammings :: [Integer]
hammings = [x | x <- [1..], mod x 2 == 0 || mod x 3 == 0 || mod x 5 == 0]

lookNsay :: [Integer]
lookNsay = iterate f 1
  where
    f x = read $ concatMap (\x -> show (length x) ++ [head x]) $ group $ show x

tartaglia :: [[Integer]]
tartaglia = iterate (\row -> zipWith (+) ([0] ++ row) (row ++ [0])) [1]