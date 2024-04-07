data Queue a = Queue [a] [a]
     deriving (Show)
 
create :: Queue a
create = Queue [] []

push :: a -> Queue a -> Queue a
push x (Queue xs ys) = Queue xs (x:ys)

pop :: Queue a -> Queue a
pop (Queue [][]) = error "empty queue"
pop (Queue (x:xs) ys) = Queue xs ys
pop (Queue [] ys) = pop $ Queue (reverse ys) []


top :: Queue a -> a
top (Queue [][]) =  error "empty queue"
top (Queue (x:_)_) = x
top (Queue [] ys) = top $ Queue (reverse ys) []

empty :: Queue a -> Bool
empty (Queue[][]) = True
empty _ = False


instance Eq a => Eq (Queue a)
    where
        (==) (Queue xs ys) (Queue xs1 ys1) = (xs ++ reverse ys) == (xs1 ++ reverse ys1)