INTRODUCTION TO COMPUTER GRAPHICS:

Three basic parts of a ray tracer: 1. ray generation (computes origin and
direction of each ray) 2. ray intersection (finds object intersecting the ray)
3. shading (computes pixel color)

for pixel in pixels: compute viewing ray find first object hit by ray and its
surface normal set pixel color value computer from hit point, light, and surface

Parallel Projection: all rays are perpendicular to the view plane points moved
along "projection direction" until they hit the image plane if image plane is
perpendicular to view plane, orthogonal, else oblique should look up some
examples of what an orthographic rendering would look
    
"You may have learned about the artistic conventions of three-point-perspective,
a system for manually constructing perspective views.  A surprising fact about
perspective is that all the rules of perspective drawing will be followed
automatically is we follow the simple mathematical rule underlying perspective:
objects are projected directly towards the eye, and they are drawn where they
meet a view plane in front of the eye."

Surface Normal: vector perpendicular to the surface 3D Parametric Lines: in
graphics we use vectors because their forms are more intuitive than the
cartesian forms.  Also easier to support in code.

8/27/14:
achingly beautiful
trillion triangles: 21 levels of detail
cultural heritage

graphics applications:
entertainment
science and engineering
virtual prototyping
cultural heritage
training and simulation
graphics art, fine art

3d modeling: differential geometry, numerical optimization, grammars
3d rendering: 2d views of 3d geometry, integrals
animation: keyframe animation (interpolation) vs physical simulation (diffeq)
images: polynomials, etc
user interaction

computer graphics: mathematics made visibile
modeling: diffuse materials

8/29/14:
cartesian product of set A and set B: all possible ordered pairs of A and B
A^2 = A x A
one to one = bijection = has inverse
frame of reference/coordinate frame: store vectors u, v and w
then we have a vector b in the canonical coordinate system
to get the u, v, w coordinates of b:
u[b] = u o b, v[b] = v o b, w[b] = w o b

9/3/14:
https://p3d.in
Use it to check vertex normals and UV coordinates, not great for diagnosing


ORAL COMMUNICATION

Dialectical: only philosophical kings know Truth Only content matters

Sophistical: hippias, gorgias -> gorgeous delivery, organization, style,
audience analysis

Rhetorical: probabilistic requires belief truth without belief without truth,
truth without belief

1. Select a topic (word, phrase, question)
2. Determine your purpose (informative, persuasive, ceremonial)
3. Research (informal, formal, library)
4. Analyze audience
5. Come up with a thesis/central idea
6. Organize speech around thesis
7. Practice and reduce notes

Invention, Organization, Style, Delivery


COMMUNICATION AND TECHNOLOGY

Discoverability: is it possible to figure out what actions are possible and how
to perform them?  Understanding: what do the settings/controls mean?

very upsetting that he is pushing a specific, non-free software "edublogs"
Industrial Design: "The professional service of creating and developing concepts
and specifications that optimize the function, value, and appearance of products
and systems for the mutual benefit of bothuser and manufacturer"

tweet @2450fall2014 about chapter 1 of Norman
set up blog site
"machines require us to be precise and accurate, things we are not very good
at"
...machines / machine-like humans as deficient
"many of the rules followed by a machine are known only by the machine and its
designers" pg. 6
"it is not our duty to understand the arbitrary, meaningless dictates of
machines" ...disagree.  should be exactly as simple

and specifications that optimize the function, value, and appearance of products
and systems for the mutual benefit of bothuser and manufacturer"

tweet @2450fall2014 about chapter 1 of Norman
set up blog site
"machines require us to be precise and accurate, things we are not very good
at"
...machines / machine-like humans as deficient
"many of the rules followed by a machine are known only by the machine and its
designers" pg. 6
"it is not our duty to understand the arbitrary, meaningless dictates of
machines" ...disagree.  should be exactly as simple

8/28/14:

key concepts from chapter 1:
 - everydayness
 - affordances: actual and perceived properties of how a thing should be used
 - visibility 
 - mappings: cultural, physical
 - feedback
 - conceptual models: design model, user model, system image

9/4/14:
information in the world: combine inforation in the world with info in head
less declarative knowledge, more procedural
great precision is not required
constraints: natural (physical) constraints, cultural constraints

NETWORKS

bipartite graphs
what are some things that can be modeled as a graph?  
matching on graphs
Internet in 1970
path: a sequence of nodes, each connected by edges
connected: path between any two nodes
is the internet today connected? ... well, by definition, probably yes
component: connected piece of a graph
visual vs non-visual graphs "to big to draw"
global friendship network has a "giant component" that contains you and most of
the world's people
could there be a second giant component?  

