# Bush Did Map Reduce

When I arrived at Cornell for my sophomore year, I was determined to set myself
up for a prestigious internship.  In early September I put on my blazer and went
to the career fair, held in the vaulted old armory building, now an indoor
track. 

I found that I enjoyed talking to the tech companies more than the banks.  When
I talked to the banks, I had this sense of emptiness: neither the recruiters or
I seemed to know what we were talking about, what exactly the **work** was.  I
felt like no information was being exchanged.  With the tech companies, at least
I could stretch my superficial knowledge of programming and talk about
something, learn something.

One specific overweight neckbeard made a lasting impression by me. 

"Do you know what Hadoop is?" he asked.

"No, what is it?" I asked.

"Oh, man.  The next big thing.  The current big thing," he said,
rocking back and forth.

"Like, what is it though?"

"It's Apache's distributed MapReduce framework.  It's how we can process
millions of ad slots a minute.  You should really look it up."

I did look it up, and felt the familiar sense of wondering what was really going
on: were terms like Hadoop, and NoSQL, or NodeJS, just buzzwords, like the names
of bands in high school, or the different sectors at an investment bank?  Or did
they **actually matter**?  

Over a year later, I would smile when I implemented the PageRank algorithm using
the Hadoop framework for my Database Systems class.  Computer Science had turned
out to be more than emptiness, for me.

And a year after **that**, one of the men indirectly responsible for the
creation of Hadoop spoke in my Information Retrieval class.  I was fascinated,
because I had watched a video where he talked about the role of 9/11 in Google's
history.  I had developed a pet theory: that the attack on the Twin Towers had
directly prompted the creation of the Map Reduce programming paradigm, and the
Hadoop framework that enabled many of the "big data" applications of the later
2000s.

Here's what I learned:

On September 11th, 2001, Amit Singhal, director of search quality at Google, was
away at a conference. As the public searched for news about the attacks on the
Twin Towers and the Pentagon, Amit and his colleagues realized that Google was
dramatically failing to meet the nation's information need. Searches for ``World
Trade Center'' led to web pages detailing the architecture of the now-destroyed
buildings, or the lunch menu at the 'Windows on the World' restaurant.  

In 2001, Google was only able to index the internet about once a month, and
therefore the index used to fulfill searches did not reflect the current,
dramatically different reality.  

Over a conference call, Amit and the Google engineers decided on a hacky
solution: they directly added links to relevant news articles on Google's
homepage.  This didn't work: the massive amounts of traffic directed to these
articles caused the news network's servers to crash almost instantly.

Bin Laden had exposed a serious weakness.

Amit and Krishna Bararat, a search architecture engineer, were stuck at the
conference center until planes were allowed to fly again.  Over the next few
days, they sketched out the architecture of what would become Google News, a
system that would index news websites constantly, ensuring that Google would be
able to provide information about events that had just happened.  Building this
system would require rethinking Google's entire data pipeline.  New programming
models for distributed systems would need to be perfected in order to have
enough computing power to simulataneously index thousands of news websites.

Over the next few years, Google built and expanded their news platform, but Amit
and Google realized that everything else also needed to be indexed in ``real
time''.  In order to index the whole internet, every day, the programming
methods used to create Google News would have to be formalized.  In addition,
Google realized that the rest of the internet had to catch up with Google.  To
address both of these concerns, in 2003 Krishna released ``the MapReduce
paper'', which explained the abstractions Google had developed in order to
reason about their complicated distributed systems.  

Something in the nature of MapReduce felt very current and zeitgeisty to me.  It
reminded me of how ``real life'' was starting to feel: many many isolated bits
of data being mapped by an abstraction, fragmented by an hash function, and then
reduced to useful key-value pairs.
