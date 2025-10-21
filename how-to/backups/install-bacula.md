(install-bacula)=
# How to install and configure Bacula

[Bacula](http://www.bacula.org/) is a backup management tool that enables you to backup, restore, and verify data across your network. There are Bacula clients for Linux, Windows, and Mac OS X -- making it a cross-platform and network-wide solution.

## Bacula components

Bacula is made up of several components and services that are used to manage backup files and locations:

- **Bacula Director**: A service that controls all backup, restore, verify, and archive operations.

- **Bacula Console**: An application that allows communication with the Director. There are three versions of the Console:
  
  - Text-based command line.
    
  - Qt GUI interface.

- **Bacula File**: This application is installed on machines to be backed up, and is responsible for handling data requested by the Director.

- **Bacula Storage**: The program that performs the storage of data onto, and recovery of data from, the physical media.

- **Bacula Catalog**: Responsible for maintaining the file indices and volume databases for all backed-up files. This enables rapid location and restoration of archived files. The Catalog supports three different databases: MySQL, PostgreSQL, and SQLite.

- **Bacula Monitor**: This is a graphical tray monitor for the Bacula backup system.

These services and applications can be run on multiple servers and clients, or they can be installed on one machine if backing up a single disk or volume.

In this documentation, we will deploy a Bacula Director, with a backup job for the Director itself, and also install the Bacule File service on a workstation, to remotely backup its data.


TBD

IMAGE

## Installing the Server Components

The Bacula components can be installed on multiple systems, or they can be grouped together where it makes sense. A fully distributed installation might be appealing and is more scalable, but is also harder to configure. Here we will pick something in between:

 * A Bacula "server", where we will install the following Bacula components: Director, Catalog with an SQL database, Storage, File, Console. The server itself should also be backed up, hence why components typically installed on clients are also installed here.
 * A Bacula "client", which is just a system to be backed up. It will have only the File component installed. Any system that needs to be backed up will have to have the File component installed.

To begin with, we have to start with installing the database that will be used by the Catalog. The choices are:

 * sqlite: Should only be used for test or development deployments of Bacula.
 * PostgreSQL
 * MySQL

Either SQL database is suitable. For this document, we will use PostgreSQL:

```bash
sudo apt install postgresql
```
```{note}
The default choices for PostgreSQL are fine for most cases, but please take a look at {ref}`MySQL databases <install-mysql>` and {ref}`PostgreSQL databases <install-postgresql>` for more details on these powerful databases.
```

Next we can install Bacula. The `bacula` package has the necessary dependencies and will pull in what is needed for our deployment scenario:

```bash
sudo apt install bacula
```
During the install process you will be asked to supply a password for the *database owner* of the *bacula database*. If left blank, a random password will be used.

## Configuring the Server

Several components were installed on this system by the `bacula` package. Each one has its own configuration file:

 * Director: `/etc/bacula/bacula-dir.conf`
 * Storage: `/etc/bacula/bacula-sd.conf`
 * File: `/etc/bacula/bacula-fd.conf`
 * Console: `/etc/bacula/bconsole.conf`

All these components need to eventually talk to each other, and the authentication is performed via passwords that were automatically generated at install time. These passwords are stored in the `/etc/bacula/common_default_passwords` file. If a new component is installed on this system, it can benefit from this file to automatically be ready to authenticate itself, but in general, after everything is installed and configured, this file isn't needed anymore.

### Director

The Bacula Director is the central component of the system. This is where we:

 * Register the clients;
 * Define the schedules;
 * Define the file sets to be backed up;
 * Define storage pools;
 * Define the backup jobs;

Bacula configuration files are formatted based on **resources** composed of **directives** surrounded by curly “{}” braces. Each Bacula component has an individual file in the `/etc/bacula` directory.

The default installation of the Director create a configuration file in `/etc/bacula/bacula-dir.conf` with some choices and examples. That is a good reference, but it does not apply to all cases. Since we are going to modify that file a lot, it's best to make a backup copy first:

```
sudo cp -af /etc/bacula/bacula-dir.conf /etc/bacula/bacula-dir.conf.bak
```
Now edit `/etc/bacula/bacula-dir.conf` and make the following changes/additions:

a) The `Director` resource

