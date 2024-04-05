fizzBuzz :: [Either Int String]
fizzBuzz = [y | x <- [0..], let y = func x]

func :: Int -> Either Int String
func x 
    | mod x 3 == 0 && mod x 5 == 0 = Right "FizzBuzz"
    | mod x 3 == 0 = Right "Fizz"
    | mod x 5 == 0 = Right "Buzz"
    | otherwise = Left x