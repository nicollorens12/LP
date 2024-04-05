data Tree a = Node a (Tree a) (Tree a) | Empty deriving (Show)

size :: Tree a -> Int
size (Node _ Empty Empty) = 1
size (Node _ t1 Empty) = 1  + size t1
size (Node _ Empty t2) = 1  + size t2
size (Node _ t1 t2) = 1  + size t1 + size t2

height :: Tree a -> Int
height (Node _ Empty Empty) = 1
height (Node _ t1 Empty) = 1  + height t1
height (Node _ Empty t2) = 1  + height t2
height (Node _ t1 t2) = 1  + if ht1 > ht2 then ht1 else ht2
    where
        ht1 = height t1
        ht2 = height t2

equal :: Eq a => Tree a -> Tree a -> Bool
equal Empty Empty = True
equal (Node x1 t1 t2) (Node x2 t3 t4) = x1 == x2 && equal t1 t3 && equal t2 t4
equal _ _ = False

isomorphic :: Eq a => Tree a -> Tree a -> Bool
isomorphic Empty Empty = True
isomorphic (Node x1 t1 t2) (Node x2 t3 t4) = x1 == x2 && ((isomorphic t1 t3 && isomorphic t2 t4) || (isomorphic t1 t4 && isomorphic t2 t3))

preOrder :: Tree a -> [a]
preOrder Empty = []
preOrder (Node x Empty t1) = [x] ++ preOrder t1
preOrder (Node x t1 Empty) = [x] ++ preOrder t1
preOrder (Node x t1 t2) = [x] ++ preOrder t1 ++ preOrder t2

postOrder :: Tree a -> [a]
postOrder Empty = []
postOrder (Node x Empty t1) = postOrder t1 ++ [x]
postOrder (Node x t1 Empty) = postOrder t1 ++ [x]
postOrder (Node x t1 t2) = postOrder t1 ++ postOrder t2 ++ [x]

inOrder :: Tree a -> [a]
inOrder Empty = []
inOrder (Node x Empty t1) = [x] ++ inOrder t1
inOrder (Node x t1 Empty) = inOrder t1 ++ [x]
inOrder (Node x t1 t2) = inOrder t1 ++ [x] ++ inOrder t2

breadthFirst :: Tree a -> [a]
breadthFirst t = bf [t]
    where
        bf [] = []
        bf ts = map root ts ++ bf (concat (map children ts))
        root (Node x _ _) = x
        children (Node _ Empty Empty) = []
        children (Node _ Empty t2) = [t2]
        children (Node _ t1 Empty) = [t1]
        children (Node _ t1 t2) = [t1, t2]

build :: Eq a => [a] -> [a] -> Tree a
build (x:xs) (y:ys)
    | x == y = Node x Empty Empty
    | otherwise = Node x (build (leftPreorder xs ys) (leftPostorder xs ys)) (build (rightPreorder xs ys) (rightPostorder xs ys))
    where
        leftPreorder xs ys = takeWhile (/= head ys) xs
        leftPostorder xs ys = takeWhile (/= last xs) ys
        rightPreorder xs ys = drop (length (leftPreorder xs ys) + 1) xs
        rightPostorder xs ys = drop (length (leftPostorder xs ys) + 1) ys
build _ _ = Empty

overlap :: (a -> a -> a) -> Tree a -> Tree a -> Tree a
overlap f Empty Empty = Empty
overlap f t1 Empty = t1
overlap f Empty t2 = t2
overlap f (Node x1 t1 t2) (Node x2 t3 t4) = Node (f x1 x2) (overlap f t1 t3) (overlap f t2 t4)