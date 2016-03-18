# Structure And Interpretation of Computer Programming Notes

Lecture One:

- Computer Science is not really a science, and is only tangentially related to
  computers.  Geometry was originally about surveying land with surveying tools.

- Concerned with procedures, not just declarative knowledge.

- A form of engineering of the ideal, rather than of reality.  The constraints
  we face are those of our own mind.

- 'Detail suppression.'

- 'We're going to express in Lisp the way that Lisp itself works.'

Tools to manage complexity:
- Black box abstraction.  Allows for composition of procedures.
- Conventional interfaces.  Generic operations, large scale structure,
  aggregates (streams).
- Metalinguistic abstraction.  Making new languages.

Exercise 1.5:
Applicative vs. Normal Order Evaluation, with applicative order (evaluate
arguments, and then apply operator), `test` never terminates.  With normal order
evaluation, (fully expand), it evaluates to true.

Applicative order:
- left arg
- right arg
- operator

Normal order:
- operator
- left arg
- right arg

Chapter 1.1.7:

Newton's Method:
'A method for finding successively better approximations to the roots/zeros of a
real valued function.'  x1 = x0 - f(x0)/f'(x0)

Exercise 1.6:
- if is a special form that does not evaluate the falsey conditional
    
