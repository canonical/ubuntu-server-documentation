# Introduction to ROCK images


## What are ROCKs? ##

Ordinary software packages can often be installed in a variety of different types of environments that satisfy the given packaging system.  However, these environments can be quite varied, such as including versions of language runtimes, system libraries, and other library dependencies that the software was not well tested with.

Software containers address this by encapsulating both the software and the surrounding environment.  Instead of installing and maintaining a collection of software packages, the user runs and maintains a single container, instantiated from a container image with the desired software already installed.  The user relies on the provider of the container image to perform the necessary software testing and maintenance updates.  There is a rich ecosystem of container providers thanks to mainstream tools like Docker, and popular container registries like Docker Hub, Amazon ECR, etc., which make it easy for anyone to build and publish a container image.  Unfortunately, with that freedom and flexibility invariably comes unreliability of maintenance and inconsistency of implementation.

The *Open Container Initiative* (OCI) establishes standards for constructing container images that can be reliably installed across a variety of compliant host environments.

Ubuntu's [LTS Docker Image Portfolio](https://ubuntu.com/security/docker-images) provides OCI-compliant images that receive stable security updates and predictable software updates, thus ensuring consistency in both maintenance schedule and operational interfaces for the underlying software your software builds on.


## Container Creation and Deletion ##

Over the course of this tutorial we'll explore deriving a customized Apache container, and then networking in a Postgres container backend for it.  By the end you'll have a working knowledge of how to set up a container-based environment using Canonical's ROCKs.

First the absolute basics.  Let's spin up a single container providing the Apache2 web server software:

    $ sudo apt-get update
    $ sudo apt-get -y install docker.io
    $ sudo docker run -d --name my-apache2-container -p 8080:80 ubuntu/apache2:2.4-22.04_beta
    Unable to find image 'ubuntu/apache2:2.4-22.04_beta' locally
    2.4-22.04_beta: Pulling from ubuntu/apache2
    13c61b50dd15: Pull complete 
    34dadde438e6: Pull complete 
    d8e11cec95e6: Pull complete 
    Digest: sha256:11647ce68a130540150dfebbb755ee79c908103fafbf805074eb6513e6b9df83
    Status: Downloaded newer image for ubuntu/apache2:2.4-22.04_beta
    4031e6ed24a6e08185efd1c60e7df50f8f60c21ed9961c858ca0cb6bb300a72a


This container, named `my-apache2-container` runs in an Ubuntu 22.04 LTS environment and can be accessed via local port 8080.  Load the website up in your local web browser:

    $ firefox http://localhost:8080

![apache2-container|690x389](https://assets.ubuntu.com/v1/d81ac993-rocks_intro.png) 

If you don't have firefox handy, `curl` can be used instead:

    $ curl -s http://localhost:8080 | grep "<title>"
    <title>Apache2 Ubuntu Default Page: It works</title>

The run command had a number of parameters to it.  The Usage section of [Ubuntu's Docker hub page for Apache2](https://hub.docker.com/r/ubuntu/apache2) has a table with an overview of parameters specific to the image, and [Docker itself](https://docs.docker.com/engine/reference/commandline/run/) has a formal reference of all available parameters, but lets go over what we're doing in this particular case:

    $ sudo docker run -d --name my-apache2-container -e TZ=UTC -p 8080:80 ubuntu/apache2:2.4-22.04_beta

The `-d` parameter causes the container to be detached so it runs in the background.  If you omit this, then you'll want to use a different terminal window for interacting with the container.  The `--name` parameter allows you to use a defined name; if it's omitted you can still reference the container by its Docker id.  The `-e` option lets you set environment variables used when creating the container; in this case we're just setting the timezone (`TZ`) to universal time (`UTC`).  The `-p` parameter allows us to map port 80 of the container to 8080 on localhost, so we can reference the service as `http://localhost:8080`.  The last parameter indicates what software image we want.

A variety of other container images are provided on [Ubuntu's Docker Hub](https://hub.docker.com/r/ubuntu/) and on [Amazon ECR](https://gallery.ecr.aws/lts?page=1), including documentation of supported customization parameters and debugging tips.  This lists the different major/minor versions of each piece of software, packaged on top of different Ubuntu LTS releases.  So for example, in specifying our requested image as `ubuntu/apache2:2.4-22.04_beta` we used Apache2 version 2.4 running on a Ubuntu 22.04 environment.

Notice that the image version we requested has `_beta` appended to it.  This is called a *Channel Tag*.  Like most software, Apache2 provides incremental releases numbered like 2.4.51, 2.4.52, and 2.4.53.  Some of these releases are strictly bugfix-only, or even just CVE security fixes; others may include new features or other improvements.  If we think of the series of these incremental releases for Apache2 2.4 on Ubuntu 22.04 as running in a *Channel*, the *Channel Tags* point to the newest incremental release that's been confirmed to the given level of stability.  So, if a new incremental release 2.4.54 becomes available, `ubuntu/apache2:2.4-22.04_edge` images would be updated to that version rapidly, then `ubuntu/apache2:2.4-22.04_beta` once it's received some basic testing; eventually, if no problems are found, it will also be available in `ubuntu/apache2:2.4-22.04_candidate` and then in `ubuntu/apache2:2.4-22.04_stable` once it's validated as completely safe.

For convenience there's also a `latest` tag and an `edge` tag which are handy for experimentation or where you don't care what version is used and just want the newest available.  For example, to launch the latest version of Nginx, we can do so as before, but specifying `latest` instead of the version:

    $ sudo docker run -d --name my-nginx-container -e TZ=UTC -p 9080:80 ubuntu/nginx:latest
    4dac8d77645d7ed695bdcbeb3409a8eda942393067dad49e4ef3b8b1bdc5d584

    $ curl -s http://localhost:9080 | grep "<title>"
    <title>Welcome to nginx!</title>

We've also changed the port to 9080 instead of 8080 using the `-p` parameter, since port 8080 is still being used by our apache2 container.  If we were to try to also launch Nginx (or another Apache2 container) on port 8080, we'd get an error message, `Bind for 0.0.0.0:8080 failed: port is already allocated` and then would need to remove the container and try again.

Speaking of removing containers, now that we know how to create generic default containers, let's clean up:

    $ sudo docker ps
    CONTAINER ID   IMAGE                           COMMAND                  CREATED          STATUS          PORTS                                   NAMES
    d86e93c98e20   ubuntu/apache2:2.4-22.04_beta   "apache2-foreground"     29 minutes ago    Up 29 minutes    0.0.0.0:8080->80/tcp, :::8080->80/tcp   my-apache2-container
    eed23be5f65d   ubuntu/nginx:latest             "/docker-entrypoint.…"   18 minutes ago   Up 18 minutes   0.0.0.0:9080->80/tcp, :::9080->80/tcp   my-nginx-container

    $ sudo docker stop my-apache2-container
    $ sudo docker rm my-apache2-container

    $ sudo docker stop my-nginx-container
    $ sudo docker rm my-nginx-container

To be able to actually use the containers, we'll have to configure and customize them, which we'll look at  [next](https://discourse.ubuntu.com/t/docker-images-tutorial/28042).
