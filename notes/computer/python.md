# Python Notes

## Dependency Management

Problem: ansible wouldn't work because NameError 'basestring'...why?  Cause of
problem: ansible doesn't work with Python3, and anaconda was overriding PATH,
even in virtualenv Fix: remove the ansible PATH thing pointing at Python3.5

### The equivalent of npm install:

- `virtualenv .venv` creates the `.venv` directory, which stores
  the python bin and the modules you install with pip
- `. .venv/bin/activate` activates the virtualenv: now pip, python etc will
  be use the `.venv` directory
- `pip install -r requirements.txt` installs the dependencies

## Django Stuff

Token Based Auth:

- Django Rest Framework's default token-based auth has a lot of problems!

Unique constraint across fields:
    unique_together = ('field1', 'field2')

django-oauth-toolkit is best.  Your front end application becomes an
`application` in the same way you set up a Twitter 'app' or a Facebook 'app',
via Oauth.  Pretty elegant.

## Issue With MySQL-python

After upgrading my Ubuntu to 16.04, I was getting the error:

```
ImportError: libmysqlclient.so.18: cannot open shared object file: No such file
or directory
```

The command `/sbin/ldconfig -p | grep mysql` revealed that I had
`libmysqlclient.so.20`, so it was obviously a versioning issue.

I tried reinstalling with pip and it didn't work.  I even `cleaned` my
virtualenv: same problem.

Eventually the command that fixed things was `pip install --no-binary
MySQL-python MySQL-python`.

Apparently there was possibly a problem with a 'cached wheel'.  Wheels seem to
be superior archives of egg distributions.  Using the `--no-binary` flag, I
suppose, causes it to find the native apt package or something, and deal with
the .20 version of the `.so` file. 

## Random

- no case statement
- snake_case for variables and functions
- tuples are immutable (makes sense), represent structure
- get index of tuple element: tup.index('hello')

