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

| Command | Description |
|---------|-------------|
| `pwd` | Print the current working directory |
| `ls` | List all files and directories in the current directory |
| `ls -l` | Long list, with permissions, owner, size, and date |
| `ls -a` | List all, including hidden files (file names starting with `.`) |
| `ls -la` or `ll` | Long listing including hidden files |
| `ls -ld <dir>` | Show the directory entry itself, not its contents, for directory `<dir>` |
| `ls -l <file>` | Show file type, permissions, owner, and size for `<file>` |
| `cd <path>` | Change to the specified directory |
| `cd ..` | Move up to the parent directory |
| `cd ~` | Return to the home directory |
| `cd -` | Return to the previous directory |
| `cd /` | Move to the root directory |
| `cd ../../` | Move up two levels at once |


## Working with the filesystem

| Command | Description |
|---------|-------------|
| `mkdir <name>` | Create a new directory |
| `rmdir <name>` | Remove an empty directory |
| `tree` | Display directory structure as a tree |
| `tree -L <n> <path>` | Display tree to depth `n` |


## Working with files

| Command | Description |
|---------|-------------|
| `touch <file>` | Create a new (empty) file, or update the timestamp of an existing file |
| `cp <src> <dest>` | Copy a file from a source (`src`) to a new destination (`dest`) |
| `cp -a <src> <dest>` | Copy a directory recursively, preserving permissions |
| `mv <src> <dest>` | Rename a file or directory |
| `mv <src>/file <dest>/file` | Move a file without renaming it | 
| `rm <file>` | Remove a file |
| `rm -r <dir>` | Remove a non-empty directory and all its contents |
| `cat <file>` | Print the contents of `<file>` to the screen |
| `less <file>` | View file contents one page at a time |
| `head -n 20 <file>` | Print the first 20 lines of a file (default without the flag is 10) |
| `tail <file>` | Print the last 10 lines of a file |


## Users, groups, and permissions

| Command | Description |
|---------|-------------|
| `chmod <mode> <file>` | Change file permissions (symbolic or numeric notation) |
| `chown <user>:<group> <file>` | Change file owner and group |
| `umask` | Show or set the default permissions mask |
| `sudo <command>` | Run a command with administrator privileges |
| `grep <name> /etc/passwd` | Look up a user account |
| `grep <name> /etc/group` | Look up group membership |


## Searching

| Command | Description |
|---------|-------------|
| `grep <pattern> <file>` | Search for lines matching a pattern in a file |
| `find <path> -name <pattern>` | Search for files matching a name pattern |
| `which <command>` | Show the full path to an executable command |
| `file <name>` | Determine the type of a file |


## Getting help

| Command | Description |
|---------|-------------|
| `man <command>` | Open the manual page for a command |
| `man man` | Open the manual page for `man` itself |
| `man -k <keyword>` | Search man page descriptions for a keyword |
| `<command> --help` | Print a brief help summary for a command |

