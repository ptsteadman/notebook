; 1.3

(define (sum-square a b)
  (+ (* a a)
     (* b b)))

(define (sum-squares-of-larger a b c)
  (if (and (>= a c) (>= b c)) 
    (sum-square a b)
    (sum-squares-of-larger b c a)))