This block defines the attributes of the Director service:
```
Director {
  Name = bacula-server-dir
  DIRport = 9101
  QueryFile = "/etc/bacula/scripts/query.sql"
  WorkingDirectory = "/var/lib/bacula"
  PidDirectory = "/run/bacula"
  Maximum Concurrent Jobs = 20
  Password = "P68sjhhjPTf4FmZsUNOUpQPj8MwV86OA7"
  Messages = Daemon
  #DirAddress = 127.0.0.1
}
```
What you should inspect and change:
 * `Name`: it's common to use the format `$hostname-dir` for the director. For example, if the hostname is "`bacula-server`", the name here would be `bacula-server-dir`.
 * `DirAddress`: by default this is set to the localhost address. In order to be able to perform remote backups, thouch, the director needs to be accessible on the network. To do that, simply remove or comment this parameter: in that case, the service will listen on all network interfaces available on the system.
 * `Password`: a random password will have been created for this installation, so it doesn't need to be changed, unless you would rather pick a different one.

```{tip}
For more details about all the options of the `Director` resource, please check the upstream [Director Resource](https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html#SECTION0023200000000000000000) documentation.
```

b) The `FileSet` resource

Let's define what we want to backup. There will likely be multiple file sets defined in a production server, but as an example, here we will define a set for backing up the home directory:
```
FileSet {
  Name = "Home"
  Include {
    Options {
      signature = SHA256
      aclsupport = yes
      xattrsupport = yes
    }
    Options {
        wilddir = "/home/*/Downloads"
        wildfile = "*.iso"
        exclude = yes
    }
    File = /home
  }
} 
```
This example illustrates some interesting points, and shows the type of flexibility he have in defining File Sets:
 * `Name`: This defines the name of this file set, and will be referenced by other configuration blocks.
 * *Include Options*: the `Options` block can be used several times inside the `Include` block. Here we define that we want to include POSIX ACLs support, and extended attributes, and use the SHA256 hash algorithm, but perhaps more interesting is how we select which files to exclude from the set:
   * `wilddir`, `wildfile`: these parameters specify globbing expressions of directories and files to exclude from the set (because we also set `exclude = yes`). In this example, we are excluding potentially large files. Unfortunately there is no direct way to exclude files from a set based on their size, so we have to make some educated guesses using standard file extensions and directory locations.
 * `File`: This parameter can be specified multiple times, and it's additive. In this example we have it only used once, to select the `/home` directory and its subdirectories, subject to the exclusions defined in the `Options` block.

```{tip}
For more details about all the options of the `FileSet` resource, please check the upstream [FileSet Resource](https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html#SECTION0023700000000000000000) documentation.
```

c) The `Client` resource
The default installation will have defined a `Client` resource. It should be similar to the following:
```
# Client (File Services) to backup
Client {
  Name = bacula-server-fd
  Address = bacula-server.lxd  # use the real hostname instead of "localhost"
  FDPort = 9102
  Catalog = MyCatalog
  Password = "R_MqfSOpsIWYx0PAwMSHEFzCHF9OkcmFI"
  File Retention = 60 days
  Job Retention = 6 months
  AutoPrune = yes
}
```
Of note in this definition we have:
 * `Name`: As with other similar resources, the default name uses the format `$hostname-fd` (where `fd` stands for *File Daemon*).
 * `Address`: The default will be `localhost`, but we should be in the habit of using a real hostname, because in a more distributed installation, these hostnames will be sent to other services in other machines, and "localhost" will then be incorrect.
 * `Password`: The password was automatically generated, and should be kept as is unless you want to use another one.
 * `File Retention`, `Job Retention`: these should be adjusted according to your particular needs for each client.
