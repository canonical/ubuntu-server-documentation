(install-bacula)=
# How to install and configure Bacula

[Bacula](http://www.bacula.org/) is a backup management tool that enables you to backup, restore, and verify data across your network. There are Bacula clients for Linux, Windows, and Mac OS X -- making it a cross-platform and network-wide solution.

## Bacula components

Bacula is made up of several components and services that are used to manage backup files and locations:

- **Bacula Director**: A service that controls all backup, restore, verify, and archive operations.

- **Bacula Console**: An application that allows communication with the Director.

- **Bacula File**: This application is installed on machines to be backed up, and is responsible for handling data requested by the Director.

- **Bacula Storage**: The program that performs the storage of data onto, and recovery of data from, the physical media.

- **Bacula Catalog**: Responsible for maintaining the file indices and volume databases for all backed-up files. This enables rapid location and restoration of archived files. The Catalog supports three different databases: MySQL, PostgreSQL, and SQLite.

- **Bacula Monitor**: This is a graphical tray monitor for the Bacula backup system.

These services and applications can be run on multiple servers and clients, or they can be installed on one machine if backing up a single disk or volume.

In this documentation, we will deploy a Bacula Director, with a backup job for the Director itself, and also install the Bacule File service on a workstation, to remotely backup its data.

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
 * `Name`: it's common to use the format `$hostname-dir` for the director. For example, if the hostname is "`bacula-server`", the name here would be `bacula-server-dir`. By sticking to this pattern, less changes will have to be made to the config, as this is what the default installation already assumes.
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

Let's go over the Default Job resource first in `/etc/bacula/bacula-dir.conf` and change it a little bit:
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
    Name = "DirectorHomeBackup"
    JobDefs = "DefaultJob"
}
```

```{tip}
A job has many attributes that can only be specified once. This means that jobs are pretty much specific to what is being backed up, and from where, among other things. It therefore helps to come up with a naming convention.

