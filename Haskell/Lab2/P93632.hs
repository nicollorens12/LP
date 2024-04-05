eql :: [Int] -> [Int] -> Bool
eql x y = if length x == length y then foldl (&&) True (zipWith (==) x y) else False

prod :: [Int] -> Int 
prod l = foldl (*) 1 l

prodOfEvens :: [Int] -> Int
prodOfEvens x = foldl (*) 1 (filter even x)

powersOf2 :: [Int]
powersOf2 = iterate (*2) 1

scalarProduct :: [Float] -> [Float] -> Float
scalarProduct x y = foldl (+) 0 (zipWith (*) x y)