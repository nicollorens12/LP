multEq :: Int -> Int -> [Int]
multEq x y = iterate (* (x*y)) 1

firstOccured :: Int -> [Int] ->  [Int] -> Bool
firstOccured x l [] = if elem x l then True else False
firstOccured _ [] _ = False
firstOccured x (e2:l2) (e3:l3)
    | x == e3 = False
    | x == e2 = True
    | otherwise = firstOccured x l2 l3

selectFirst :: [Int] -> [Int] -> [Int] -> [Int]
selectFirst [] _ _ = []
selectFirst _ [] _ = []
selectFirst l1 l2 l3
    | notElem (head l1) l2 = selectFirst (tail l1) l2 l3
    | elem (head l1) l2 && length l3 == 0 = [head l1] ++ selectFirst (tail l1) l2 l3
    | firstOccured (head l1) l2 l3 = [head l1] ++ selectFirst (tail l1) l2 l3
    | otherwise = selectFirst (tail l1) l2 l3

myIterate :: (a -> a) -> a -> [a]
myIterate f n = scanl (\x _ -> f x) n (repeat n)

type SymTab a = String -> Maybe a

empty :: SymTab a
empty = \_ -> Nothing

get :: SymTab a -> String -> Maybe a
get l e = l e

set :: SymTab a -> String -> a -> SymTab a
set l e v = \x -> if x == e then Just v else l x

data Expr a = Val a | Var String | Sum (Expr a) (Expr a) | Sub (Expr a) (Expr a) | Mul (Expr a) (Expr a)
    deriving Show

eval :: (Num a) => SymTab a -> Expr a -> Maybe a
eval st (Val x) = Just x
eval st (Var x) = get st x
eval st (Sum expr1 expr2) = do
                                x <- (eval st expr1)
                                y <- (eval st expr2)
                                return (x + y)
eval st (Sub expr1 expr2) = do
                                x <- (eval st expr1)
                                y <- (eval st expr2)
                                return (x - y)
eval st (Mul expr1 expr2) = do
                                x <- (eval st expr1)
                                y <- (eval st expr2)
                                return (x * y)