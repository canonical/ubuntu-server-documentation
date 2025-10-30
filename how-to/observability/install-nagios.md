(install-nagios)=
# How to install and configure Nagios Core 4

The monitoring of essential servers and services is an important part of system administration. This guide walks through how to install and configure Nagios Core 4 for availability monitoring.

The example in this guide uses two servers, with hostnames `server01` and `server02`.

`server01` will be configured with Nagios to monitor services on itself and on `server02`, while `server02` will be configured to send data to `server01`.

Two users will be created: `nagiosadmin` with full administrative access, and user `nagiosuser` with viewing access only.

## Installation

### Install Nagios Core 4 on `server01`

On `server01`, install the `nagios4` package and NRPE plugin:

```none
sudo apt install nagios4 nagios-nrpe-plugin
```

The package will install Postfix by default. You will be prompted for mail server information. If you don't have a FQDN mail server or want to do the configuration at a later time, you can choose the "No configuration" option, from the Postfix Configuration dialog.
See {ref}`how to install and configure Postfix <install-postfix>`. It is also recommended that `server01` is set up with a fully qualified domain name (FQDN). Refer to the documentation on {ref}`how to install and configure DNS <install-dns>`. The NRPE plugin package will be used to collect data from `server02`.


### Create a user for accessing the Nagios web interface

After installing Nagios 4 on `server01`, create the `nagiosadmin` user:

```none
sudo htdigest -c /etc/nagios4/htdigest.users "Nagios4" nagiosadmin
```

Use the `-c` argument only when creating the user for the first time.

The `htdigest` tool is installed by default by Nagios 4 core package. "Nagios4" here is the realm argument provided in directive `AuthName` in the `/etc/nagios4/apache2.conf` file. More information on this will be provided later when we configure the Nagios server on `server01`. For more information on the `htdigest` tool see [Nagios CGI security documentation](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/cgisecurity.html).

Moving on to `server02`...


### Install `nagios-nrpe-server` on `server02`

Next, on `server02`, install the `nagios-nrpe-server` package:

```none
sudo apt install nagios-nrpe-server
```

NRPE allows you to execute local checks on remote hosts. There are other ways of accomplishing this through other Nagios plugins, as well as other checks.


## Configuring the Nagios server

Back on `server01`...

Before configuring the Nagios server it is important to understand the location of directories containing Nagios configuration and check files.

`/etc/nagios4`
: Contains configuration files for the operation of the Nagios daemon. Most of the maintenance of the Nagios server will be performed at this location. This directory contains user authentication file htdigest.users, custom configuration directory conf.d and objects directory.
`/etc/nagios-plugins/config`
: Contains configuration files for the service checks.
`/etc/nagios`
: On the remote host, contains the nagios-nrpe-server configuration files.

Apache files are located in the `/etc/apache2` directory.


### Enable authentication

As a first step in the configuration, on `server01`, to use digest
authentication, the `use_authentication` default setting must be changed. Edit
the `/etc/nagios4/cgi.cfg` file and change the directive ` use_authentication=0`
to ` use_authentication=1`.

Save the file and close.

### Apache configuration for Nagios

The Apache configuration for Nagios involves editing the default configuration
`apache2.conf` file provided in `/etc/nagios4`, and enabling the web interface
in Apache2. It is a good idea to create a copy of this file before working on
it, so you can have the original file saved for reference. You can achieve this
on `server01` by running:

```none
sudo cp /etc/nagios4/apache2.conf /etc/nagios4/apache2.conf.orig
```

On the next step, edit `/etc/nagios4/apache2.conf` to complete the digest
authentication configuration for the Nagios web interface. Edit the
`/etc/nagios4/apache2.conf` file, and change the following lines:

Comment out the "Require IP" directive (add a `#` in front of it):

```none
#Require ip ::1/128 fc00::/7 fe80::/10 10.0.0.0/8 169.254.0.0/16 172.16.0.0/12 192.168.0.0/16
```

This line was enabled by default, to only allow private IP addresses access.
If that is what you need, then leave it un-commented.

Inside the `<Files "cmd.cgi">` block, change or add the "Require all granted"
and "Require valid-user" directives. Comment out the "Require all granted"
directive and un-comment "Require valid-user". This directive forces user
authentication; which is necessary to issue commands, such as to silence
notifications:

```none
<Files "cmd.cgi">
   Options  ExecCGI
   AuthDigestDomain  "Nagios4"
   AuthDigestProvider  file
   AuthUserFile  "/etc/nagios4/htdigest.users"
   AuthGroupFile "/etc/group"
   AuthName  "Nagios4"
   AuthType  Digest
   #Require all  granted
   Require  valid-user
</Files>
```

### Forcing all users to authenticate

The next step will force ALL users to authenticate. Comment out the following
two lines:

```none
#<Files "cgi.cmd">
```

and its closing bracket:

```none
#</Files>
```

This has the effect of moving all directives that were inside the `<Files>`
block, to the `<DirectoryMatch>` block and therefore, enforcing all users to
authenticate against the matched directories paths expressed in the regex pattern.

