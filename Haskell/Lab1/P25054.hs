myLength :: [Int] -> Int
myLength [] = 0
myLength (x:xs) = 1 + myLength xs

myMaximum :: [Int] -> Int
myMaximum [x] = x
myMaximum (x:xs) = if x > myMaximum xs then x else myMaximum xs

mySum :: [Int] -> Int
mySum [] = 0
mySum (x:xs) = x + mySum xs

average :: [Int] -> Float
average [] = 0
average xs = fromIntegral (mySum xs) / fromIntegral (myLength xs)

buildPalindrome :: [Int] -> [Int] 
buildPalindrome [] = []
buildPalindrome xs = reverse xs ++ xs

removeElem :: [Int] -> Int -> [Int]
removeElem [] _ = []
removeElem (x:xs) n = if x == n then removeElem xs n else [x] ++ removeElem xs n

remove :: [Int] -> [Int] -> [Int]
remove [] _ = []
remove l [] = l
remove l (x:xs) = remove (removeElem l x) xs

flatten :: [[Int]] -> [Int]
flatten [[]] = []
flatten [x] = x
flatten xs = (head xs) ++ flatten (tail xs)

oddsNevens :: [Int] -> ([Int],[Int])
oddsNevens [] = ([], [])
oddsNevens (x:xs)
    | even x = (odds, x:evens)
    | otherwise = (x:odds, evens)
    where
        (odds, evens) = oddsNevens xs

primeDivisors :: Int -> [Int]
primeDivisors n = factorize n 2
    where
        factorize 1 _ = []
        factorize k d
            | k `mod` d == 0 = d : factorize (k `div` d) d
            | otherwise = factorize k (d + 1)