import Data.List (sort, group)

countItems :: Eq a => [a] -> [(a,Int)]
countItems = map (\xs -> (head xs, length xs)) . group

main :: IO()
main = do
    contents <- getContents
    let inp = countItems (sort $ words contents)
    let out_strings = map (\(x,y) -> x ++ " " ++ show y) inp
    mapM_ putStrLn out_strings