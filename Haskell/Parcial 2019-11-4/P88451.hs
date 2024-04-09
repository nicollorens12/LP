data Tree a = Empty | Node a (Tree a) (Tree a)

instance Show a => Show (Tree a) where 
    show (Empty) = "()"
    show (Node x t1 t2) = "(" ++ show t1 ++ "," ++ show x ++ "," ++ show t2 ++ ")"

instance Functor (Tree) where
    fmap f Empty = Empty
    fmap f (Node x t1 t2) =  (Node (f x) (fmap f t1) (fmap f t2))

doubleT :: Num a => Tree a -> Tree a
doubleT t = fmap (*2) t

data Forest a = Forest [Tree a] deriving (Show)

instance Functor (Forest) where
    fmap _ (Forest []) = Forest []
    fmap f (Forest trees) = Forest (map (fmap f) trees)

doubleF :: Num a => Forest a -> Forest a
doubleF (Forest []) = Forest []
doubleF (Forest trees) = Forest (fmap doubleT trees)