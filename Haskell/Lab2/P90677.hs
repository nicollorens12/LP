myFoldl :: (a -> b -> a) -> a -> [b] -> a
myFoldl f e [] = e
myFoldl f e (x:xs) = myFoldl f (f e x) xs

myFoldr :: (a -> b -> b) -> b -> [a] -> b
myFoldr f e [] = e
myFoldr f e l = myFoldr f (f (last l) e) (init l)

myIterate :: (a -> a) -> a -> [a]
myIterate f e = [e] ++ myIterate f (f e) 

myUntil :: (a -> Bool) -> (a -> a) -> a -> a
myUntil g f e = if g $ f e then f e else myUntil g f (f e)

myMap :: (a -> b) -> [a] -> [b]
myMap f [] = []
myMap f l = [f e] ++ myMap f (tail l)
    where e = head l

myFilter :: (a -> Bool) -> [a] -> [a]
myFilter f [] = []
myFilter f l = if f (head l) then [head l] ++ myFilter f (tail l) else myFilter f (tail l)

myAll :: (a -> Bool) -> [a] -> Bool
myAll _ [] = True
myAll f l = if f (head l) then myAll f (tail l) else False

myAny :: (a -> Bool) -> [a] -> Bool
myAny _ [] = False
myAny f l  = if f $ head l then True else myAny f (tail l)

myZip :: [a] -> [b] -> [(a, b)]
myZip [] [] = []
myZip _ [] = []
myZip [] _ = []
myZip l s = [(head l, head s)] ++ myZip (tail l) (tail s)

myZipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
myZipWith f [] [] = []
myZipWith f _ [] = []
myZipWith f [] _ = []
myZipWith f l s = [f (head l) (head s)] ++ myZipWith f (tail l) (tail s)