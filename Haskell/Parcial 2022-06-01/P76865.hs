data Tree a = Empty | Node a (Tree a) (Tree a)
         deriving (Show)

instance Foldable Tree where
    foldr f z Empty = z
    foldr f z (Node x t1 t2) = foldr f (f x (foldr f z t2)) t1

avg :: Tree Int -> Double
avg Empty = 0
avg (Node x t1 t2) = fromIntegral (sum (Node x t1 t2)) / fromIntegral (length (Node x t1 t2))

cat :: Tree String -> String
cat = foldl (\acc x -> acc ++ " " ++ x) ""
