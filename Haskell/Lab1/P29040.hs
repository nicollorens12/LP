insert :: [Int] -> Int -> [Int]
insert [] n = [n]
insert (x:xs) n
    | x <= n    = x : insert xs n
    | otherwise = n : x : xs

isort :: [Int] -> [Int] 
isort [] = []
isort (x:xs) = insert (isort xs) x

remove :: [Int] -> Int -> [Int]
remove [] _ = []
remove (x:xs) n
    | x == n    = xs
    |otherwise  = x : (remove xs n)

ssort :: [Int] -> [Int]
ssort [] = []
ssort l = reverse (auxssort l [])

auxssort :: [Int] -> [Int] -> [Int]
auxssort [] l = l
auxssort xs l = auxssort (remove xs xs_min) (xs_min : l)
    where xs_min = minimum xs

merge :: [Int] -> [Int] -> [Int]
merge [] l = l
merge l [] = l
merge (x:xs) l = merge xs (insert l x)

msort :: [Int] -> [Int]
msort [] = []
msort [x] = [x]
msort xs = 
    let (left, right) = splitAt (length xs `div` 2) xs
    in merge (msort left) (msort right)

qsort :: [Int] -> [Int]
qsort [] = []
qsort (x:xs) = 
    let smallerSorted = qsort (filter (<= x) xs)
        biggerSorted = qsort (filter (> x) xs)
    in smallerSorted ++ [x] ++ biggerSorted

genQsort :: Ord a => [a] -> [a]
genQsort [] = []
genQsort (x:xs) =
    let smallerSorted = genQsort (filter (<= x) xs)
        biggerSorted = genQsort (filter (> x) xs)
    in smallerSorted ++ [x] ++ biggerSorted