The Apache configuration file for Nagios is now configured, so save close it.

```{note}
The Alias `/nagios4` in directive `Alias /nagios4 /usr/share/nagios4/htdocs` can
be changed to be anything you need. This is how you would reach the Nagios
interface from the browser. In this setup, you would enter into the browser: `server01/nagios4`.

For more information on the topic of authentication and authorization, see both
[Apache's documentation](https://httpd.apache.org/docs/2.2/howto/auth.html) and
[Nagios's documentation](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/cgisecurity.html). If you need granular access for users, use the `/etc/nagios4/cgi.cfg` file to
define the access the user is authorized for.
```

## Nagios web interface

At this point, the web interface is not yet working as intended.

Still working on `server01`, copy the `/etc/nagios4/apache2.conf` file to the
`/etc/apache2/sites-available` directory by running:

```none
sudo cp /etc/nagios4/apache2.conf /etc/apache2/sites-available/nagios4.conf
```

Then enable the configuration:

```none
sudo a2ensite nagios4.conf
```

Nagios web interface Apache site is now enabled. It is time to reload both
Apache2 and Nagios to apply configuration changes:

```none
sudo systemctl reload apache2
sudo systemctl reload nagios4
```

Check the status of Nagios and Apache2. Examine output for any errors:

```none
sudo systemctl status apache2
```

then run:

```none
sudo systemctl status nagios4
```

If both are active (running) and no errors are reported, then the web interface
can be tested.

For information on how to configure Apache2, refer to the
{ref}`how-to configure Apache2 <install-apache2>` page.


## Modifying the Nagios Apache site

At this point, the Nagios site can be tested. From a browser, type
`server01/nagios4` and press {kbd}`Enter`. Alternatively, if the hostname does
not resolve to DNS, enter the IP address: `172.10.100.1/nagios4`.

Replace the IP address with the IP address of your Nagios server. You will
be asked to authenticate, so log in as the user `nagiosadmin` that was created
earlier. You will notice that under "hosts", only the localhost is being
monitored. More on working with objects later.

To illustrate making modifications to the Nagios site, landing `server01/nagios4`
is going to be changed to `server01/nagios`.

On `server01`, edit file `/etc/nagios4/apache2.conf`, changing the line:

```none
Alias /nagios4 /usr/share/nagios4/htdocs
```

to:

```none
Alias /nagios /usr/share/nagios4/htdocs
```

Save the file and quit.

To activate this change, disable the `nagios4` site first:

```none
sudo a2dissite nagios4
```

Then copy the `/etc/nagios4/apache2.conf` file to the
`/etc/apache2/sites-available` directory:

```none
sudo cp /etc/nagios4/apache2.conf /etc/apache2/sites-available/nagios4.conf
```

Enable the configuration:

```none
sudo a2ensite nagios4.conf
```

And reload Apache2:

```none
sudo systemctl reload apache2
```

To test the change, enter `server01/nagios` into a browser.

You can directly edit the `/etc/apache2/sites-enabled/nagios4.conf` file and
then reload Apache2, without disabling the site first, but this makes it harder
to keep track of changes and restore to a working state if something goes wrong.
It is a good idea to always back up the file before making any changes, so you
can quickly restore from it.

## Working with Nagios users

So far, the only user with access to Nagios is `nagiosadmin`. In the next steps,
a `nagiosuser` will be created and configured to have viewing access to Nagios.
On `server01`, enter in the terminal:

```none
sudo htdigest -c /etc/nagios4/htdigest.users "Nagios4" nagiosuser
```

At this point, `nagiosuser` is created but no access has been defined. To define
access, edit file `/etc/nagios4/cgi.cfg` and change the following line:

```none
authorized_for_system_information=nagiosadmin
```

to:

```none
authorized_for_system_information=nagiosadmin, nagiosuser
```

To allow the user to view global hosts and services, define access by changing
these lines:

```none
authorized_for_all_services=nagiosadmin
authorized_for_hosts=nagiosadmin
```

to

```none
authorized_for_all_services=nagiosadmin, nagiosuser
authorized_for_all_hosts=nagiosadmin, nagiosuser
```

Save the file and quit, then reload the Nagios configuration:

```none
sudo systemctl reload nagios4
```

To test it, navigate in a browser to `server01/nagios` and login as
`nagiosuser`. Click on Hosts, Services links. You should be able to view both.
Then look for System, Configuration links. When trying to access the
Configuration, a "no permission to view information" message should be displayed.

```{note}
When using the `htdigest` utility, use the `-c` option only when first creating
a user. Omit the `-c` to change password afterwards. The `/etc/nagios4/cgi.cfg`
has many options. Review the file for usage.
```

## Working with resource objects

Objects are definitions files for each one of the resources available in Nagios.
Files are located in the `/etc/nagios4/objects` directory.

The Nagios 4 package installs the standard Nagios monitoring plugins.
These are located in directory `/usr/lib/nagios/plugins`. So far, the checks
defined for the localhost in file `/etc/nagios4/objects/localhost.cfg` make use
of these plugins. By default, Nagios is configured to check HTTP, disk space,
SSH, current users, processes, and load on the localhost; as well as ping check
the gateway.


