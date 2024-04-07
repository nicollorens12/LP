import Data.List(sort)

equalSum :: Int -> [Int] -> Bool
equalSum x ls = x == sum ls

allSublists :: [Int] -> [[Int]]
allSublists [] = [[]] 
allSublists (x:xs) = let rest = allSublists xs
                     in rest ++ map (x:) rest

sumEquals2 :: Int -> [Int] -> Maybe [Int]
sumEquals2 _ [] = Nothing  
sumEquals2 s xs = case reverse (sumEquals1 s (sort xs)) of 
                    [] -> Nothing  -- Si sumEquals1 devuelve una lista vacía, no hay subconjunto con suma s
                    (y:_) -> Just y  -- Tomamos el primer elemento de la lista, que será el subconjunto más grande en orden lexicográfico