9/2/14: Bridge: removal would put endpoints in different components
new information tends to flow over a bridge
local bridge: an edge whose endpoints have no neighbors in common...not part of
any triangle

9/5/14: Networks with Positive and Negative Links
claim: if a complete graph is balanced, then one of two things must occur:
    - all edges are positive
    - the nodes can be divided into two groups
proof:
take any node A, x = A and A's friends
                 y = A's enemies
in a balanced world, every pair of A's friends must be friends
in a balanced world, every pair of A's enemies must be friends
in a balanced world, any pair of a friend and an enemy must be enemies

9/8/14: 


INFORMATION RETRIEVAL

cranfield test collection paradigm for evaluation
evaluation corpus: documents, queries, and relevance judgments
queries: static set of information needs that a user might want to search on
test collections drive IR research
test collection drawbacks: hard to get realistic queries...also hard to avoid
bias in relevance judgment
only cover part of what is needed: user interactions are important but
abstracted out
"Document categorization in legal electronic discovery: computer classification
vs manual review"
Less than 20% agreement with documents actually turned over
Amount of disagreement: relevance judgment doesn't necessarily effect the
ranking of systems
25 queries is the absolute minimum to be able to make general claims
50 is preferred
necessity for averaging over queries
no single perfect query standard to tune towards
so, there's been a lot of a focus on statistical methodology
effectiveness measures: A is relevant, B is retreived

recall = porportion of relevant documents retreived
precision = porportion of retreived documents that are relevant

false positive (Type I Error): a non-relevant document is retrieved
false negative (Type II Error): relevant document is not retrieved

F-Measure= Harmonic Mean of recall and precision = 2RP/(R + P)
emphasizes small values

Evaluating the effectiveness of ranking:
     - calculatig recall and precision at fixed ranking
     - calculating precision at standard recall levels
     - average precision values from the points where relevant docs
	- Mean Average Precision (MAP): assumes user is interested in finding
	  many relevant documents for each query, requires many relevance judg
     - recall precision graph
     - calculate maximum precision at any point

9/4/14: Text Acquisition and Web Crawlers
What pages should we search?
web crawler starts with set of seeds
seeds are added to a url request queue, new urls are added "frontier"
Exact duplicate detection is easy: 
Checksum: value based on the contetn of the file...Cyclic Redundancy Check (CRC)
Near Duplicate Detection: Search is O(N), Discovery is O(N^2).  Fingerprinting
Simple priority queue fails: many links out of a page go to same server
politeness policy, use threads
Mercator Scheme: URLs-> Prioritizer -> front queues of pri -> back queue router
-> back queues with single host on each -> back queue selector
Desktop Crawlers:
	- easier to find data
	- responding to updates is more important
	- must be more conservative of cpu/disk usage
	- many document formats
	- data privacy
Also, Document Feeds:
	- push feeds alerts subscriber to new documents
	- pull feed requires the subscriber to check
	- RSS: ttl (amount of time contents should

9/9/14:
BigTable:
    - No query language
    - only row level operations
    - row stores data for a single web page: row key, column key, timestamp
    - distributed
    - huge number of columns: same column groups, not necessarily the same
      columns
    - important for reducing disk/memory reads to access document data
    - rows are partitioned into tablets based on their row keys
    - tablet server allows for distribution...similar to a B tree
    - in 2006: 800TB crawl, 11% compression, 1000 billion cells, 16 column
      families
    - no locking issues: data is never overwritten
Removing Noise:
    - look at the tag/token ratio
Processing Text:
    - converting documents to a more consistent set of index terms
    - can't match strings
    - not all words are of equal value
    - Zipf's Law: rank of a word times its frequency is approximately a
      constant 0.1
    - word that occurs n times has rank k/n
    - number of words with requence n is 
    - Heap's Law: as corpus grows, so does vocabularly size slowly
    - v = k * n^b...logarithmic
    - tokenizing: small decisions in tokenzizing can have large impact on
      queries
    - small words can be important in some queries, usually in combination
    - often hyphenated and non-hyphenated forms of words are both common
    - best to defer complex decision to other components
    - stopping: removing high frequency words, but they can be important in
      combination
    - stemming: many morphological variations of words...inflectional (plurals,
      tenses), derivational (making verbs nouns...)
    - same or similar meaningsa
    - things can be done at query time or as part of indexing
    - 
