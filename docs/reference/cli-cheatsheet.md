---
myst:
  html_meta:
    description: Quick reference sheet for common Ubuntu command-line commands.
---

(command-line-cheat-sheet)=
# Command-line cheat sheet

This page lists the most common commands in the Ubuntu command line.
For full details on any command, run `man <command>` in your terminal.


## Navigation

| Command | Description | Online manual page |
|---------|-------------|--------------------|
| `pwd` | Print the current working directory | {manpage}`pwd(1)`|
| `ls` | List all files and directories in the current directory | {manpage}`ls(1)` |
| `ls -l` | Long list, with permissions, owner, size, and date | |
| `ls -a` | List all, including hidden files (file names starting with `.`) | |
| `ls -la` or `ll` | Long listing including hidden files | |
| `ls -ld <dir>` | Show the directory entry itself, not its contents, for directory `<dir>` |
| `ls -l <file>` | Show file type, permissions, owner, and size for `<file>` |
| `cd <path>` | Change to the specified directory | _[cd(1posix)](https://manpages.ubuntu.com/manpages/resolute/man1/cd.1posix.html)_|
| `cd ..` | Move up to the parent directory | |
| `cd ~` | Return to the home directory | |
| `cd -` | Return to the previous directory | |
| `cd /` | Move to the root directory | |
| `cd ../../` | Move up two levels at once | |


## Working with the filesystem

| Command | Description | Online manual page |
|---------|-------------|--------------------|
| `mkdir <name>` | Create a new directory | {manpage}`mkdir(1)`|
| `rmdir <name>` | Remove an empty directory | {manpage}`rmdir(1)`|
| `tree` | Display directory structure as a tree | {manpage}`tree(1)`|
| `tree -L <n> <path>` | Display tree to depth `n` | |


## Working with files

| Command | Description | Online manual page |
|---------|-------------|--------------------|
| `touch <file>` | Create a new (empty) file, or update the timestamp of an existing file | {manpage}`touch(1)`|
| `cp <src> <dest>` | Copy a file from a source (`src`) to a new destination (`dest`) | {manpage}`cp(1)`|
| `cp -a <src> <dest>` | Copy a directory recursively, preserving permissions | |
| `mv <src> <dest>` | Rename a file or directory | {manpage}`mv(1)` |
| `mv <src>/file <dest>/file` | Move a file without renaming it | | 
| `rm <file>` | Remove a file | {manpage}`rm(1)` |
| `rm -r <dir>` | Remove a non-empty directory and all its contents | |
| `cat <file>` | Print the contents of `<file>` to the screen | {manpage}`cat(1)`|
| `less <file>` | View file contents one page at a time | {manpage}`less(1)`|
| `head -n 20 <file>` | Print the first 20 lines of a file (default with no flag is 10) | {manpage}`head(1)`|
| `tail -n 20 <file>` | Print the last 20 lines of a file (default with no flag is 10) | {manpage}`tail(1)`|


## Users, groups, and permissions

| Command | Description | Online manual page |
|---------|-------------|--------------------|
| `chmod <mode> <file>` | Change file permissions (symbolic or numeric notation) | {manpage}`chmod(1)`|
| `chown <user>:<group> <file>` | Change file owner and group | {manpage}`chown(1)`|
| `umask` | Show or set the default permissions mask  | {manpage}`umask(2)`|
| `sudo <command>` | Run a command with administrator privileges | {manpage}`sudo(8) <sudo-rs(8)>`|


## Searching

| Command | Description | Online manual page |
|---------|-------------|--------------------|
| `grep <pattern> <file>` | Search for lines matching a pattern in a file  | {manpage}`grep(1)`|
| `grep <name> /etc/passwd` | Look up a user account | |
| `grep <name> /etc/group` | Look up group membership | |
| `find <path> -name <pattern>` | Search for files matching a name pattern  | {manpage}`find(1)`|
| `which <command>` | Show the full path to an executable command  | {manpage}`which(1) <which.debianutils(1)>`|
| `file <name>` | Determine the type of a file  | {manpage}`file(1)`|


## Getting help

| Command | Description | Online manual page |
|---------|-------------|--------------------|
| `man <command>` | Open the manual page for a command ||
| `man man` | Open the manual page for `man` itself | {manpage}`man(1)`|
| `man -k <keyword>` | Search man page descriptions for a keyword ||
| `<command> --help` | Print a brief help summary for a command ||