The upstream documentation has a section about [Naming Resources](https://docs.baculasystems.com/BEPlanningAndPreparation/BackupPolicy/NamingResources/index.html) with some suggestions.
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

### Cleaning up
We have added new resources to some Bacula components, and changed some existing ones. There are also resources we didn't touch, but they will show up in the console or logs. Optionally, we can remove them to cleanup our config files.

In `/etc/bacula/bacula-dir.conf`:
 * all the `Autochanger` resources can be removed, since they are not referred to by any other resource.

In `/etc/bacula/bacula-sd.conf`:
 * The `Autochanger` resources can be removed, as it's not being used.
 * The `FileChgr1-Dev1`, `FileChgr1-Dev2`, `FileChgr2-Dev1`, and `FileChgr2-Dev2` Devices, referred to by the Autochangers above, should then also be removed.


## Our first backup and restore
We now have everything in place to run our first backup job.

On the Bacula Director system, run the `bconsole` command as root to enter the Bacula Console:

```
sudo bconsole
```
The command will connect to the the local Director, and open up an interactive prompt:
```
Connecting to Director localhost:9101
1000 OK: 10002 bacula-server-dir Version: 15.0.3 (25 March 2025)
Enter a period to cancel a command.
*
```
You can type `help` for a full list of all the available commands, and `help <command>` for more detailed information about the specific `<command>`.

For example, to obtain help text about the `run` command, type `help run` to obtain the following output:
```
  Command       Description
  =======       ===========
  run           Run a job

Arguments:
        job=<job-name> client=<client-name>
        fileset=<FileSet-name> level=<level-keyword>
        storage=<storage-name> where=<directory-prefix>
        when=<universal-time-specification> pool=<pool-name>
         nextpool=<next-pool-name> comment=<text> accurate=<bool> spooldata=<bool> yes

When at a prompt, entering a period cancels the command.
```
Let's interactively run a backup job. The output below will show the `run` command and all the replies that were typed in response to the console prompts:
```
*run
Using Catalog "MyCatalog"
A job name must be specified.
The defined Job resources are:
     1: HomeBackup
     2: BackupCatalog
     3: RestoreFiles
Select Job resource (1-3): 1
Run Backup job
JobName:  HomeBackup
Level:    Incremental
Client:   bacula-server-fd
FileSet:  Home Set
Pool:     File (From Job resource)
Storage:  FileBackup (From Job resource)
When:     2025-10-20 20:21:03
Priority: 10
OK to run? (Yes/mod/no): yes
Job queued. JobId=7
```
Let's unpack this:
 * `run`: This is the command. Since no parameters were given, Bacula will ask for what's missing.
 * Which job should be run: `HomeBackup` is the job we defined in this how-to, and we select it by its index number.
 * Summary: at the end, we are given a summary of the job. Here we can still change values via the `mod` reply, but for now let's just accept those values and reply `yes`.
 * JobId: the job is accepted, and we are given an ID. In this case, it was "`7`".

To check the result of a job, there are several methods:
 * Messages: right after scheduling the job, it's likely something will be logged. You can run the `messages` command, and it will show the latest unread messages (and also mark them as read, so you can only benefit from this once).
 * The `list jobs` command, to list all jobs, or, more specifically, `list jobid=7` to list a particular job.
 * Inspect the full log of that particular job, via the `list joblog jobid=<N>` command.
 * Server log: you can inspect the server log at `/var/log/bacula/bacula.log`.

For example, if we run `list jobid=7`, this is the output:
```
+-------+------------+---------------------+------+-------+----------+----------+-----------+
| jobid | name       | starttime           | type | level | jobfiles | jobbytes | jobstatus |
+-------+------------+---------------------+------+-------+----------+----------+-----------+
|     7 | HomeBackup | 2025-10-20 20:21:11 | B    | I     |        0 |        0 | T         |
+-------+------------+---------------------+------+-------+----------+----------+-----------+
```
That tells us some details about this job, in particular that it finished correctly (the `T` code).

```{tip}
For a list of status and error codes, check the upstream [Job status and Error codes tables](https://www.bacula.org/15.0.x-manuals/en/main/Job_status_Error_codes.html#blb:director:job:status).
```

To see the full log of this specific job, we can use the `list joblog jobid=7` command. This is quite detailed, and the output below is truncated for brevity:
```
+----------------------------------------------------------------------------------------------------+
| logtext                                                                                              |
+----------------------------------------------------------------------------------------------------+
| bacula-server-dir JobId 7: Start Backup JobId 7, Job=HomeBackup.2025-10-20_20.21.08_03               |
| bacula-server-dir JobId 7: Connected to Storage "FileBackup" at bacula-server.lxd:9103 with TLS      |
| bacula-server-dir JobId 7: Using Device "FileBackup" to write.                                       |
...
  Build OS:               x86_64-pc-linux-gnu ubuntu 25.10
  JobId:                  7
  Job:                    HomeBackup.2025-10-20_20.21.08_03
  Backup Level:           Incremental, since=2025-10-20 18:11:00
  Client:                 "bacula-server-fd" 15.0.3 (25Mar25) x86_64-pc-linux-gnu,ubuntu,25.10
  FileSet:                "Home Set" 2025-10-20 16:27:31
  Pool:                   "File" (From Job resource)
  Catalog:                "MyCatalog" (From Client resource)
  Storage:                "FileBackup" (From Job resource)
...
  Non-fatal FD errors:    0
  SD Errors:              0
  FD termination status:  OK
  SD termination status:  OK
  Termination:            Backup OK                                                                    |
...
```

If we inspect the backup target location on the Storage server (which in this deployment is the same as the Director), we can see that a volume file was created:
```
-rw-r----- 1 bacula tape 345K Oct 20 20:21 /storage/backups/Vol-0001
```

So what is it that was backed up? This job used the `Home Set`, so we expect to see files from the `/home` directory. To see what are the contents of that backup job, we can use the `restore` job. Below is the output of an interactive `restore` session where we selected the option "Select the most recent bakcup for a client":
```
First you select one or more JobIds that contain files
to be restored. You will be presented several methods
of specifying the JobIds. Then you will be allowed to
select which files from those JobIds are to be restored.

To select the JobIds, you have the following choices:
     1: List last 20 Jobs run
...
     5: Select the most recent backup for a client
...
Select item:  (1-14): 5
Automatically selected Client: bacula-server-fd
Automatically selected FileSet: Home Set
+-------+-------+----------+----------+---------------------+------------+
| jobid | level | jobfiles | jobbytes | starttime           | volumename |
+-------+-------+----------+----------+---------------------+------------+
|     4 | F     |      266 |  312,756 | 2025-10-20 17:34:43 | Vol-0001   |
|     5 | I     |        3 |       32 | 2025-10-20 18:11:00 | Vol-0001   |
+-------+-------+----------+----------+---------------------+------------+
You have selected the following JobIds: 4,5
...
You are now entering file selection mode where you add (mark) and
remove (unmark) files to be restored. No files are initially added, unless
you used the "all" keyword on the command line.
Enter "done" to leave this mode.

cwd is: /
$
```
Here we can navigate the filesystem and inspect which files are part of the backup:
```
$ dir
drwxr-xr-x   1 root     root              12  2025-10-20 14:03:44  /home/
$ cd home/ubuntu
cwd is: /home/ubuntu/
$ dir
-rw-------   1 ubuntu   ubuntu            32  2025-10-20 18:10:51  /home/ubuntu/.bash_history
-rw-r--r--   1 ubuntu   ubuntu           220  2025-10-20 14:03:50  /home/ubuntu/.bash_logout
-rw-r--r--   1 ubuntu   ubuntu          3830  2025-10-20 14:03:50  /home/ubuntu/.bashrc
-rw-r--r--   1 ubuntu   ubuntu           807  2025-10-20 14:03:44  /home/ubuntu/.profile
drwx------   1 ubuntu   ubuntu            30  2025-10-20 14:03:45  /home/ubuntu/.ssh/
-rw-rw-r--   1 ubuntu   ubuntu             0  2025-10-20 18:10:50  /home/ubuntu/this-is-on-the-server.txt
```

To restore a file, we use the `mark` command on it. For example, let's restore `/home/ubuntu/.tmux.conf`:
```
$ mark .tmux.conf
1 file marked.
$ done
Bootstrap records written to /var/lib/bacula/bacula-server-dir.restore.1.bsr

The Job will require the following (*=>InChanger):
   Volume(s)                 Storage(s)                SD Device(s)
===========================================================================

    Vol-0001                  FileBackup                FileBackup

Volumes marked with "*" are in the Autochanger.


1 file selected to be restored.

Run Restore job
JobName:         RestoreFiles
Bootstrap:       /var/lib/bacula/bacula-server-dir.restore.1.bsr
Where:           /storage/restore
Replace:         Always
FileSet:         Home Set
Backup Client:   bacula-server-fd
Restore Client:  bacula-server-fd
Storage:         FileBackup
When:            2025-10-20 21:02:37
Catalog:         MyCatalog
Priority:        10
Plugin Options:  *None*
OK to run? (Yes/mod/no):
```
Now we have some choices. Notice how the `RestoreFiles` job was automatically selected. That's the only job of the type `Restore` that we defined in the Director configuration earlier. It has certain default values, and we can either accept those (by replying `yes`), or modify them (by replying `mod`).

If we accept these default, the marked files will be restored to the `/storage/restore` path on the `bacula-server-fd` system:
```
OK to run? (Yes/mod/no): yes
Job queued. JobId=8
*
```
And indeed, if we inspect that location, we see the file that we marked for restoration:
```
-rw-r--r-- 1 ubuntu ubuntu 2.4K Oct 20 14:03 /storage/restore/home/ubuntu/.tmux.conf
```

If we wanted to restore it to its original place, for example, if the user mistakenly deleted it and wanted it back, we would select the `mod` option to change where the file should be placed:
```
OK to run? (Yes/mod/no): mod
Parameters to modify:
     1: Level
     2: Storage
     3: Job
     4: FileSet
     5: Restore Client
     6: When
     7: Priority
     8: Bootstrap
     9: Where
    10: File Relocation
    11: Replace
    12: JobId
    13: Plugin Options
Select parameter to modify (1-13): 9
Please enter the full path prefix for restore (/ for none): /
Run Restore job
JobName:         RestoreFiles
Bootstrap:       /var/lib/bacula/bacula-server-dir.restore.2.bsr
Where:
Replace:         Always
FileSet:         Home Set
Backup Client:   bacula-server-fd
Restore Client:  bacula-server-fd
Storage:         FileBackup
When:            2025-10-20 21:11:55
Catalog:         MyCatalog
Priority:        10
Plugin Options:  *None*
OK to run? (Yes/mod/no): yes
Job queued. JobId=9
```
By giving a restoration prefix of `/`, we are essentially asking to restore the file at its original full path.


## Adding a client
If we want to start backing up a new system, we need to install the File Daemon on that system and include it in the Bacula Director. In this example, the new system we are adding is called `workstation1`.

First, on the system that we want to add, let's install the client portion of Bacula, which is the File Daemon component:

```
sudo apt install bacula-fd
```
Next, update the Director resource in `/etc/bacula/bacula-fd.conf` to point at the existing Director we have already deployed:
```
Director {
  Name = bacula-server-dir # same as Director's Name on the Director server
  Password = "JdRJy-5vaCuj7FywN2rXK0xDYsbtui6Mj" # to be added to the Director
}
```
Notes:
 * `Name`: This has to be the same name set on the Director's `/etc/bacula/bacula-dir.conf` file, in the `Director` resource over there. It's not the hostname.
 * `Password`: The password was randomly generated when the `bacula-fd` package was installed. This password has to match the password in the new `Client` resource that we will add to the Director next.

Also in `/etc/bacula/bacula-fd.conf`, we have to remove or comment out the `FDAddress` parameter in the `FileDaemon` resource, so that this service will listen on all available network interfaces, and not just localhost:
```
FileDaemon {
  Name = workstation1-fd
  FDport = 9102           # where we listen for the director
  WorkingDirectory = /var/lib/bacula
  Pid Directory = /run/bacula
  Maximum Concurrent Jobs = 20
  Plugin Directory = /usr/lib/bacula
  #FDAddress = 127.0.0.1  # default is to listen on all interfaces
}
```
And finally, in the same file, update the `Messages` resource and update the Director name in there as well:
```
Messages {
    Name = Standard
    director = bacula-server-dir = all, !skipped, !restored, !verified, !saved
}
```
With these changes done, restart the File Daemon:
```
sudo systemctl restart bacula-fd.service
```

Now we switch to the Director system, where we have to let it know about this new Client that we just provisioned.

In `/etc/bacula/bacula-dir.conf`, add a new `Client` resource:
```
Client {
    Name = workstation1-fd
    Address = workstation1.lxd
    FDPort = 9102
    Catalog = MyCatalog
    Password = "JdRJy-5vaCuj7FywN2rXK0xDYsbtui6Mj" # password from bacula-fd.conf on workstation1-fd
    File Retention = 60 days
    Job Retention = 6 months
    AutoPrune = yes
}
```
Notes:
 * `Name`: The name has to match the name defined in the `FileDaemon` resource from `/etc/bacula/bacula-fd.conf` of the system we just added.
 * `Password`: The password has to be the same as the one defined in the `Director` resource from `/etc/bacula/bacula-fd.conf` of that system.
 * `Address`: The hostname or IP of the system we added.

This makes the Director know how to reach the new client.

Now we have to define a new job to backup files from this new client. Again on `/etc/bacula/bacula-dir.conf` on the Director, let's add a new `Job` resource:
```
Job {
    Name = "BackupWorkstation"
    JobDefs = "DefaultJob"
    Client = workstation1-fd
}
```
This job inherits all parameters from the `DefaultJob`, and just overrides the client.

With this done, we can restart the Director:
```
sudo systemctl restart bacula-dir.service
```

If we now enter the console, we should be able to list the new client, and run its new backup job:
```
*list clients
Automatically selected Catalog: MyCatalog
Using Catalog "MyCatalog"
+----------+------------------+---------------+--------------+
| clientid | name             | fileretention | jobretention |
+----------+------------------+---------------+--------------+
|        1 | bacula-server-fd |     5,184,000 |   15,552,000 |
|        2 | workstation1-fd  |     5,184,000 |   15,552,000 |
+----------+------------------+---------------+--------------+
```
Let's run the new `BackupWorkstation` job:
```
*run
Using Catalog "MyCatalog"
A job name must be specified.
The defined Job resources are:
     1: HomeBackup
     2: BackupWorkstation
     3: BackupCatalog
     4: RestoreFiles
Select Job resource (1-4): 2
Run Backup job
JobName:  BackupWorkstation
Level:    Incremental
Client:   workstation1-fd
FileSet:  Home Set
Pool:     File (From Job resource)
Storage:  FileBackup (From Job resource)
When:     2025-10-21 21:02:48
Priority: 10
OK to run? (Yes/mod/no): yes
Job queued. JobId=14
You have messages.
```

And for a quick check of the contents (for testing, there was a file called `this-is-workstation1.txt` in `/home/ubuntu` on that system):
```
*restore
...
     5: Select the most recent backup for a client
...
Select item:  (1-14): 5
Defined Clients:
     1: bacula-server-fd
     2: workstation1-fd
Select the Client (1-2): 2
...
$ cd home/ubuntu
cwd is: /home/ubuntu/
$ dir this*
-rw-rw-r--   1 ubuntu   ubuntu             0  2025-10-21 21:02:08  /home/ubuntu/this-is-workstation1.txt
```

## Further reading

* For more Bacula configuration options, refer to the [Bacula documentation](https://www.bacula.org/documentation/documentation/).

* The [Bacula home page](http://www.bacula.org/) contains the latest Bacula news and developments.

* Also, see the [Bacula Ubuntu Wiki](https://help.ubuntu.com/community/Bacula) page.
