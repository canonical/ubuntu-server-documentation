---
myst:
  html_meta:
    description: "Reference documentation for Byobu terminal multiplexer, including keyboard shortcuts and configuration options."
---

(byobu)=
# Byobu


One of the most useful applications for any system administrator is an xterm multiplexer such as screen or tmux. It allows for the execution of multiple shells in one terminal. To make some of the advanced multiplexer features more user-friendly and provide some useful information about the system, the byobu package was created. It acts as a wrapper to these programs. By default Byobu is installed in Ubuntu server and it uses tmux (if installed) but this can be changed by the user.

Invoke it simply with:

    byobu

Now bring up the configuration menu. By default this is done by pressing the *F9* key. This will allow you to:

  - Help -- Quick Start Guide

  - Toggle status notifications

  - Change the escape sequence

  - Byobu currently does not launch at login (toggle on)

byobu provides a menu which displays the Ubuntu release, processor information, memory information, and the time and date. The effect is similar to a desktop menu.

Using the *"Byobu currently does not launch at login (toggle on)"* option will cause byobu to be executed any time a terminal is opened. Changes made to byobu are on a per user basis, and will not affect other users on the system.

One difference when using byobu is the *scrollback* mode. Press the *F7* key to enter scrollback mode. Scrollback mode allows you to navigate past output using *vi* like commands. Here is a quick list of movement commands:

  - *h* - Move the cursor left by one character

  - *j* - Move the cursor down by one line

  - *k* - Move the cursor up by one line

  - *l* - Move the cursor right by one character

  - *0* - Move to the beginning of the current line

  - *$* - Move to the end of the current line

  - *G* - Moves to the specified line (defaults to the end of the buffer)

  - */* - Search forward

  - *?* - Search backward

  - *n* - Moves to the next match, either forward or backward

## Resources

  - For more information on screen see the [screen web site](http://www.gnu.org/software/screen/).

  - And the [Ubuntu Wiki screen](https://help.ubuntu.com/community/Screen) page.

  - Also, see the byobu [project page](https://launchpad.net/byobu) for more information.
