sumStrings :: [String] -> Int
sumStrings [] = 0
sumStrings (x:[]) = read x :: Int
sumStrings (x:xs) = (read x :: Int) + sumStrings xs

main :: IO ()
main = do
    string <- getContents
    let l = words string
    print $ sumStrings l