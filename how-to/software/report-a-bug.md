(report-a-bug)=
# How to report a bug in Ubuntu Server

The Ubuntu project, including Ubuntu Server, [uses Launchpad](https://launchpad.net/) as its bug tracker. To file a bug, you will first need to [create a Launchpad account](https://help.launchpad.net/YourAccount/NewAccount).

## Report bugs with `apport-cli`

The preferred way to report a bug is with the `apport-cli` command. This command collects information from the machine on which it is run and publishes it to the bug report on Launchpad.

Getting this information to Launchpad can be a challenge if the system is not running a desktop environment with a browser (a common scenario with servers) or if it does not have Internet access. The steps to take in these situations are described below.

```{note}
The commands `apport-cli` and `ubuntu-bug` should give the same results on a command-line interface (CLI) server. The latter is actually a symlink to `apport-bug`, which is intelligent enough to know whether a desktop environment is in use, and will choose `apport-cli` if not. Since server systems tend to be CLI-only, `apport-cli` was chosen from the outset in this guide.
```

Bug reports in Ubuntu need to be filed against a specific software package, so the name of the package (source package or program name/path) affected by the bug needs to be supplied to `apport-cli`:

```bash
apport-cli PACKAGENAME
```

Once `apport-cli` has finished gathering information you will be asked what to do with it. For instance, to report a bug against vim using `apport-cli vim` produces output like this:

```text
*** Collecting problem information
    
The collected information can be sent to the developers to improve the
application. This might take a few minutes.
...
    
*** Send problem report to the developers?
    
After the problem report has been sent, please fill out the form in the
automatically opened web browser.
   
What would you like to do? Your options are:
  S: Send report (2.8 KB)
  V: View report
  K: Keep report file for sending later or copying to somewhere else
  I: Cancel and ignore future crashes of this program version
  C: Cancel
Please choose (S/V/K/I/C):
```

The first three options are described below.

### S: Send report

Submits the collected information to Launchpad as part of the process of filing a new bug report. You will be given the opportunity to describe the bug in your own words.
    
```text 
*** Uploading problem information
    
The collected information is being sent to the bug tracking system.
This might take a few minutes.
94%
    
*** To continue, you must visit the following URL:
    
  https://bugs.launchpad.net/ubuntu/+source/vim/+filebug/09b2495a-e2ab-11e3-879b-68b5996a96c8?
    
You can launch a browser now, or copy this URL into a browser on another computer.
    
    
Choices:
  1: Launch a browser now
  C: Cancel
Please choose (1/C):  1
```
    
The browser that will be used when choosing '1' will be the one known on the system as `www-browser` via the [Debian alternatives system](https://manpages.ubuntu.com/manpages/en/man1/update-alternatives.1.html). Examples of text-based browsers to install include links, {term}`ELinks`, lynx, and w3m. You can also manually point an existing browser at the given URL.

### V: View

This displays the collected information on the screen for review. This can be a lot of information! Press <kbd>Enter</kbd> to scroll through the screens. Press <kbd>q</kbd> to quit and return to the choice menu.

### K: Keep

This writes the collected information to disk. The resulting file can be later used to file the bug report, typically after transferring it to another Ubuntu system.
    
```text    
What would you like to do? Your options are:
  S: Send report (2.8 KB)
  V: View report
  K: Keep report file for sending later or copying to somewhere else
  I: Cancel and ignore future crashes of this program version
  C: Cancel
Please choose (S/V/K/I/C): k
Problem report file: /tmp/apport.vim.1pg92p02.apport
```

To report the bug, get the file onto an Internet-enabled Ubuntu system and apply `apport-cli` to it. This will cause the menu to appear immediately (since the information is already collected). You should then press <kbd>s</kbd> to send:

```bash    
apport-cli apport.vim.1pg92p02.apport
```    

To directly save a report to disk (without menus) you can run:

```bash
apport-cli vim --save apport.vim.test.apport
```

Report names should end in `.apport`.
   
```{note}
If this Internet-enabled system is non-Ubuntu/Debian, `apport-cli` is not available so the bug will need to be created manually. An `apport` report is also not to be included as an attachment to a bug either so it is completely useless in this scenario.
```

## Reporting application crashes

The software package that provides the `apport-cli` utility, `apport`, can be configured to automatically capture the state of a crashed application. This is enabled by default in `/etc/default/apport`.

After an application crashes, if enabled, `apport` will store a crash report under `/var/crash`:

```text
-rw-r----- 1 peter    whoopsie 150K Jul 24 16:17 _usr_lib_x86_64-linux-gnu_libmenu-cache2_libexec_menu-cached.1000.crash
```

Use the `apport-cli` command with no arguments to process any pending crash reports. It will offer to report them one by one, as in the following example:

```bash
apport-cli
``` 

```text
*** Send problem report to the developers?
    
After the problem report has been sent, please fill out the form in the
automatically opened web browser.
    
What would you like to do? Your options are:
  S: Send report (153.0 KB)
  V: View report
  K: Keep report file for sending later or copying to somewhere else
  I: Cancel and ignore future crashes of this program version
  C: Cancel
Please choose (S/V/K/I/C): s
```

If you send the report, as was done above, the prompt will be returned immediately and the `/var/crash` directory will then contain 2 extra files:

```text
-rw-r----- 1 peter    whoopsie 150K Jul 24 16:17 _usr_lib_x86_64-linux-gnu_libmenu-cache2_libexec_menu-cached.1000.crash
-rw-rw-r-- 1 peter    whoopsie    0 Jul 24 16:37 _usr_lib_x86_64-linux-gnu_libmenu-cache2_libexec_menu-cached.1000.upload
-rw------- 1 whoopsie whoopsie    0 Jul 24 16:37 _usr_lib_x86_64-linux-gnu_libmenu-cache2_libexec_menu-cached.1000.uploaded
```

Sending in a crash report like this will not immediately result in the creation of a new public bug. The report will be made private on Launchpad, meaning that it will be visible to only a limited set of bug triagers. These triagers will then scan the report for possible private data before creating a public bug.

## Further reading

- See the [Reporting Bugs](https://help.ubuntu.com/community/ReportingBugs) Ubuntu wiki page.
- Also, [the Apport page](https://wiki.ubuntu.com/Apport) has some useful information. Though some of it pertains to using a {term}`GUI`.
