; 1.3

(define (sum-square a b)
  (+ (* a a)
     (* b b)))

(define (sum-squares-of-larger a b c)
  (if (and (>= a c) (>= b c)) 
    (sum-square a b)
    (sum-squares-of-larger b c a)))

; 1.7 (define (good-enough? guess x)
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
        ((= 0 (modulo n 2)) (expt-iter (* b b) (/ n 2) a))
        (else (expt-iter b (- n 1) (* b a)))))

(= (expt-iter 2 2 1) 4)
(= (expt-iter 2 0 1) 1)
(= (expt-iter 3 2 1) 9)
(= (expt-iter 3 3 1) 27)
(= (expt-iter 9 2 1) 81)
(= (expt-iter 2 8 1) 256)

  
; 1.17

(define (halve a) (/ a 2))
(define (double a) (+ a a))

(define (* a b)
  (cond 
    ((= b 0) 0) 
    ((= (modulo b 2) 0) (double (* a (halve b))))
    (else (+ a (* a (- b 1))))))

(define (* a b c)
  (cond
    ((= b 0) 0)
    ((= b 1) a)
    ((= (modulo b 2) 0) (* (double a) (halve b) c))
    (else (* (+ a a) (- b 1)))
  )
)


; 1.20
; Euclid's Algorithm for finding GCD of two positive integers

(define (gcd a b)
  (if (= b 0)
    a
    (gcd b (remainder a b))))

; Applicative order evalation, how many remainder operations are performed?

(gcd 206 40)
(if (= 40 0) 206 (gcd 40 (remainder 206 40))) 
(gcd 40 (remainder 206 40)) ; remainder
(gcd 40 6) 
(if (= 6 0) 40 (gcd 6 (remainder 40 6))) 
(gcd 6 (remainder 40 6)) ; remainder
(gcd 6 4)
(if (= 4 0) 6 (gcd 4 (remainder 6 4))) 
(gcd 4 (remainder 6 4)) ; remainder
(gcd 4 2)
(if (= 2 0) 4 (gcd 2 (remainder 4 2))) 
(gcd 2 (remainder 4 2)) ; remainder
(gcd 2 0)
(if (= 0 0) 2 (gcd 2 (remainder 2 0)))
2

; 4 remainder operations

; Normal order evaluation
(gcd 206 40)
(if (= 40 0) 206 (gcd 40 (modulo 206 40))) 
(gcd 40 (modulo 206 40))
(if (= (modulo 206 40) 0) 40 (gcd (modulo 206 40) (modulo 40 (modulo 206 40))))
(gcd (modulo 206 40) (modulo 40 (modulo 206 40)))

(if (= 40 0) 206 (gcd 40 6)) 
(if (= 40 0) 
  206  
  (if (= 6 0) 40 (gcd 6 (modulo 40 6)))) ; modulo
(if (= 40 0) 
  206  
  (if (= 6 0) 40 (gcd 6 4)))
(if (= 40 0) 
  206  
  (if (= 6 0) 
    40 
    (if (= 4 0)
      6 
      (gcd 4 (modulo 6 4))))) ; modulo
(if (= 40 0) 
  206  
  (if (= 6 0) 
    40 
    (if (= 4 0)
      6 
      (gcd 4 2)))) 
(if (= 40 0) 
  206  
  (if (= 6 0) 
    40 
    (if (= 4 0)
      6 
      (if (= 2 0)
        4 
        (gcd 2 (modulo 4 2)))))) ; modulo
(if (= 40 0) 
  206  
  (if (= 6 0) 
    40 
    (if (= 4 0)
      6 
      (if (= 2 0)
        4 
        (gcd 2 0))))) 
(if (= 40 0) 
  206  
  (if (= 6 0) 
    40 
    (if (= 4 0)
      6 
      (if (= 2 0)
        4 
        (if (= 0 0)
          2 
          (gcd 0 (modulo 2 0))))))) ; modulo
(if (= 40 0) 
  206  
  (if (= 6 0) 
    40 
    (if (= 4 0)
      6 
      (if (= 2 0)
        4 
        (if (= 0 0)
          2 
          (gcd 0 (modulo 2 0))))))) ; modulo
; can't take (modulo 2 0).  6 operations, last one failing
