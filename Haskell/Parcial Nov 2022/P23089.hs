import Data.List

myUnfoldr :: (b -> Maybe (a, b)) -> b -> [a]
myUnfoldr f x = case f x of
                  Just (elem, nextX) -> elem : myUnfoldr f nextX
                  Nothing            -> []

myReplicate :: a -> Int -> [a]
myReplicate e n = myUnfoldr (\n-> if n == 0 then Nothing else Just (e, n -1)) n

myIterate :: (a -> a) -> a -> [a] 
myIterate f x = myUnfoldr (\n -> Just (n, f n)) x

myMap :: (a -> b) -> [a] -> [b]
myMap f l = myUnfoldr (\l -> case l of
                              [] -> Nothing
                              x:xs -> Just (f x, xs)) l