By default, the backup job named `BackupClient1` is configured to archive the Bacula Catalog. If you plan on using the server to back up more than one client you should change the name of this job to something more descriptive. To change the name, edit `/etc/bacula/bacula-dir.conf`:
 * `AutoPrune`: This setting makes Bacula automatically apply the retention parameters at the end of a backup job. It is enabled by default.

```{tip}
For more details about all the options of the `Client` resource, please check the upstream [Client Resource](https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html#SECTION00231300000000000000000) documentation.
```


```text
#
# Define the main nightly save backup job
#   By default, this job will back up to disk in 
Job {
  Name = "BackupServer"
  JobDefs = "DefaultJob"
  Write Bootstrap = "/var/lib/bacula/Client1.bsr"
}
```

```{note}
The example above changes the job name to "BackupServer", matching the machine's host name. Replace “BackupServer” with your own {term}`hostname`, or other descriptive name.
```

The Console can be used to query the Director about jobs, but to use the Console with a *non-root* user, the user needs to be in the **Bacula group**. To add a user to the Bacula group, run the following command from a terminal:

```bash
sudo adduser $username bacula
```

```{note}
Replace `$username` with the actual username. Also, if you are adding the current user to the group you should log out and back in for the new permissions to take effect.
```

## Localhost backup

This section shows how to back up specific directories on a single host to a local tape drive.

- First, the Storage device needs to be configured. Edit `/etc/bacula/bacula-sd.conf` and add:
  ```text
  Device {
    Name = "Tape Drive"
    Device Type = tape
    Media Type = DDS-4
    Archive Device = /dev/st0
    Hardware end of medium = No;
    AutomaticMount = yes;               # when device opened, read it
    AlwaysOpen = Yes;
    RemovableMedia = yes;
    RandomAccess = no;
    Alert Command = "sh -c 'tapeinfo -f %c | grep TapeAlert'"
  }
  ```
  The example is for a DDS-4 tape drive. Adjust the "Media Type" and "Archive Device" to match your hardware. Alternatively, you could also uncomment one of the other examples in the file.

- After editing `/etc/bacula/bacula-sd.conf`, the Storage daemon will need to be restarted:
   ```bash 
   sudo systemctl restart bacula-sd.service
   ```

- Now add a Storage resource in `/etc/bacula/bacula-dir.conf` to use the new Device:
  ```text
  # Definition of "Tape Drive" storage device
  Storage {
    Name = TapeDrive
    # Do not use "localhost" here
    Address = backupserver               # N.B. Use a fully qualified name here
    SDPort = 9103
    Password = "Cv70F6pf1t6pBopT4vQOnigDrR0v3LT3Cgkiyjc"
    Device = "Tape Drive"
    Media Type = tape
  }
  ```
  Note:
  * The **Address** directive needs to be the Fully Qualified Domain Name (FQDN) of the server.
  * Change `backupserver` to the actual host name.
  * Make sure the **Password** directive matches the password string in `/etc/bacula/bacula-sd.conf`.

- Create a new **{term}`FileSet`** -- this will define which directories to backup -- by adding:
  ```text
  # LocalhostBacup FileSet.
  FileSet {
    Name = "LocalhostFiles"
    Include {
      Options {
        signature = MD5
        compression=GZIP
      }
      File = /etc
      File = /home
    }
  }
  ```
  This FileSet will backup the `/etc` and `/home` directories. The **Options** resource directives configure the FileSet to create an MD5 signature for each file backed up, and to compress the files using {term}`GZIP`.

- Next, create a new **Schedule** for the backup job:
  ```text
  # LocalhostBackup Schedule -- Daily.
  Schedule {
    Name = "LocalhostDaily"
    Run = Full daily at 00:01
  }
  ```
  The job will run every day at 00:01 or 12:01 am. There are many other scheduling options available.

