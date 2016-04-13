# DevOps Notes

There is a difference between 0.0.0.0 and 127.0.0.1.  This caused this problem:
http://stackoverflow.com/questions/28727798/cant-connect-to-rails-server-running-on-ec2-from-public-ip

_502 Bad Gateway_: implication is that there's an error with the configuration of an upstream server

#### Redirect www subdomain to top level domain with S3 static sites: 
Create another bucket `www.bucketname.com` that redirects to the top level
bucket `bucketname.com`, and make a subdomain for that bucket.

