import Data.Ord
import Data.List

votsMinim :: [([Char], Int)] -> Int -> Bool
votsMinim [] _ = False
votsMinim (x:xs) vots = if (snd x) < vots then True else votsMinim xs vots

orderBySecond :: Ord b => (a, b) -> (a, b) -> Ordering
orderBySecond = comparing snd

candidatMesVotat :: [([Char], Int)] -> [Char]
candidatMesVotat l = fst (maximumBy orderBySecond l)

getNames :: [([Char], Int)] -> [[Char]]
getNames [] = []
getNames (x:xs) = [(fst x)] ++ (getNames xs)

votsIngressos :: [([Char], Int)] -> [([Char], Int)] -> [[Char]]
votsIngressos [] ingressosL = []
votsIngressos (x:xs) ingressosL
    | not $ elem (fst x) names = [fst x] ++ votsIngressos xs ingressosL
    | otherwise = votsIngressos xs ingressosL
    where 
        names = getNames ingressosL

votsMinim :: [([Char], Int)] -> Int -> Bool
votsMinim [] _ = False
votsMinim (x:xs) vots = if (snd x) < vots then True else votsMinim xs vots

orderBySecond :: Ord b => (a, b) -> (a, b) -> Ordering
orderBySecond = comparing snd

candidatMesVotat :: [([Char], Int)] -> [Char]
candidatMesVotat l = fst (maximumBy orderBySecond l)

getNames :: [([Char], Int)] -> [[Char]]
getNames [] = []
getNames (x:xs) = [(fst x)] ++ (getNames xs)

votsIngressos :: [([Char], Int)] -> [([Char], Int)] -> [[Char]]
votsIngressos [] ingressosL = []
votsIngressos (x:xs) ingressosL
    | not $ elem (fst x) names = [fst x] ++ votsIngressos xs ingressosL
    | otherwise = votsIngressos xs ingressosL
    where 
        names = getNames ingressosL

rics :: [([Char], Int)] -> [([Char], Int)] -> [[Char]]
rics vots ingressos = map addAsterisk $ take 3 $ sortBy (flip orderBySecond) ingressos
  where
    addAsterisk (name, _) = name ++ "*"
