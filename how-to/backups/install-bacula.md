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
Please take a look at {ref}`MySQL databases <install-mysql>` and {ref}`PostgreSQL databases <install-postgresql>` for more details on these powerful databases.
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

The default installation of the several bacula components will create configuration files in `/etc/bacula/` with some choices and examples. That is a good reference, but it does not apply to all cases. Since we are going to modify these files a lot, it's best to make a backup copy first:

```
for f in /etc/bacula/bacula-{dir,sd,fd}.conf; do sudo cp -af $f $f.bak; done
```
Now edit `/etc/bacula/bacula-dir.conf` and make the following changes/additions:

#### The `Director` resource

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

#### The `FileSet` resource

Let's define what we want to backup. There will likely be multiple file sets defined in a production server, but as an example, here we will define a set for backing up the home directory:
```
FileSet {
  Name = "Home Set"
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

#### The `Client` resource

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

#### The `Pool` resource

A *Pool* in Bacula represents a collection of volumes. A *Volume* is a single physical tape, or a file on disk, and is where Bacula will write the backup data.

The default configuration file will have defined several *Pools* already. For this documentation, we are interested in the `File` pool:
```
Pool {
  Name = File
  Pool Type = Backup
  Recycle = yes                  # Bacula can automatically recycle Volumes
  AutoPrune = yes                # Prune expired volumes
  Volume Retention = 365 days    # one year
  Maximum Volume Bytes = 50G     # Limit Volume size
  Maximum Volumes = 100          # Limit number of Volumes in Pool
  Label Format = "Vol-"          # Auto label
}
```
We will use this pool to backup to a directory on the server (which will usually be the mount point for a big storage device). The pool resource has some definitions that affect how large the backups can become, so these have to be checked:
 * `Name`: The name of the pool, which will be referenced in other resources.
 * `Volume Retention`: For how long volumes are kept.
 * `Maximum Volume Bytes`: What is the maximum size of each volume file.
 * `Maximum Volumes`: How many volume files are we going to keep at most.
 * `Label Format`: The prefix that each volume file will get. In this example, the files will be automatically named `Vol-0001`, `Vol-0002`, and so on.

With the values in the example above, we will be storing at most 50G * 100 = 5000GB in this pool.

```{tip}
For more details about all the options of the `Pool` resource, please check the upstream [Pool Resource](https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html#SECTION00231600000000000000000) documentation.
```

#### The `Storage` resource

The *Storage* resource in the bacula Director configuration file points at the system where the Storage component is running.

In our current setup, that's the same system where the Director is running, but we **MUST NOT** use `localhost` in the definition, because this configuration is also sent to the File component on other systems. In another system, `localhost` will mean itself, but the Storage daemon is not running over there.

This time we will have to change two configuration files: the Director one, and the Storage one. Let's begin by defining a `Storage` resource on `/etc/bacula/bacula-dir.conf`, the Director configuration file:
```
Storage {
  Name = FileBackup
  Address = bacula-server.lxd
  SDPort = 9103
  Password = "nuzA3-p89t_HXHYcCeoUtX7FdFQbJv8wB"
  Device = FileBackup
  Media Type = File
}
```
Here is what we have defined with the block above:
 * `Name`: The name of this Storage resource, which will be referenced in other places.
 * `Address`: The name of the system where the Storage daemon is running. Again, never use `localhost` here, even if it's the same system where the Director is running.
 * `Password`: The password that should be used when connecting to the Storage daemon. The installation of the packages will have generated a random password. It can be found either in the existing `Autochanger` definitions in `/etc/bacula/bacula-dir.conf`, or in `/etc/bacula/common_default_passwords` in the line for `SDPASSWD`, or in the Storage daemon configuration file `/etc/bacula/bacula-sd.conf`.
 * `Device`: This must match an existing `Device` definition in the Storage daemon's configuration file (which will be covered next).
 * `Media Type`: Likewise, this must also match the same `Media Type` defined in the Storage daemon's configuration file.

```{tip}
For more details about all the options of the `Pool` resource, please check the upstream [Storage Resource](https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html#blb:StorageResource) documentation.
```

Next we need to edit the corresponding Storage daemon configuration in `/etc/bacula/bacula-sd.conf`.

First, remove or comment out the `SDAddress` configuration, so that the daemon will listen on all network interfaces it finds:
```
Storage {
  Name = bacula-server-sd
  SDPort = 9103
  WorkingDirectory = "/var/lib/bacula"
  Pid Directory = "/run/bacula"
  Plugin Directory = "/usr/lib/bacula"
  Maximum Concurrent Jobs = 20
  Encryption Command = "/etc/bacula/scripts/key-manager.py getkey"
  #SDAddress = 127.0.0.1
}
```
Important points for the config above:
 * `Name`: It's standard for Bacula systems to suffix the name of the system where a component is running with the abbreviation of that component. In this case, the name of the system is `bacule-server`, and the component we are defining is the Storage Daemon, hence the `-sd` suffix.
 * `SDAddress`: We need this daemon to listen on all interfaces so it's reachable from other systems, so we comment this line out and rely on the default which it to listen on all interfaces.

Next, let's define a `Device`, also in `/etc/bacula/bacula-sd.conf`:
```
Device {
    Name = FileBackup
    Media Type = File
    Archive Device = /storage/backup
    Random Access = yes
    Automatic Mount = yes
    Removable Media = no
    Always Open = no
    Label Media = yes
}
```
What we need to pay close attention to here is:
 * `Name`: This has to match the name this device will be referred to in other services. In our case, it matches the name we are using in the `Device` entry of the `Storage` definition we added to the Director configuration file `/etc/bacula/bacula-dir.conf` earlier.
 * `Media Type`: Likewise, this has to match the entry we used in the `Storage` definition in the Director.
 * `Archive Device`: Since we are going to store backups as files, and not as tapes, the `Archive Device` configuration points to a directory. Here we are using `/storage/backup`, which can be the mount point of an external storage for example. This is the target directory of all backup jobs what will refer to this device of this storage server.
 * `Label Media`: Since we are using files and not real tapes, we want the Storage daemon to actually name the files for us. This configuration option allows it to do so.

Lastly, the Storage component needs to be told about the Director. This is done with a `Director` resource in `/etc/bacula/bacula-sd.conf`. No changes should be needed here, but it's best to check:
```
Director {
    Name = bacula-server-dir
    Password = NWib9m5fym8_bMDXtLdncPNB6qWDWCtCC
}
```
These two options need to match the following:
 * `Name`: This names which Director is allowed to use this Storage component, and therefore needs to match the `Name` defined in the `Director` resource in `/etc/bacula/bacula-dir.conf` on the Director system.
 * `Password`: The password that the Director needs to use to authenticate against this Storage component. This needs to match the `Password` set in the `Storage` resource in `/etc/bacula/bacula-dir.conf` on the Directory system.

#### The `Job` resource

The `Job` resource is the basic unit in Bacula, and ties everything together:
 * Who is being backed up (`Client`).
 * What should be backed up (`FileSet`).
 * Where should the data be stored (`Storage`, `Pool`), and where to record the job (`Catalog`)
 * When thouls the job run (`Schedule`)

The default Director configuration file includes a default Job resource, and more Jobs can inherit from that.

Let's go over the Default Job resource first in `/etc/bacula/bacula-dir.conf`:
```
JobDefs {
  Name = "DefaultJob"
  Type = Backup
  Level = Incremental
  Client = bacula-server-fd
  FileSet = "Home Set"
  Schedule = "WeeklyCycle"
  Storage = FileBackup
  Messages = Standard
  Pool = File
  SpoolAttributes = yes
  Priority = 10
  Write Bootstrap = "/var/lib/bacula/%c.bsr"
}
```
This configuration is selecting some defaults:
  * `Name`: The name of this Job.
  * `Client`: To which client it applies. This must match an existing `Client {}` resource definition.
  * `FileSet`: The name of the `FileSet` resource that defines the data to be backed up.
  * `Schedule`: The name of the `Schedule` resource that defines when this job should run.
  * `Storage`: Which `Storage` resource this job should use.
  * `Pool`: Which `Pool` resource this job should use.

We can now take advantage of this set of defaults, and define a new Job resource with minimal config:
```
Job {
    Name = "HomeBackup"
    JobDefs = "DefaultJob"
}
```

We also need a Job definition for the restore task. The default configuration file will have a definition for this already, but it needs to be changed:
```
Job {
    Name = "RestoreFiles"
    Type = Restore
    Client = bacula-server-fd
    Storage = FileBackup
    # The FileSet and Pool directives are not used by Restore Jobs
    # but must not be removed
    FileSet = "Home Set"
    Pool = File
    Messages = Standard
    Where = /storage/restore
}
```
Important parameters defined above:
 * `Name`: The name of this job.
 * `Type`: This is a job that restores backups (`Restore`).
 * `Client`: Where the files should be restored to. This can be overridden when the job is invoked.
 * `Storage`: The storage from where the backup should be restored.
 * `FileSet` and `Pool`: These are not used, but must be present and point to valid resources.
 * `Where`: The path where the restored files should be placed. This can also be overridden when the job is invoked.

```{tip}
For more details about all the options of the `Job` resource, please check the upstream [Job Resource](https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html#blb:JobResource) documentation.
```

### Storage daemon
There isn't much more to configure for the Storage daemon after the Director configuration steps done earlier, but we still need to create the directories for the backup and restore jobs:
```
sudo mkdir -m 0700 /storage /storage/backups /storage/restore
sudo chown bacula: -R /storage
```
This will allow bacula, and only bacula, to read and write to the storage path. You can, of course, adjust the permissions and ownership to something that suits your deployment. Just be mindful that the bacula user needs to be able to create and remove files from the `/storage/backups` and `/storage/restore` paths, and that regular users should not be allowed to read those.

```{tip}
For more details about the Storage daemon configuration options, please check the upstream [Storage Daemon](https://www.bacula.org/15.0.x-manuals/en/main/Storage_Daemon_Configuratio.html) documentation.
```

### File daemon
The File daemon configuration is located in the `/etc/bacula/bacula-fd.conf` file, and the only remaining task is to make sure it listens on the network. To be fair, in this particular deployment layout, this is not strictly needed, as both the Director and Storage daemons are located on the same system, but making this change allows for those components to be split off to different systems should that need arise.

To make this change, we are going to remove or comment out the `FDAddress` option in the `FileDaemon` resource in `/etc/bacula/bacula-fd.conf` file:
```
FileDaemon {
  Name = bacula-server-fd
  FDport = 9102
  WorkingDirectory = /var/lib/bacula
  Pid Directory = /run/bacula
  Maximum Concurrent Jobs = 20
  Plugin Directory = /usr/lib/bacula
  #FDAddress = 127.0.0.1
}
```
After making the change and saving the file, restart the File daemon service:
```
sudo systemctl restart bacula-fd.service
```

```{tip}
For more details about the File daemon configuration, please check the upstream [File Daemon](https://www.bacula.org/15.0.x-manuals/en/main/Client_File_daemon_Configur.html) documentation.
```


### Console
There is no further configuration to be done for the Console at this time. The defaults selected and adjusted by the package install are sufficient. The configuration file is `/etc/bacula/bconsole.conf`, and more details are available in the upstream [Console Configuration](https://www.bacula.org/15.0.x-manuals/en/main/Console_Configuration.html) documentation.

The Console can be used to query the Director about jobs, but to use the Console with a *non-root* user, the user needs to be in the **Bacula group**. To add a user to the Bacula group, run the following command from a terminal:

```bash
sudo adduser <username> bacula
```
Replace `<username>` with the actual username. Also, if you are adding the current user to the group you should log out and back in for the new permissions to take effect.

```{warning}
Be mindful of who is added to the `bacula` group: members of this group are able to read all the data that is being backed up!
```

## Our first backup
We now have everything in place to run our first backup job.


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
