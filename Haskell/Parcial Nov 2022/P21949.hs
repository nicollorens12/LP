hanoi :: Int -> String -> String -> String -> [(String, String)]
hanoi 0 _ _ _ = []
hanoi n from to aux = hanoi (n - 1) from aux to ++ [(from, to)] ++ hanoi (n - 1) aux to from

main :: IO ()
main = do
    input <- getLine
    let [n, from, to, aux] = words input
        moves = hanoi (read n) from to aux
    mapM_ (\(x, y) -> putStrLn $ x ++ " -> " ++ y) moves