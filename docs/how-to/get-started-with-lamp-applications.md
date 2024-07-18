(get-started-with-lamp-applications)=
# Get started with LAMP applications

## Overview

LAMP installations (Linux + Apache + MySQL + PHP/Perl/Python) are a popular setup for Ubuntu servers. There are a plethora of Open Source applications written using the LAMP application stack. Some popular LAMP applications include **wikis**, **management software** such as phpMyAdmin, and  **Content Management Systems (CMSs)** like WordPress.

One advantage of LAMP is the substantial flexibility for different database, web server, and scripting languages. Popular substitutes for MySQL include PostgreSQL and SQLite. Python, Perl, and Ruby are also frequently used instead of PHP. While Nginx, Cherokee and Lighttpd can replace Apache.

## Quickstart

The fastest way to get started is to install LAMP using `tasksel`. Tasksel is a Debian/Ubuntu tool that installs multiple related packages as a co-ordinated "task" onto your system.

At a terminal prompt enter the following commands:

```bash
sudo apt-get update
sudo apt-get install -y tasksel
sudo tasksel install lamp-server
```

### LAMP application install process

After installing LAMP you'll be able to install most LAMP applications in this way:

- Download an archive containing the application source files.

- Unpack the archive, usually in a directory accessible to a web server.

- Depending on where the source was extracted, configure a web server to serve the files.

- Configure the application to connect to the database.

- Run a script, or browse to a page of the application, to install the database needed by the application.

- Once the steps above, or similar steps, are completed you are ready to begin using the application.

A disadvantage of using this approach is that the application files are not placed in the file system in a standard way, which can cause confusion as to where the application is installed.

### Update LAMP applications

When a new LAMP application version is released, follow the same installation process to apply updates to the application.

Fortunately, a number of LAMP applications are already packaged for Ubuntu, and are available for installation in the same way as non-LAMP applications (some applications may need extra configuration and setup steps). Two popular examples are phpMyAdmin and WordPress.

Refer to our guides on how to [install phpMyAdmin](how-to-install-and-configure-phpmyadmin.md) and how to [install WordPress](how-to-install-and-configure-wordpress.md) for more information on those applications.
