main :: IO ()

main = do
    line <- getLine
    if last line == 'a' then do
        putStrLn $ "Hola maca!" 
        main
    else do
        putStrLn $ "Hola maco!"
        main