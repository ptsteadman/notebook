# Review of 'CSS Secrets' by Lea Verou

I bought this book because I wanted to gain an understanding of CSS.  I write
CSS on a pretty regular basis, but my CSS skills feel like a random collection
of hacks and habits without any sort of foundation.  For a while, I've been
looking for some sort of book or course that would help me really understand
CSS, in the same way that John Resig's 'Secrets of the JavaScript Ninja' helped
me understand JavaScript, or how 'The Body Book For Boys' helped me understand
puberty.

Verou takes an approach that I generally like: investigate the trickiest parts
of a subject in order to understand the subject as a whole.  Besides the
(excellent) introduction which summarizes the recent history of CSS, the book is
just a series of secrets, grouped into sections like: Backgrounds, Layout and
Positioning, Animations, Text Effects, etc.  Many of the secrets link to the
blog of the discoverer, and many of these blogs are good resources in their own
right.

The first few sections focused on backgrounds, gradients, and borders have the
most value.  They build on each other, and demonstrate the power of a part of
the language you probably hadn't considered.  The book becomes a bit more
scattered as it progresses, but overall, it is very readable.

Critically, the book focuses on CSS as it is now, not as it was six years ago.
One issue with trying to learn CSS from the Internet is that many of the top
stack overflow answers are from 2009, when browser support was very different.
This means that when you search for a vertical centering solution, you might end
up implementing an ugly pseudoelement hack, when an elegant flexbox solution
exists, and has great browser support (now).

The main flaw of the book, for my purposes, was the lack of sections devoted to
high-level overview of best practices for structuring stylesheets in production
applications.  I would have liked to read an expert's brief on CSS best
practices like object oriented CSS, SMACSS, preprocessors, etc.  Verou spends a
lot of time trying to make her CSS very DRY, but doesn't write anything about
how to make different CSS components work together.  Perhaps that is more a
design concern.
