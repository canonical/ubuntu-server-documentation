(install-mysql)=
# Install and configure a MySQL server

[MySQL](https://www.mysql.com/) is a fast, multi-threaded, multi-user, and robust SQL database server. It is intended for mission-critical, heavy-load production systems and mass-deployed software.

## Install MySQL

To install MySQL, run the following command from a terminal prompt:

```bash
sudo apt install mysql-server
```

Once the installation is complete, the MySQL server should be started automatically. You can quickly check its current status via systemd:

```bash
sudo service mysql status
```

Which should provide an output like the following:

```text
● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2019-10-08 14:37:38 PDT; 2 weeks 5 days ago
 Main PID: 2028 (mysqld)
    Tasks: 28 (limit: 4915)
   CGroup: /system.slice/mysql.service
           └─2028 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid
 Oct 08 14:37:36 db.example.org systemd[1]: Starting MySQL Community Server...
Oct 08 14:37:38 db.example.org systemd[1]: Started MySQL Community Server.
```

The network status of the MySQL service can also be checked by running the `ss` command at the terminal prompt:

```bash
sudo ss -tap | grep mysql
```

When you run this command, you should see something similar to the following:

```text
LISTEN    0         151              127.0.0.1:mysql             0.0.0.0:*       users:(("mysqld",pid=149190,fd=29))
LISTEN    0         70                       *:33060                   *:*       users:(("mysqld",pid=149190,fd=32))
```

If the server is not running correctly, you can type the following command to start it:

```bash
sudo service mysql restart
```

A good starting point for troubleshooting problems is the systemd journal, which can be accessed from the terminal prompt with this command:

```bash
sudo journalctl -u mysql
```

## Configure MySQL

You can edit the files in `/etc/mysql/` to configure the basic settings -- log file, port number, etc. For example, to configure MySQL to listen for connections from network hosts, in the file `/etc/mysql/mysql.conf.d/mysqld.cnf`, change the `bind-address` directive to the server's IP address:

```mysql
bind-address            = 192.168.0.5
```

```{note}
Replace `192.168.0.5` with the appropriate address, which can be determined via the `ip address show` command.
```

After making a configuration change, the MySQL daemon will need to be restarted with the following command:

```bash
sudo systemctl restart mysql.service
```

## User setup

By default, `mysql-server` initially provides a `'root'@'localhost'` user for managing the server locally. You can enter the MySQL command-line as this user by running:

```none
sudo mysql -u root
```

No password is required by MySQL as it authenticates with [auth_socket](https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.0/en/secure-deployment-configure-authentication.html).

### Create a new user

From the command-line, you can create additional MySQL users with different privileges using the `CREATE USER` command. For authentication, the two main options are to use a password or use a socket like the root user.

To create a user authenticated with a password, you can use MySQL's provided `caching_sha2_password` plugin. It can be invoked in the following way, providing the password in plaintext:

```none
CREATE USER 'username'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'password';
```

A random password can also be generated here with:

```none
CREATE USER 'username'@'localhost' IDENTIFIED WITH caching_sha2_password BY RANDOM PASSWORD;
```

[MySQL's upstream documentation](https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.0/en/secure-deployment-user-accounts.html) provides an overview of additional options when creating accounts with passwords.

Socket-based authentication is used to allow a local system user to access an account without entering a password. Invoke this with:

```none
CREATE USER 'username'@'localhost' IDENTIFIED WITH auth_socket;
```

By default, only the system user with the matching username can access this account. If you want the MySQL account username to differ from the system user username, then use the `AS` option:

```none
CREATE USER 'username'@'localhost' IDENTIFIED WITH auth_socket AS 'system-user-username';
```

### Adding user permissions

A newly created user will require privilege updates to interact with databases in any way. These are provided by the `GRANT` command alongside specified roles or operations. For example, to give your user the ability to view table entries using the `SELECT` operation on all databases, run the following:

```none
GRANT SELECT on *.* TO 'username'@'localhost';
```

## Database engines

Whilst the default configuration of MySQL provided by the Ubuntu packages is perfectly functional and performs well there are things you may wish to consider before you proceed.

MySQL is designed to allow data to be stored in different ways. These methods are referred to as either database or storage engines. There are two main storage engines that you'll be interested in: [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) and [MyISAM](https://dev.mysql.com/doc/refman/8.0/en/myisam-storage-engine.html). Storage engines are transparent to the end user. MySQL will handle things differently under the surface, but regardless of which storage engine is in use, you will interact with the database in the same way.

Each engine has its own advantages and disadvantages.

While it is possible (and may be advantageous) to mix and match database engines on a table level, doing so reduces the effectiveness of the performance tuning you can do as you'll be splitting the resources between two engines instead of dedicating them to one.

### InnoDB

As of MySQL 5.5, InnoDB is the default engine, and is highly recommended over MyISAM unless you have specific needs for features unique to that engine.

InnoDB is a more modern database engine, designed to be [ACID compliant](http://en.wikipedia.org/wiki/ACID) which guarantees database transactions are processed reliably. To meet ACID compliance all transactions are journaled independently of the main tables. This allows for much more reliable data recovery as data consistency can be checked.

Write locking can occur on a row-level basis within a table. That means multiple updates can occur on a single table simultaneously. Data caching is also handled in memory within the database engine, allowing caching on a more efficient row-level basis rather than file block.

### MyISAM

MyISAM is the older of the two. It can be faster than InnoDB under certain circumstances and favours a read-only workload. Some web applications have been tuned around MyISAM (though that's not to imply that they will be slower under InnoDB).

MyISAM also supports the {term}`FULLTEXT` index type, which allows very fast searches of large quantities of text data. However MyISAM is only capable of locking an entire table for writing. This means only one process can update a table at a time. As any application that uses the table scales this may prove to be a hindrance.

It also lacks journaling, which makes it harder for data to be recovered after a crash. The following link provides some points for consideration about using [MyISAM on a production database](http://www.mysqlperformanceblog.com/2006/06/17/using-myisam-in-production/).

## Backups

MySQL databases should be backed up regularly. Backups can be accomplished through several methods, of which we'll discuss three here.

[mysqldump](#mysqldump) is included with `mysql-server`. It is useful for backing up smaller databases, allows backups to be edited prior to a restore, and can be used for exporting to CSV and XML.

[MySQL Shell's Dump Utility](#mysql-shell-dump-utility) allows for backups of specific schema and tables, both to local files and remote secure servers. It is recommended for creating partial backups, and for integration with Python programs.

[Percona Xtrabackup](#percona-xtrabackup) creates full backups with far greater performance than the former options. However, it lacks the ability to customize schema and tables. It is the recommended option for backing up large databases in a production environment.

### mysqldump

`mysqldump` is a built-in tool that performs [logical backups](https://dev.mysql.com/doc/refman/8.4/en/glossary.html#glos_logical_backup) for MySQL.

To dump the data of a publicly available database on the local MySQL server into a file, run the following:

```bash
mysqldump [database name] > dump.sql
```

For restricted databases, specify a user with the proper permissions using `-u`:

```bash
mysqldump -u root [database name] > dump.sql
```

To restore a database from the backup file, run the `mysql` command and pipe the file through stdin:

```bash
mysql -u root [database name] < dump.sql
```

See the [upstream documentation](https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html) for more information.

### MySQL Shell Dump Utility

MySQL Shell, supported in Ubuntu 24.04 LTS and later, contains a set of utilities for dumping, backing up, and restoring MySQL data. It provides a programmatic option for logical backups with filtering options.

To install MySQL Shell, run the following:

```bash
sudo apt install mysql-shell
```

Run the following to connect to the local MySQL server on Ubuntu with MySQL Shell in Python mode:

```bash
mysqlsh --socket=/var/run/mysqld/mysqld.sock --no-password --python
```

Initiate a local backup of all data in Python mode with:
```python
util.dump_instance("/tmp/worlddump")
```

Dump a specific set of tables with `dump_tables`:

```python
util.dump_tables("database name", ["table 1", "table 2"], "/tmp/tabledump")
```

To restore dumped data, use the [dump loading utility](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-load-dump.html).

```python
util.load_dump("/tmp/worlddump")
```

```{note}
To restore data from a local file, `local_infile` needs to be enabled on the MySQL server. Activate this by accessing the server with the `mysql` command and entering `SET GLOBAL local_infile=1;`.
```

See the [MySQL Shell dump documentation](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.html) for more information.

### Percona Xtrabackup

Also supported in Ubuntu 24.04 LTS and later, Percona Xtrabackup is a tool for creating [physical backups](https://dev.mysql.com/doc/refman/8.4/en/glossary.html#glos_physical_backup). It is similar to the commercial offering of [MySQL Enterprise Backup](https://www.mysql.com/products/enterprise/backup.html).

To install Xtrabackup, run the following command from a terminal prompt:

```bash
sudo apt install percona-xtrabackup
```

Create a new backup with the `xtrabackup` command. This can be done while the server is running.

```bash
xtrabackup --backup --target-dir=/tmp/worlddump
```

To restore from a backup, service will need to be interrupted. This can be achieved with the following:

```bash
sudo systemctl stop mysql
xtrabackup --prepare --target-dir=/tmp/worlddump
sudo rm -rf /var/lib/mysql
sudo xtrabackup --copy-back --target-dir=/tmp/worlddump --datadir=/var/lib/mysql
sudo chown -R mysql:mysql /var/lib/mysql
sudo systemctl start mysql
```

For more information, see [Percona's upstream documentation](https://docs.percona.com/percona-xtrabackup/8.0/).

## Advanced configuration

### Creating a tuned configuration

There are a number of parameters that can be adjusted within MySQL's configuration files. This will allow you to improve the server's performance over time.

Many parameters can be adjusted with the existing database, however some may affect the data layout and thus need more care to apply.

First, if you have existing data, you will first need to carry out a `mysqldump` and reload:

```bash
mysqldump --all-databases --routines -u root -p > ~/fulldump.sql
```

This will then prompt you for the root password before creating a copy of the data. It is advisable to make sure there are no other users or processes using the database while this takes place. Depending on how much data you've got in your database, this may take a while. You won't see anything on the screen during the process.

Once the dump has been completed, shut down MySQL:

```bash
sudo service mysql stop
```

It's also a good idea to backup the original configuration:

```bash
sudo rsync -avz /etc/mysql /root/mysql-backup
```

Next, make any desired configuration changes. Then, delete and re-initialise the database space and make sure ownership is correct before restarting MySQL:

```bash
sudo rm -rf /var/lib/mysql/*
sudo mysqld --initialize
sudo chown -R mysql: /var/lib/mysql
sudo service mysql start
```

The final step is re-importation of your data by piping your SQL commands to the database.

```bash
cat ~/fulldump.sql | mysql
```

For large data imports, the 'Pipe Viewer' utility can be useful to track import progress. Ignore any ETA times produced by `pv`; they're based on the average time taken to handle each row of the file, but the speed of inserting can vary wildly from row to row with `mysqldumps`:

```bash
sudo apt install pv
pv ~/fulldump.sql | mysql
```

Once this step is complete, you are good to go\!

```{note}
This is not necessary for all `my.cnf` changes. Most of the variables you can change to improve performance are adjustable even whilst the server is running. As with anything, make sure to have a good backup copy of your config files and data before making changes.
```

### MySQL Tuner

[MySQL Tuner](https://github.com/major/MySQLTuner-perl) is a Perl script that connects to a running MySQL instance and offers configuration suggestions for optimising the database for your workload. The longer the server has been running, the better the advice `mysqltuner` can provide. In a production environment, consider waiting for at least 24 hours before running the tool. You can install `mysqltuner` with the following command:

```bash
sudo apt install mysqltuner
```

Then once it has been installed, simply run: `mysqltuner` -- and wait for its final report. 

The top section provides general information about the database server, and the bottom section provides tuning suggestions to alter in your `my.cnf`. Most of these can be altered live on the server without restarting; look through the [official MySQL documentation](https://dev.mysql.com/doc/) for the relevant variables to change in production.

The following example is part of a report from a production database showing potential benefits from increasing the query cache:

```text
-------- Recommendations -----------------------------------------------------
General recommendations:
    Run OPTIMIZE TABLE to defragment tables for better performance
    Increase table_cache gradually to avoid file descriptor limits
Variables to adjust:
    key_buffer_size (> 1.4G)
    query_cache_size (> 32M)
    table_cache (> 64)
    innodb_buffer_pool_size (>= 22G)
```

Obviously, performance optimisation strategies vary from application to application; what works best for WordPress might not be the best for Drupal or Joomla. Performance can depend on the types of queries, use of indexes, how efficient the database design is and so on.

You may find it useful to spend some time searching for database tuning tips based on the applications you're using. Once you've reached the point of diminishing returns from database configuration adjustments, look to the application itself for improvements, or invest in more powerful hardware and/or scale up the database environment.

## Further reading

- Full documentation is available in both online and offline formats from the [MySQL Developers portal](http://dev.mysql.com/doc/)

- For general SQL information see the O'Reilly books [Getting Started with SQL: A Hands-On Approach for Beginners](http://shop.oreilly.com/product/0636920044994.do) by Thomas Nield as an entry point and [SQL in a Nutshell](http://shop.oreilly.com/product/9780596518851.do) as a quick reference.
