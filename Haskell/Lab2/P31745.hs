flatten :: [[Int]] -> [Int]
flatten x = foldl (++) [] x

myLength :: String -> Int
myLength l = foldl (+) 0 (map (\x -> 1) l)

myReverse :: [Int] -> [Int]
myReverse l = foldl (flip (:)) [] l

countIn :: [[Int]] -> Int -> [Int] 
countIn l x = map (\y -> length (filter (==x) y)) l

firstWord :: String -> String
firstWord l = takeWhile (/=' ') (dropWhile (==' ') l)