- Finally, create the **Job**:
  ```bash
  # Localhost backup.
  Job {
    Name = "LocalhostBackup"
    JobDefs = "DefaultJob"
    Enabled = yes
    Level = Full
    FileSet = "LocalhostFiles"
    Schedule = "LocalhostDaily"
    Storage = TapeDrive
    Write Bootstrap = "/var/lib/bacula/LocalhostBackup.bsr"
  }
  ```
  The Job will do a **Full** backup every day to the tape drive.

- Each tape used will need to have a **Label**. If the current tape does not have a Label, Bacula will send an email letting you know. To label a tape using the Console enter the following command from a terminal:

  ```bash
  bconsole
  ```

- At the Bacula Console prompt enter:
  ```bash
  label
  ```

- You will then be prompted for the Storage resource:
  ```text
  Automatically selected Catalog: MyCatalog
  Using Catalog "MyCatalog"
  The defined Storage resources are:
       1: File
       2: TapeDrive
  Select Storage resource (1-2):2
  ```

- Enter the new **Volume** name:
  ```text 
  Enter new Volume name: Sunday
  Defined Pools:
       1: Default
       2: Scratch
  ```
  Replace "Sunday" with the desired label.

- Now, select the **Pool**:
  ```text 
  Select the Pool (1-2): 1
  Connecting to Storage daemon TapeDrive at backupserver:9103 ...
  Sending label command for Volume "Sunday" Slot 0 ...
  ```

Congratulations, you have now configured Bacula to backup the `localhost` to an attached tape drive.

### File

### Storage

Bacula has support for many different storage devices, notable tape drives, and the default configuration has many examples. Here we will configure a path for the Storage component to use for backups and restores, and it is assumed that this path is a mount point for some external storage device.


## Adding a client

On the client

sudo apt install bacula-fd

Director {
  Name = bacula-dir ## same as Director's Name on the Director server
  Password = "ue2FpvuVaztKON1nibj-tfYUTXUFzp5gT" # same as the Client resource for this system on the Director server
  Address = bacula-dir.lxd # IP/hostname of the Director server. Only needed if ConnectToDirector is used
}

FileDaemon {
  Name = workstation-fd
  FDport = 9102                  # where we listen for the director
  WorkingDirectory = /var/lib/bacula
  Pid Directory = /run/bacula
  Maximum Concurrent Jobs = 20
  Plugin Directory = /usr/lib/bacula
  #FDAddress = 127.0.0.1 # don't set: default is to listen on all addresses
}


On the director:

Add client instance to director:
Client {
    Name = workstation-fd
    Address = workstation.lxd
    FDPort = 9102
    Catalog = MyCatalog
    Password = "ue2FpvuVaztKON1nibj-tfYUTXUFzp5gT" # password from bacula-fd.conf on the new client
    File Retention = 60 days
    Job Retention = 6 months
    AutoPrune = yes
}

New job on the director:

Job {
    Name = "BackupWorkstation"
    JobDefs = "DefaultJob"
    Client = workstation-fd
}


console commands
list clients


## Further reading

* For more Bacula configuration options, refer to the [Bacula documentation](https://www.bacula.org/documentation/documentation/).

* The [Bacula home page](http://www.bacula.org/) contains the latest Bacula news and developments.

* Also, see the [Bacula Ubuntu Wiki](https://help.ubuntu.com/community/Bacula) page.



Useful commands:
- list jobloj jobid=<N>
- list jobs
- list volumes
- run job=<name> yes


Restoring
restore
5 (Select the most recent backup for a client)
defined client: : workstation-fd
navigate to path
type "mark <file>"
done
Use "mod" to change restore: you can restore in another client, another path, etc

job status codes: https://www.bacula.org/15.0.x-manuals/en/main/Job_status_Error_codes.html#blb:director:job:status


Be mindful of 127.0.0.1!!! Better to avoid it!!!
