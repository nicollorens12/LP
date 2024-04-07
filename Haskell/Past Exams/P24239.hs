getVal :: Char -> Int
getVal v
    | v == 'M' = 1000
    | v == 'D' = 500
    | v == 'C' = 100
    | v == 'L' = 50
    | v == 'X' = 10
    | v == 'V' = 5
    | v == 'I' = 1
    | v == '0' = 0

greaterThan :: Char -> Char -> Bool
greaterThan x y = if (getVal x) > (getVal y) then True else False

roman2int :: String -> Int
roman2int [] = 0
roman2int (x:[]) = getVal x
roman2int (x:xs)
    | x == 'M' = (getVal x) + roman2int xs
    | x == 'D' && greaterThan x ((head xs)) =  (getVal x) + roman2int xs
    | x == 'D' && not (greaterThan x ((head xs))) = ((getVal (head xs)) - (getVal x)) + roman2int (tail xs) 
    | x == 'C' && (greaterThan x ((head xs)) || x == (head xs)) =  (getVal x) + roman2int xs
    | x == 'C' && not (greaterThan x ((head xs)) || x == (head xs)) = ((getVal (head xs)) - (getVal x)) + roman2int (tail xs)
    | x == 'L' && (greaterThan x ((head xs)) || x == (head xs)) =  (getVal x) + roman2int xs
    | x == 'L' && not (greaterThan x ((head xs)) || x == (head xs)) = ((getVal (head xs)) - (getVal x)) + roman2int (tail xs)
    | x == 'X' && greaterThan x ((head xs)) = (getVal x) + roman2int xs
    | x == 'X' && not (greaterThan x ((head xs))) = ((getVal (head xs)) - (getVal x)) + roman2int (tail xs)
    | x == 'V' && greaterThan x ((head xs)) =  (getVal x) + roman2int xs
    | x == 'V' && not (greaterThan x ((head xs))) = ((getVal (head xs)) - (getVal x)) + roman2int (tail xs) 
    | x == 'I' && (greaterThan x ((head xs)) || x == (head xs)) =  (getVal x) + roman2int xs
    | x == 'I' && not (greaterThan x ((head xs)) || x == (head xs)) = ((getVal (head xs)) - (getVal x)) + roman2int (tail xs)


roman2int' :: String -> Int
roman2int' [] = 0
roman2int' xs = foldl (\acc (x, y) -> if x >= y then acc + x else acc - x) 0 (zip (map getVal xs) (map getVal (tail xs ++ "0")))

nextTaylor :: Float -> Float -> Float
nextTaylor x fx = (0.5 * (fx + (x/fx)))

arrels :: Float -> [Float]
arrels x = iterate (nextTaylor x) x

arrel :: Float -> Float -> Float
arrel x e = head (dropWhile (\y -> if (abs (y - (sqrt x))) > e then True else False) (arrels x))

data LTree a = Leaf a | Node (LTree a) (LTree a) 

instance Show a => Show (LTree a) where
    show (Leaf a) = "{" ++ show a ++ "}"
    show (Node x y) = "<" ++ show x ++ "," ++ show y ++ ">"

build :: [a] -> LTree a
build [x] = Leaf x
build xs = Node (build left) (build right)
    where
        (left, right) = if mod (length xs) 2 == 0 then splitAt (div (length xs) 2) xs  else splitAt ((div (length xs) 2)+1) xs 

sameSize :: LTree a -> LTree b -> Bool
sameSize (Leaf _) (Leaf _) = True
sameSize (Node _ _) (Node _ _) = True
sameSize _ _ = False
 
zipLTrees :: LTree a -> LTree b -> Maybe (LTree (a, b))
zipLTrees (Leaf a) (Leaf b) = Just (Leaf (a, b))
zipLTrees (Node x y) (Node a b)
    | not (sameSize (Node x y) (Node a b)) = Nothing
    | otherwise = do
        left <- zipLTrees x a
        right <- zipLTrees y b
        return (Node left right)
zipLTrees _ _ = Nothing