convertRes :: Float -> String
convertRes x
    | x < 18 = "magror"
    | x < 25 = "corpulencia normal"
    | x < 30 = "sobrepes"
    | x < 40 = "obesitat"
    | x >= 40 = "obesitat morbida"

main :: IO ()
main = do
    infoString <- getLine
    let info = words infoString
    if head info == "*" then return ()
    else do
        putStr $ head info ++ ": "
        let m = read (info !! 1 ):: Float
        let h = read (info !! 2 ):: Float
        let res = m / (h**2)
        putStrLn $ convertRes res
        main

