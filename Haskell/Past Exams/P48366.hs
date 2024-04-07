eval2 :: String -> Int
eval2 expr = head $ foldl evalStack [] (words expr)
  where
    evalStack :: [Int] -> String -> [Int]
    evalStack (x:y:ys) "+" = (y + x) : ys
    evalStack (x:y:ys) "-" = (y - x) : ys
    evalStack (x:y:ys) "*" = (y * x) : ys
    evalStack (x:y:ys) "/" = (y `div` x) : ys
    evalStack xs numStr = read numStr : xs

fsmap :: a -> [a -> a] -> a
fsmap e [] = e
fsmap e flist  = fsmap ((head flist) e ) (tail flist)

