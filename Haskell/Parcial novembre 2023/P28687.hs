import Data.Ratio

factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

termesCosinus :: Rational -> [Rational]
termesCosinus r = myIterate (\x -> (-1**x) * (r**(2*x)) / factorial (2*n )) 1
    where n = 1
