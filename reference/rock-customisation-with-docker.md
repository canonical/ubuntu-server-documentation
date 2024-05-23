# ROCK customisation with Docker


In the [last section](https://discourse.ubuntu.com/t/docker-images-introduction/27993) we looked at the basics of how to start and stop containers.  Here we'll apply our own modifications to the images.

You'll recall we used the `-p` parameter to give the two containers we created different ports so they didn't conflict with each other.  We can think of this type of customization as a *container configuration*, as opposed to an *image configuration* change defined in the `Dockerfile` settings for the image itself.  From a single image definition we can create an arbitrary number of different containers with different ports (or other pre-defined aspects), which are all otherwise reliably identical.  A third approach is to modify the running container after it has been launched, applying whatever arbitrary changes we wish as *runtime modifications*.

* **image configuration**:  Done in `Dockerfile`, changes common to all container instances of that image.  Requires rebuilding the image.

* **container configuration**:  Done at container launch, allowing variation between instances of a given image.  Requires re-launching the container to change.

* **runtime modifications**:  Done dynamically after container launch.  Does not require re-launching the container.

The second approach follows Docker's immutable infrastructure principle, and is what the ROCKs system intends for production environments.  For the sake of this tutorial we'll use the third approach for introductory purposes, building on that later to show how to achieve the same with only configuration at container creation time.


## Setting up a Development Environment ##

Speaking of doing things properly, let's prepare a virtual machine (VM) to do our tutorial work in.

While you can of course install the `docker.io` package directly on your desktop, as you may have done in the previous section of this tutorial, using it inside a VM has a few advantages.  First, it encapsulates the system changes you want to experiment with, so that they don't affect your desktop; if anything gets seriously messed up you just can delete the VM and start over.  Second, it facilitates experimenting with different versions of Ubuntu, Docker, or other tools than would be available from your desktop.  Third, since "The Cloud" is built with VM's, developing in a VM from the start lets you more closely emulate likely types of environments you'll be deploying to.

There are a number of different VM technologies available, any of which will suit our purposes, but for this tutorial we'll set one up using Canonical's Multipass software, which you can install [on Windows using a downloadable installer](https://multipass.run/docs/installing-on-windows), or [on macOS via brew](https://multipass.run/docs/installing-on-macos), or [any flavor of Linux via snapd](https://multipass.run/docs/installing-on-linux).

Here's how to launch a Ubuntu 22.04 VM with a bit of extra resources, and log in:

    host> multipass launch --cpus 2 --mem 4G --disk 10G --name my-vm daily:20.04
    host> multipass shell my-vm

If later you wish to suspend or restart the VM, use the stop/start commands:

    host> multipass stop my-vm
    host> multipass start my-vm

Go ahead and set up your new VM devel environment with Docker, your preferred editor, and any other tools you like having on hand:

    $ sudo apt-get update
    $ sudo apt-get -y install docker.io


## Data Customization ##

The most basic customization for a webserver would be the index page.  Let's replace the default one with the typical hello world example:

    $ echo '<html><title>Hello Docker...</title><body>Hello Docker!</body></html>' > index.html

The technique we'll use to load this into the webserver container is called *bind mounting a volume*, and this is done with the `-v` (or `--volume`) flag to `docker run` (not to be confused with `docker -v` which of course just prints the docker version).  A *volume* is a file or directory tree or other data on the host we wish to provide via the container.  A *bind mount* means rather than copying the data *into* the container, we establish a linkage between the local file and the file in the container.  Have a look at how this works:

    $ sudo docker run -d --name my-apache2-container -e TZ=UTC -p 8080:80 -v "${HOME}/index.html:/var/www/html/index.html" ubuntu/apache2:latest
    ...

    $ curl http://localhost:8080
    <html><title>Hello Docker...</title></html>

    $ sudo docker inspect -f "{{ .Mounts }}" my-apache2-container
    [{bind  /home/ubuntu/index.html /var/www/html/index.html   true rprivate}]

Watch what happens when we change the `index.html` contents:

    $ echo '<html><title>...good day!</title></html>' > index.html

    $ curl http://localhost:8080
    <html><title>...good day</title></html>

This linkage is two-way, which means that the container itself can change the data.  (We mentioned *runtime modifications* earlier -- this would be an example of doing that.)

    $ sudo docker exec -ti my-apache2-container /bin/bash

    root@abcd12345678:/# echo '<html><title>Hello, again</title></html>' > /var/www/html/index.html
    root@abcd12345678:/# exit
    exit

    $ curl http://localhost:8080
    <html><title>Hello, again</title></html>

What if we don't want that behavior, and don't want to grant the container the ability to do so?  We can set the bind mount to be read-only by appending `:ro`:

    $ sudo docker stop my-apache2-container
    $ sudo docker rm my-apache2-container
    $ sudo docker run -d --name my-apache2-container -e TZ=UTC -p 8080:80 -v ${HOME}/index.html:/var/www/html/index.html:ro ubuntu/apache2:latest

    $ sudo docker exec -ti my-apache2-container /bin/bash

    root@abcd12345678:/# echo '<html><title>good day, sir!</title></html>' > /var/www/html/index.html
    bash: /var/www/html/index.html: Read-only file system

    root@abcd12345678:/# exit

    $ curl http://localhost:8080
    <html><title>Hello, again</title></html>

However, the read-only mount still sees changes on the host side:

    $ echo '<html><title>I said good day!</title></html>' > ./index.html

    $ curl http://localhost:8080
    <html><title>I said good day!</title></html>

This same approach can be used to seed database containers:

    $ echo 'CREATE DATABASE my_db;' > my-database.sql
    $ sudo docker run -d --name my-database -e TZ=UTC \
         -e POSTGRES_PASSWORD=mysecret \
         -v $(pwd)/my-database.sql:/docker-entrypoint-initdb.d/my-database.sql:ro \
         ubuntu/postgres:latest

The `docker-entrypoint-initdb.d/` directory we're using here is special in that files ending in the `.sql` extension (or `.sql.gz` or `.sql.xz`) will be executed to the database on container initialization.  Bash scripts (`.sh`) can also be placed in this directory to perform other initialization steps.

Let's verify the database's creation:

    $ sudo docker exec -ti my-database su postgres --command "psql my_db --command 'SELECT * FROM pg_database WHERE datistemplate = false;'"
    oid  | datname  | datdba | encoding | datcollate |  datctype  | datistemplate | datallowconn | datconnlimit | datlastsysoid | datfrozenxid | datminmxid | dattablespace | datacl   -------+----------+--------+----------+------------+------------+---------------+--------------+--------------+---------------+--------------+------------+---------------+--------
    13761 | postgres |     10 |        6 | en_US.utf8 | en_US.utf8 | f          | t            |           -1 |         13760 |          727 |          1 |          1663 |
    16384 | my_db    |     10 |        6 | en_US.utf8 | en_US.utf8 | f           | t            |           -1 |         13760 |          727 |          1 |          1663 |
    (2 rows)


## Debugging Techniques ##

Most containers are configured to make pertinent status information (such as their error log) visible through Docker's `logs` command:

    $ sudo docker logs my-apache2-container
    AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
    ...

Sometimes this isn't sufficient to diagnose a problem.  In the previous example we shelled into our container to experiment with, via:

    $ sudo docker exec -it my-apache2-container /bin/bash
    root@abcd12345678:/# cat /proc/cmdline 
    BOOT_IMAGE=/boot/vmlinuz-5.15.0-25-generic root=LABEL=cloudimg-rootfs ro console=tty1 console=ttyS0

This places you inside a bash shell inside the container; commands you issue will be executed within the scope of the container.  While tinkering around inside the container isn't suitable for normal production operations, it can be a handy way to debug problems such as if you need to examine logs or system settings.  For example, if you're trying to examine the network:

    root@abcd12345678:/# apt-get update && apt-get install -y iputils-ping iproute2
    root@abcd12345678:/# ip addr | grep inet
        inet 127.0.0.1/8 scope host lo
        inet 172.17.0.3/16 brd 172.17.255.255 scope global eth0

    root@abcd12345678:/# ping my-apache2-container
    ping: my-apache2-container: Name or service not known
    root@abcd12345678:/# ping -c1 172.17.0.1 | tail -n2
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.194/0.194/0.194/0.000 ms
    root@abcd12345678:/# ping -c1 172.17.0.2 | tail -n2
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.044/0.044/0.044/0.000 ms
    root@abcd12345678:/# ping -c1 172.17.0.3 | tail -n2
    1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

We won't use this container any further, so can remove it:

    $ sudo docker stop my-apache2-container
    $ sudo docker rm my-apache2-container


## Network ##

IP addresses may be suitable for debugging purposes, but as we move beyond individual containers we'll want to refer to them by network hostnames.  First we create the network itself:

    $ sudo docker network create my-network
    c1507bc90cfb6100fe0e696986eb99afe64985c7c4ea44ad319f8080e640616b

    $ sudo docker network list
    NETWORK ID     NAME         DRIVER    SCOPE
    7e9ce8e7c0fd   bridge       bridge    local
    6566772ff02f   host         host      local
    c1507bc90cfb   my-network   bridge    local
    8b992742eb38   none         null      local

Now when creating containers we can attach them to this network:

    $ sudo docker run -d --name my-container-0 --network my-network ubuntu/apache2:latest
    $ sudo docker run -d --name my-container-1 --network my-network ubuntu/apache2:latest

    $ sudo docker exec -it my-container-0 /bin/bash
    root@abcd12345678:/# apt-get update && apt-get install -y iputils-ping bind9-dnsutils 
    root@abcd12345678:/# ping my-container-1 -c 1| grep statistics -A1
    --- my-container-1 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms

    root@abcd12345678:/# dig +short my-container-0 my-container-1
    172.18.0.2
    172.18.0.3

    root@abcd12345678:/# exit

    $ sudo docker stop my-container-0 my-container-1
    $ sudo docker rm my-container-0 my-container-1

A common use case for networked containers is load balancing.  Docker's `--network-alias` option provides one means of setting up *round-robin* load balancing at the network level during container creation:

    $ sudo docker run -d --name my-container-0 --network my-network --network-alias my-website -e TZ=UTC -p 8080:80 -v ${HOME}/index.html:/var/www/html/index.html:ro ubuntu/apache2:latest
    $ sudo docker run -d --name my-container-1 --network my-network --network-alias my-website -e TZ=UTC -p 8081:80 -v ${HOME}/index.html:/var/www/html/index.html:ro ubuntu/apache2:latest
    $ sudo docker run -d --name my-container-2 --network my-network --network-alias my-website -e TZ=UTC -p 8082:80 -v ${HOME}/index.html:/var/www/html/index.html:ro ubuntu/apache2:latest

    $ sudo docker ps
    CONTAINER ID   IMAGE                   COMMAND                CREATED      STATUS      PORTS                                   NAMES
    665cf336ba9c   ubuntu/apache2:latest   "apache2-foreground"   4 days ago   Up 4 days   0.0.0.0:8082->80/tcp, :::8082->80/tcp   my-container-2
    fd952342b6f8   ubuntu/apache2:latest   "apache2-foreground"   4 days ago   Up 4 days   0.0.0.0:8081->80/tcp, :::8081->80/tcp   my-container-1
    0592e413e81d   ubuntu/apache2:latest   "apache2-foreground"   4 days ago   Up 4 days   0.0.0.0:8080->80/tcp, :::8080->80/tcp   my-container-0

The `my-website` alias selects a different container for each request it handles, allowing load to be distributed across all of them.

    $ sudo docker exec -it my-container-0 /bin/bash
    root@abcd12345678:/# apt update; apt install -y bind9-dnsutils
    root@abcd12345678:/# dig +short my-website
    172.18.0.3
    172.18.0.2
    172.18.0.4

Run that command several times, and the output should display in a different order each time.

    root@abcd12345678:/# dig +short my-website
    172.18.0.3
    172.18.0.4
    172.18.0.2
    root@abcd12345678:/# dig +short my-website
    172.18.0.2
    172.18.0.3
    172.18.0.4
    root@abcd12345678:/# exit

    $ sudo docker stop my-container-0 my-container-1  my-container-2
    $ sudo docker rm my-container-0 my-container-1  my-container-2


## Installing Software ##

By default Apache2 can serve static pages, but for more than that it's necessary to enable one or more of its modules.  As we mentioned above, there are three approaches you could take:  Set things up at runtime by logging into the container and running commands directly; configuring the container at creation time; or, customizing the image definition itself.

Ideally, we'd use the second approach to pass a parameter or setup.sh script to install software and run `a2enmod <mod>`, however the Apache2 image lacks the equivalent of Postgres' `/docker-entrypoint-initdb.d/` directory and automatic processing of shell scripts.  So for a production system you'd need to derive your own customized Apache2 image and build containers from that.

For the purposes of this tutorial, though, we can use the runtime configuration approach just for experimental purposes.

First, create our own config file that enables CGI support:

    $ cat > ~/my-apache2.conf << 'EOF'
    User ${APACHE_RUN_USER}
    Group ${APACHE_RUN_GROUP}
    ErrorLog ${APACHE_LOG_DIR}/error.log
    ServerName localhost
    HostnameLookups Off
    LogLevel warn
    Listen 80

    # Include module configuration:
    IncludeOptional mods-enabled/*.load
    IncludeOptional mods-enabled/*.conf

    <Directory />
            AllowOverride None
            Require all denied
    </Directory>

    <Directory /var/www/html/>
            AllowOverride None
            Require all granted
    </Directory>

    <Directory /var/www/cgi-bin/>
            AddHandler cgi-script .cgi
            AllowOverride None
            Options +ExecCGI -MultiViews
            Require all granted
    </Directory>

    <VirtualHost *:80>
            DocumentRoot /var/www/html/
            ScriptAlias /cgi-bin/ /var/www/cgi-bin/
    </VirtualHost>
    EOF


Next, copy the following into a file named `fortune.cgi`.

    $ cat > ~/fortune.cgi << 'EOF'
    #!/usr/bin/env bash
    echo -n -e "Content-Type: text/plain\n\n"
    echo "Hello ${REMOTE_ADDR}, I am $(hostname -f) at ${SERVER_ADDR}"
    echo "Today is $(date)"
    if [ -x /usr/games/fortune ]; then
        /usr/games/fortune
    fi
    EOF
    $ chmod a+x ~/fortune.cgi

Now create our container:

    $ sudo docker run -d --name my-fortune-cgi -e TZ=UTC -p 9080:80 \
         -v $(pwd)/my-apache2.conf:/etc/apache2/apache2.conf:ro \
         -v $(pwd)/fortune.cgi:/var/www/cgi-bin/fortune.cgi:ro \
         ubuntu/apache2:latest
    c3709dc03f24fbf862a8d9499a03015ef7ccb5e76fdea0dc4ac62a4c853597bf

Next, perform the runtime configuration steps:

    $ sudo docker exec -it my-fortune-cgi /bin/bash

    root@abcd12345678:/# apt-get update && apt-get install -y fortune
    root@abcd12345678:/# a2enmod cgid
    root@abcd12345678:/# service apache2 force-reload

Finally, restart the container so our changes take effect:

    $ sudo docker restart my-fortune-cgi
    my-fortune-cgi

Let's test it out:

    $ curl http://localhost:9080/cgi-bin/fortune.cgi
    Hello 172.17.0.1, I am 8ace48b71de7 at 172.17.0.2
    Today is Wed Jun  1 16:59:40 UTC 2022
    Q:	Why is Christmas just like a day at the office?
    A:	You do all of the work and the fat guy in the suit
            gets all the credit.

Finally is cleanup, if desired:

    $ sudo docker stop my-fortune-cgi
    $ sudo docker rm my-fortune-cgi


## Next ###

While it's interesting to be able to customize a basic container, how can we do this without resorting to runtime configuration?  As well, a single container by itself is not terrible useful, so in the [next section](https://discourse.ubuntu.com/t/rock-images-multi-node-configuration-with-docker-compose/28708) we'll practice setting up a database node to serve data to our webserver.
