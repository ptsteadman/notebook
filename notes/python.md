# Python Notes

## Dependency Management

Problem: ansible wouldn't work because NameError 'basestring'...why?
Cause of problem: ansible doesn't work with Python3, and anaconda was overriding PATH, even in virtualenv
Fix: remove the ansible PATH thing pointing at Python3.5

### The equivalent of npm install:
- `virtualenv .venv` creates the `.venv` directory, which stores
  the python bin and the modules you install with pip
- `. .venv/bin/activate` activates the virtualenv: now pip, python etc will
  be use the `.venv` directory
- `pip install -r requirements.txt` installs the dependencies

## Django Stuff

- Django Rest Framework's default token-based auth has a lot of problems!

Unique constraint across fields:
    unique_together = ('field1', 'field2')

## Random

- no case statement
- snake_case for variables and functions
