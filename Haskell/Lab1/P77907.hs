absValue :: Int -> Int

absValue x = if x < 0 then x*(-1) else x

power :: Int -> Int -> Int 
power x p = x^p

isPrime :: Int -> Bool
isPrime n
  | n <= 1 = False
  | n == 2 = True
  | even n = False
  | otherwise = not $ any (\x -> n `mod` x == 0) [3,5..(floor . sqrt . fromIntegral) n]

slowFib :: Int -> Int 

slowFib 0 = 0
slowFib 1 = 1
slowFib n = slowFib(n-2) + slowFib(n-1)

quickFib :: Int -> Int
quickFib n = fibs !! n
  where
    fibs = 0 : 1 : zipWith (+) fibs (tail fibs)