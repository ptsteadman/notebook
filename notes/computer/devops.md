# DevOps Notes

There is a difference between 0.0.0.0 and 127.0.0.1.  This caused this problem:
http://stackoverflow.com/questions/28727798/cant-connect-to-rails-server-running-on-ec2-from-public-ip

_502 Bad Gateway_: implication is that there's an error with the configuration of an upstream server

#### Redirect www subdomain to top level domain with S3 static sites: 
Create another bucket `www.bucketname.com` that redirects to the top level
bucket `bucketname.com`, and make a subdomain for that bucket.

#### Generate a static key

#### When SSL Cert Works on Desktop but not Mobile

The report from SSLabs says:

  This server's certificate chain is incomplete. Grade capped to B.
  ....
  Chain Issues                  Incomplete

Desktop browsers often have chain certificates cached from previous connections
or download them from the URL specified in the certificate. Mobile browsers and
other applications usually don't.

Fix your chain by including the missing certificates and everything should be
right.

The CA sends two files: your cert, and a bundle representing their authority to
grand you a cert.  They need to be bundled again, your cert first.  The md5 hash
of the bundle you create and the private key should be the same.

#### Video Tag Constantly Loading

Keeping devtools open with a looped video causes constant downloading.  Managed
to burn through 600 gb of transfer bandwidth just by having my devtools open
while developing...

#### Manual Update of letsencrypt Certificate

1. `sudo service nginx stop` to stop nginx so letsencrypt can do its thing

2. `cd letsencrypt; sudo ./letsencrypt-auto`

3. select 'redirect to HTTPS'

4. `sudo service apache2 stop`

5. `sudo service nginx start`

#### arp-scan

`sudo apt install arp-scan`
`sudo arp-scan -i eth0 192.168.0.0/24`

#### review-deploy
