import Data.List

degree :: Eq a => [(a, a)] -> a -> Int
degree [] _ = 0
degree l v = if fst (head l) == v || snd (head l) == v then 1 + (degree (tail l) v) else degree (tail l) v

hasEdge :: Eq a => a -> (a,a) -> Bool
hasEdge e x = if fst x == e || snd x == e then True else False

degree' :: Eq a => [(a, a)] -> a -> Int
degree' l v = length (filter (hasEdge v) l)

filterEdge :: Eq a =>  a -> (a, a) -> a
filterEdge v x = if fst x == v then snd x else fst x

neighbors :: Ord a => [(a, a)] -> a -> [a]
neighbors l v = map (filterEdge v) (filter (hasEdge v) l)