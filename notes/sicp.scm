; 1.3

(define (sum-square a b)
  (+ (* a a)
     (* b b)))

(define (sum-squares-of-larger a b c)
  (if (and (>= a c) (>= b c)) 
    (sum-square a b)
    (sum-squares-of-larger b c a)))

; 1.7

(define (good-enough? guess x)
  (< (abs (- guess x)) .001))

(define (cube-root x guess)
  (if (good-enough? (* guess guess guess) x )
    guess
    (cube-root-iter (improve guess x) x)))
 
(define (improve guess x) 
  (/
    (+ (* 2 guess) (/ x (* guess guess)))
    3)
  )



