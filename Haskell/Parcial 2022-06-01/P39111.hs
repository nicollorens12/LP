import Data.List (sort)

type Pos = (Int, Int)

dins :: Pos -> Bool
dins (x,y)
    | x > 1 && x < 9 && y > 1 && y < 9 = True
    | otherwise = False

moviments :: Pos -> [Pos]
moviments (x,y) = filter dins [(x+1,y+2),(x-1,y+2),(x+1,y-2),(x-1,y-2),(x+2,y+1),(x+2,y-1),(x-2,y+1),(x-2,y-1)]

potAnar3 :: Pos -> Pos -> Bool
potAnar3 inicial final = elem final (concat $ map moviments (concat $ map moviments (moviments inicial)))

potAnar3' :: Pos -> Pos -> Bool
potAnar3' inicial final = elem final (concatMap moviments (concatMap moviments (moviments inicial)))