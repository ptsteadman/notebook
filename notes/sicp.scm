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

; 1.11

(define (f n) (f-iter 0 1 2 n))

(define (f-iter a b c n)
  (if (= n 2)
    c
    (f-iter b c (+ c (* 2 b) (* 3 a)) (- n 1))))

; 1.12

(define (pascal row col) 
  (cond ((= col 0) 1)
        ((= col row) 1)
        (else 
          (+
            (pascal (- row 1) (- col 1))
            (pascal (- row 1) col)
            ))))

(= (pascal 0 0) 1)
(= (pascal 4 4) 1)
(= (pascal 2 1) 2)

; 1.16

(define (expt-iter b n a)
  (cond ((= n 0) a)
        ((even n) (expt-iter b (- n 1) (* b a)))
        (else (

  
