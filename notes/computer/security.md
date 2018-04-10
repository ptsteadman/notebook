# Security

### XSS: Cross-Site Scripting

#### Non-persistent XSS Vulnerability:

A classic example of a potential vector is a site search engine: if one searches
for a string, the search string will typically be redisplayed verbatim on the
result page to indicate what was searched for. If this response does not
properly escape or reject HTML control characters, a cross-site scripting flaw
will ensue.  (Because same origin policy: the script could load a JS tag that
sends privileged data back to a server).

A reflected attack is typically delivered via email or a neutral
web site. The bait is an innocent-looking URL, pointing to a trusted site but
containing the XSS vector. If the trusted site is vulnerable to the vector,
clicking the link can cause the victim's browser to execute the injected script.

#### Persistent XSS Vulnerability:

The persistent (or stored) XSS vulnerability is a more devastating variant of a
cross-site scripting flaw: it occurs when the data provided by the attacker is
saved by the server, and then permanently displayed on "normal" pages returned
to other users in the course of regular browsing, without proper HTML escaping. 

To do this, for the question "Describe your Ideal First Date", Mallory gives a
short answer (to appear normal) but the text at the end of her answer is her
script to steal names and emails. If the script is enclosed inside a <script>
element, it won't be shown on the screen. Then suppose that Bob, a member of the
dating site, reaches Mallory’s profile, which has her answer to the First Date
question. Her script is run automatically by the browser and steals a copy of
Bob’s real name and email directly from his own machine.</script>

### CSRF: Cross-Site Request Forgery 

Cross-site request forgery, also known as one-click attack or session riding and
abbreviated as CSRF (sometimes pronounced sea-surf) or XSRF, is a type of
malicious exploit of a website where unauthorized commands are transmitted from
a user that the website trusts.  Unlike cross-site scripting (XSS), which
exploits the trust a user has for a particular site, CSRF exploits the trust
that a site has in a user's browser.

If an attacker is able to find a reproducible link that executes a specific
action on the target page while the victim is logged in there, they are able to
embed such link on a page they control and trick the victim into opening it.[1]
The attack carrier link may be placed in a location that the victim is likely to
visit while logged into the target site (e.g. a discussion forum), sent in a
HTML email body or attachment. A real CSRF vulnerability in uTorrent
(CVE-2008-6586) exploited the fact that its web console accessible at
localhost:8080 allowed mission-critical actions to be executed as a matter of
simple GET request:

