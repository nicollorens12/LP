myMap :: (a -> b) -> [a] -> [b]
myMap _ [] = []
myMap f l = [f x | x <- l]

myFilter :: (a -> Bool) -> [a] -> [a]
myFilter f l = [x | x <- l, f x]

myZipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
myZipWith f l1 l2 = [f x y | (x, y) <- zip l1 l2]

thingify :: [Int] -> [Int] -> [(Int, Int)]
thingify l s = [(x,y) | x <- l, y <- s, mod x y == 0]

factors :: Int -> [Int]
factors n = [x | x <- [1..n], mod n x == 0]

