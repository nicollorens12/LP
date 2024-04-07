data Queue a = Queue [a] [a]
     deriving (Show)
 
create :: Queue a
create = Queue [] []

push :: a -> Queue a -> Queue a
push x (Queue xs ys) = Queue xs (x:ys)


instance Eq a => Eq (Queue a)
    where
        (==) (Queue xs ys) (Queue xs1 ys1) = (xs ++ reverse ys) == (xs1 ++ reverse ys1)

instance Functor Queue where
    fmap f (Queue l s) = Queue (map f l) (map f s)

translation :: Num b => b -> Queue b -> Queue b
translation f q = fmap (+ f) q

instance Monad Queue where
    return x = Queue [x] []
    q >>= f  = foldr push create (fmap f q)

kfilter :: (p -> Bool) -> Queue p -> Queue p
kfilter f q = 
    do
        x <- q
        if f x then return x else create
