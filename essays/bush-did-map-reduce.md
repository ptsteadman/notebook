# How 9/11 Motivated Google News and Big Data

Pitch: How 9/11 Motivated the Development of Google News and Big Data

Hello ----,

I'm curious if ---- would be interested in a piece along these lines.

On the morning of September 11th, 2001, Amit Singhal, director of search quality
at Google, was away at a conference in upstate New York. As the public searched
for news about the attacks on the Twin Towers and the Pentagon, Amit and his
colleagues realized that Google was dramatically failing to meet the nation's
information needs. Searches for "World Trade Center" led to web pages detailing
the architecture of the now-destroyed buildings, or the lunch menu at the
'Windows on the World' restaurant.

In 2001, Google was only able to index the internet about once a month, and
therefore the index used to fulfill searches did not reflect the current,
dramatically different state of the world.

Over a conference call, Amit and the Google engineers decided on a hacky
solution: they hand-edited the HTML of the Google homepage to include links to
relevant news articles. This didn't work: the massive amounts of traffic
directed to these articles caused the news network's servers to crash almost
instantly.

Terrorism had revealed a major limit of the era's information processing
systems.

Amit and Krishna Bararat, a search architecture engineer, were stuck at the
conference center until planes were allowed to fly again. Over the next few
days, they sketched out the architecture of an internal tool that would
eventually become Google News. The system would index news websites constantly,
ensuring that Google would be able to provide information about events that had
just happened. Building this system would require rethinking Google's entire
data pipeline. New programming models for distributed systems would need to be
created in order to have enough computing power to concurrently index thousands
of websites.

Over the next few years, Google built and expanded their news platform, but Amit
and other Google execs like Marissa Mayer realized that everything else also
needed to be indexed in "real time".  In order to index the whole internet,
every day, the programming techniques used to create Google News would have to
be formalized.  In addition, Google realized that the rest of the internet had
to catch up with Google. To address both of these concerns, in 2004 Google
released "the MapReduce paper", which explained the abstractions Google had
developed in order to reason about their complicated distributed systems.

MapReduce is a process by which data can be mapped to many computers by a
'magic' hash function, and reduced to useful information. A MapReduce platform
like Hadoop enables programmers and businesses to solve problems in a
distributed way without explicitly managing the cost of said distribution. This
pattern became fundamental to Web 2.0 businesses.  Many web 2.0 companies manage
their own complexity by using abstractions to efficently offload work to
different nodes, or process user data to generate value. For example, in 2013
Facebook used a MapReduce cluster with over eighty powerful servers just to
compute 'recommended friends'...

...

Reserach I'd like to do: try to contact Amit Singhal (who was recently ousted
from Uber due to a sexual harrassment accustation at Google), Krishna Bharat, or
others involved.  Read more about MapReduce paper, the development of Hadoop at
Yahoo. Determine whether or not MapReduce was key to Web 2.0, Big Data. Talk
about what comes next.

Good primary sources exist, example: https://youtu.be/mTBShTwCnD4?t=2m

Let me know if you'd like to talk further.

Thanks,
Patrick

