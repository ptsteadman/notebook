# Review of 'CSS Secrets' by Lea Verou

I bought this book because I wanted to gain a deeper understanding of CSS, so I
don't feel like this all the time:

![Peter Griffen CSS](http://i.imgur.com/Q3cUg29.gif)

I write CSS on a pretty regular basis, but my CSS skills feel like a random
collection of hacks without any sort of foundation.  For a while, I've been
looking for some sort of book or course that would help me really understand
CSS, in the same way that [John Resig's 'Secrets of the JavaScript
Ninja'](https://www.manning.com/books/secrets-of-the-javascript-ninja) helped me
understand JavaScript, or how ['The Body Book For
Boys'](http://www.amazon.com/The-Body-Book-For-Boys/dp/0545237513) helped me
understand puberty.

Verou takes an approach that I generally like: investigate the trickiest parts
of a subject in order to understand the subject as a whole.  Besides the
(excellent) introduction which summarizes the recent history of CSS, the book is
just a series of secrets, grouped into sections like: Backgrounds, Layout and
Positioning, Animations, Text Effects, etc.  Many of the secrets link to the
blog of the discoverer, and many of these blogs are good resources in their own
right.

The first few sections are the most valuable, focusing on backgrounds,
gradients, and borders.  They build on each other, and demonstrate the power of
a part of the language you probably haven't fully considered.  The book becomes
a bit more scattered as it progresses, but overall, it is very readable.

Critically, the book focuses on CSS as it is now, not as it was six years ago.
One issue with trying to learn CSS from the Internet is that many of the top
Stack Overflow answers are from 2009, when browser support was very different.
This means that when one searches for a vertical centering solution, one might
end up implementing an ugly pseudoelement hack, when an elegant flexbox solution
exists, and has great browser support (now).

The main flaw of the book, for my purposes, was the lack of sections devoted to
high-level overview of best practices for structuring stylesheets for production
applications.  I would have liked an expert's brief on CSS best practices like
object oriented CSS, SMACSS, preprocessors, etc.  Verou spends a lot of time
trying to make her CSS very DRY, but doesn't write anything about how to make
different CSS components work together on the page.  Perhaps that is more a
design concern.  

I remember watching an excellent walk-through of the jQuery source created by
Paul Irish, I think I would benefit from something similar, but for the
Bootstrap framework.
