# Docker and docker-compose

- `docker ps -a` all docker files, even the non-running ones

- `docker build -t tag-name .` builds a docker image with the tag tag-name,
  looking for a Dockerfile in the current directory

- `docker images` lists the docker images you have locally

- Installing `docker-compose`: the curl command probably works best, might need
  to clear executable cache [link](https://docs.docker.com/compose/install/)

- Running just one command on a docker image: `docker-compose run foo cowsay`

For docker on Linux, the containers run as the root user.

