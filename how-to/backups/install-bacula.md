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

## Install Bacula

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

## Configure Bacula

Several components were installed on this system by the `bacula` package. Each one has its own configuration file:

 * Director: `/etc/bacula/bacula-dir.conf`
 * Storage: `/etc/bacula/bacula-sd.conf`
 * File: `/etc/bacula/bacula-fd.conf`
 * Console: `/etc/bacula/bconsole.conf`

All these components need to eventually talk to each other, and the authentication is performed via passwords that were automatically generated at install time. These passwords are stored in the `/etc/bacula/common_default_passwords` file. If a new component is installed on this system, it can benefit from this file to automatically be ready to authenticate itself, but in general, after everything is installed and configured, this file isn't needed anymore.

The default installation of all these components already configured several aspects of bacula, but some fine tuning will be needed.

### Storage

Bacula has support for many different storage devices, notable tape drives, and the default configuration has many examples. Here we will configure a path for the Storage component to use for backups and restores, and it is assumed that this path is a mount point for some external storage device.

### Director


Bacula configuration files are formatted based on **resources** composed of **directives** surrounded by curly “{}” braces. Each Bacula component has an individual file in the `/etc/bacula` directory.

The various Bacula components must authorise themselves to each other. This is accomplished using the **password** directive. For example, the Storage resource password in the `/etc/bacula/bacula-dir.conf` file must match the Director resource password in `/etc/bacula/bacula-sd.conf`.

By default, the backup job named `BackupClient1` is configured to archive the Bacula Catalog. If you plan on using the server to back up more than one client you should change the name of this job to something more descriptive. To change the name, edit `/etc/bacula/bacula-dir.conf`:

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

## Further reading

* For more Bacula configuration options, refer to the [Bacula documentation](https://www.bacula.org/documentation/documentation/).

* The [Bacula home page](http://www.bacula.org/) contains the latest Bacula news and developments.

* Also, see the [Bacula Ubuntu Wiki](https://help.ubuntu.com/community/Bacula) page.