### Creating host config file for `server02`

To create host config file for `server02`, on `server01`:

```none
sudo cp /etc/nagios4/objects/localhost.cfg /etc/nagios4/conf.d/server02.cfg
```

Then, edit file `/etc/nagios4/conf.d/server02.cfg`. Change the host definition.
Replace address with the IP address of `server02`. On existing definitions,
replace `host_name` with `server02`.

```none
define host {
      use              generic-host     ;Name of host template to use
      host_name        server02         ;This host definition will inherit all variables that are defined
      alias            server 02        ;in (or inherited by) the linux-server host template definition.
      address          172.10.100.2
}
```

Also, add a DNS check service definition by adding these lines:

```none
# Define a DNS check service on server02
define service {
      use                    local-service
      host_name              server02
      service_description    DNS
      check_command          check_dns
      notification_enabled   0
}

```

Save the file and exit.

When copying resource files to use as templates, be aware that this can create
duplicate definitions. When you run a pre-flight check described in next section,
errors and warnings will be reported. To avoid this, comment out the duplicate
definitions.

Before restarting the Nagios server, test the configuration.

## Testing the Nagios configuration and troubleshooting

When you make changes to the Nagios configuration, you can test the
configuration before it is enabled. In this way you can make the necessary
changes, in case of errors, before restarting the Nagios server.

Still on `server01`, enter into the terminal:

```none
sudo nagios4 -v /etc/nagios4/nagios.cfg
```

If no errors are found, restart the Nagios server:

```none
sudo systemctl restart nagios4
```

### Hostgroup definitions

Now create a hostgroup definition, which is used to group one or more hosts
together for easier configuration. In this step you will create a service
definition for the MySQL check and a MySQL hostgroup definition. To install the
MySQL server, run:

```none
sudo apt install mysql-server
```

For the purpose of this guide, MySQL server has been installed on server02.

```{seealso}
* {ref}`install-mysql`
* [MYSQL tutorial by tutorials24x7.com](https://www.tutorials24x7.com/mysql/how-to-install-mysql-8-on-ubuntu-2004-lts)
* [MySQL official documentation](https://www.mysql.com)
```

Next, add a service definition for the MySQL check and the hostgroup `mysql-servers` definition.
The service definition is added to the file `/etc/nagios4/conf.d/services_nagios2.cfg`:

```none
#check MySQL servers
define service {
             hostgroup_name            mysql-servers
             service_description       MySQL
             check_command             check_mysql_cmdlinecred!nagios!secret!$HOSTADRESS
             use                       generic-service
             notification_interval     0; set > 0 to be re-notified
}
```

Add the `mysql-servers` definition by editing `/etc/nagios4/conf.d/hostgroups_nagios2.cfg`:

```none
#MySQL group definition
define hostgroup {
             hostgroup_name      mysql-servers
             alias               MySQL  servers
             members             localhost, server02
}
```

### Nagios user authentication to MySQL

The Nagios check needs to authenticate to MySQL. Add a Nagios user to MySQL on
`server02`:

```none
mysql -u root -p -e "create user nagios identified by 'secret';"
```

Alternatively, you can log into MySQL and create the Nagios user. Replace
'secret' with a password.

```none
sudo mysql -u root -p
mysql> CREATE USER 'nagios' IDENTIFIED BY 'secret';
mysql> flush privileges;
mysql> exit
```

```{note}
The Nagios user will need to be added to all hosts in the `mysql-servers` hostgroup.
```

Restart Nagios to start checking the MySQL servers. On `server01` run:

```none
sudo systemctl restart nagios4
```

## NRPE configuration

As a last step, configure NRPE to check disk space on `server02`.

On `server01`, add the service check to `/etc/nagios4/conf.d/server02.cfg`:

```none
#NRPE disk check
define service {
             use                  generic-service
             host_name            server02
             server_description   nrpe-disk-check
             check_command        check_nrpe_1arg!check_all_disks!172.10.100.2
}
```

On `server02`, edit `/etc/nagios/nrpe.cfg`, changing:

```none
allowed_hosts=172.10.100.1
```

Below, in the command definition area, add:

```none
command[check_all_disks]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -e
```

While on `server02`, restart `nagios-nrpe-server`:

```none
sudo systemctl restart nagios-nrpe-server.service
```

Finally, on `server01` restart Nagios:

```none
sudo systemctl restart nagios4
```

## Further reading

This guide is meant to serve as a stepping stone into Nagios Core 4.

There are many more Nagios features and uses not covered here. There are many
resources and tutorials available online. Some are listed below. This guide made
use of previous installation instructions for Nagios 3:

* For more information about Nagios and its features, visit the [Nagios website](https://www.nagios.com).
* Also the [Nagios Core Documentation](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/whatsnew.html) and [Nagios Core 4 Documentation](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/).
* Nagios website also offers a [list of books](https://www.nagios.org/about/propaganda/books-2/) related to Nagios, its administration and monitoring.
