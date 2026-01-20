---
myst:
  html_meta:
    description: "Reference documentation for terminal multiplexers including tmux, screen, and Byobu, with detailed tmux examples and usage patterns."
---

(terminal-multiplexers)=
# Terminal multiplexers

Terminal multiplexers are essential tools for system administrators and power users. They allow you to run multiple terminal sessions within a single window, detach from sessions while keeping processes running, and reattach to those sessions later. This provides protection against network disconnects, enables persistent remote sessions, and allows you to organize your workflow across multiple virtual terminals.

The key benefits of using a terminal multiplexer include:

- **Session persistence**: Processes continue running even after disconnecting from SSH
- **Multiple windows**: Run multiple shells in one terminal session
- **Session sharing**: Multiple users can attach to the same session for collaboration or training
- **Split panes**: View and interact with multiple terminals simultaneously
- **Scrollback buffers**: Review command output history
- **Scripting and automation**: Create and restore complex session layouts

## tmux

tmux (terminal multiplexer) is the modern, actively developed terminal multiplexer that has become the standard choice for most users. It offers a rich feature set, better performance than older alternatives, and active development with regular updates. For detailed information, see the {manpage}`tmux(1)` manual page.

tmux is pre-installed on Ubuntu Server, so you can start using it immediately without any installation steps.

### Control key and keybindings

tmux uses a two-step command system: first press a "prefix" key (also called the control key), then press a command key. This prevents tmux commands from interfering with normal terminal applications. The default prefix key is {kbd}`Ctrl+b`. After pressing the prefix, release it, then press the command key to issue various commands. These command combinations are called *keybindings*.

**Detaching from a session**:

To detach from your current session while keeping all programs running:

- {kbd}`Ctrl+b` {kbd}`d` - Detach from session

After detaching, you can safely close your terminal or disconnect from SSH - your session continues running.

### Session management

Session management is one of tmux's most powerful features. Sessions allow you to preserve your work environment - when you detach from a session, all programs continue running in the background. This is particularly valuable for long-running tasks, maintaining persistent development environments, or recovering from network disconnections during SSH sessions.

Create a named session for easy identification:

```bash
tmux new-session -s myproject
```

List all sessions:

```bash
tmux list-sessions
# or the shorthand:
tmux ls
```

Attach to a specific session by name:

```bash
tmux attach-session -t myproject
# or the shorthand:
tmux a -t myproject
```

To attach to a session and detach all other clients connected to it:

```bash
tmux attach-session -t myproject -d
```

This is useful when you want exclusive access to a session.

Attach to the most recent session:

```bash
tmux attach
```

Kill a session:

```bash
tmux kill-session -t myproject
```

### Window management

Windows in tmux are like tabs in a browser - each window is a separate workspace within a session. You can have multiple windows open and switch between them.

**Creating and navigating windows**:

- {kbd}`Ctrl+b` {kbd}`c` - Create a new window
- {kbd}`Ctrl+b` {kbd}`n` - Switch to next window
- {kbd}`Ctrl+b` {kbd}`p` - Switch to previous window
- {kbd}`Ctrl+b` {kbd}`0-9` - Switch to window number 0-9
- {kbd}`Ctrl+b` {kbd}`,` - Rename current window
- {kbd}`Ctrl+b` {kbd}`w` - List all windows and select from an interactive menu

:::{note}
When you exit the shell in a window (by typing `exit` or pressing {kbd}`Ctrl+d`), that window closes. If it was the last window in a session, the entire tmux session terminates.
:::

### Pane management

Within a window, you can split your terminal into multiple panes to view different shells simultaneously.

**Creating and navigating panes**:

- {kbd}`Ctrl+b` {kbd}`%` - Split pane vertically (side by side)
- {kbd}`Ctrl+b` {kbd}`"` - Split pane horizontally (top and bottom)
- {kbd}`Ctrl+b` {kbd}`o` - Switch to next pane
- {kbd}`Ctrl+b` {kbd}`arrow-key` - Navigate between panes using arrow keys
- {kbd}`Ctrl+b` {kbd}`x` - Close current pane (prompts for confirmation)

Closing a pane terminates the shell running in it. If you want to preserve the process, detach from the session instead of closing panes.

**Resizing panes**:

Once you have multiple panes, you can resize them. The easiest method is to **hold** {kbd}`Ctrl+b` and while holding use the arrow keys {kbd}`←` {kbd}`↑` {kbd}`→` {kbd}`↓` to adjust the size of the current pane.
Keep {kbd}`Ctrl+b` held down while pressing arrow keys repeatedly to resize continuously and smoothly.

Alternatively, you can use explicit resize commands:

- {kbd}`Ctrl+b` {kbd}`:` then type `resize-pane -D 10` (Down by 10 lines)
- {kbd}`Ctrl+b` {kbd}`:` then type `resize-pane -U 10` (Up by 10 lines)
- {kbd}`Ctrl+b` {kbd}`:` then type `resize-pane -L 10` (Left by 10 columns)
- {kbd}`Ctrl+b` {kbd}`:` then type `resize-pane -R 10` (Right by 10 columns)

Some interactions like resizing panes can be complex, but custom key bindings can be configured to make whatever an administrator's common actions are more comfortable.

**Scrollback mode**:

Scrollback allows you to review previous command output that has scrolled off the screen. tmux maintains a buffer (history) of terminal output.

- {kbd}`Ctrl+b` {kbd}`[` - Enter scrollback mode

Once in scrollback mode, use arrow keys, {kbd}`Page Up`/{kbd}`Page Down`, or vi-style keys ({kbd}`j`/{kbd}`k`) to navigate. Press {kbd}`q` to exit scrollback mode. The default scrollback buffer stores 2000 lines, but this can be increased in the configuration (see the Configuration section).

### Console-based screen sharing

One of tmux's powerful features is the ability to share sessions between multiple users over SSH. This is invaluable for pair programming, training, or troubleshooting.

**Basic session sharing** (same user):

User 1 creates a session:
```bash
tmux new-session -s shared
```

User 2 (logged in as the same user on another terminal/SSH connection) attaches to it:
```bash
tmux attach-session -t shared
```

Both users now see and can provide input to the same terminal session in real-time - any keystrokes from either user are processed by the session.

**Read-only session sharing**:

By default, all users attached to a session have read/write access to the terminal input/output. To allow someone to watch your session without being able to send input (read-only mode), they can attach with the `-r` flag:

User 2 attaches in read-only mode:
```bash
tmux attach-session -t shared -r
```

In read-only mode, User 2 can see all terminal output but cannot type commands or interfere with the session.

**Multi-user session sharing** (different users):

For different users to share a session, you need to create a shared socket:

User 1 creates a session with a shared socket:
```bash
tmux -S /tmp/shared-session new-session -s collaboration
chmod 777 /tmp/shared-session
```

User 2 connects using the shared socket:
```bash
tmux -S /tmp/shared-session attach-session -t collaboration
```

:::{note}
For multi-user sharing, ensure both users have appropriate permissions on the socket file. Consider security implications when sharing sessions between different users.
:::

### Configuration

tmux can be customized through the `~/.tmux.conf` file. The configuration possibilities are extensive and depend on your specific needs. Here are two commonly useful examples:

**Enable mouse support** for easier pane/window navigation and resizing:

```bash
# Enable mouse support
set -g mouse on
```

**Increase scrollback history** to review more command output:

```bash
# Increase scrollback buffer size from default 2000 to 10000 lines
set-option -g history-limit 10000
```

After creating or modifying `~/.tmux.conf`, reload it from within tmux:

```bash
tmux source-file ~/.tmux.conf
```

Or use {kbd}`Ctrl+b` {kbd}`:` and type `source-file ~/.tmux.conf`.

Reloading the configuration preserves all your existing sessions, windows, and panes. The alternative would be to exit and restart tmux, but that would lose your current work environment.

### Scripting and automation

tmux can be scripted to automate the creation of complex session layouts with multiple windows and panes. Scripts can use commands like `new-session`, `split-window`, `new-window`, and `send-keys` to set up your preferred environment automatically. Sessions are identified by name, windows by their index within a session, and panes by their index within a window. For detailed scripting syntax and options, refer to the {manpage}`tmux(1)` manual page.

### tmux plugins

The tmux ecosystem includes a plugin manager called TPM (Tmux Plugin Manager) that extends functionality. Install it from the Ubuntu archive:

```bash
sudo apt install tmux-plugin-manager
```

:::{note}
While tmux plugins can be powerful, be aware that they introduce third-party code and configuration into your system. The same considerations discussed in the [third-party repository usage](https://documentation.ubuntu.com/server/explanation/software/third-party-repository-usage/) documentation apply here - evaluate trustworthiness, security implications, and maintenance status before using plugins, especially in production environments.
:::

Popular plugins include:
- **tmux-resurrect**: Save and restore tmux sessions across system restarts
- **tmux-continuum**: Builds on tmux-resurrect to provide automatic continuous saving of tmux sessions at regular intervals (default every 15 minutes)
- **tmux-yank**: Improved copy/paste functionality

## Other options

### Mosh (mobile shell)

While not a terminal multiplexer itself, Mosh (mobile shell) deserves mention as it complements SSH and terminal multiplexers. Mosh is closer to "ssh + tmux" than just tmux alone. Its primary strength is handling flaky network connections even more gracefully than tmux alone - it maintains connectivity through connection loss, IP address changes (roaming between networks), and even laptop sleep/wake cycles.

If your main interest in terminal multiplexers is protection against disconnects rather than the window/pane management features, Mosh combined with tmux might be the ideal solution. Mosh handles the network resilience while tmux provides session persistence and workspace management.

Install Mosh:
```bash
sudo apt install mosh
```

Connect to a remote server:
```bash
mosh user@remote-server
```

### GNU Screen

GNU Screen is the established terminal multiplexer that has been available for decades and is pre-installed on Ubuntu Server. While it's still functional and widely available, it's generally considered aging technology with development largely stalled. Screen uses similar concepts to tmux but with a different key binding scheme (default prefix {kbd}`Ctrl+a`).

Screen also supports session sharing between users on a system. Users can share a screen session by using the `-x` flag to attach to another user's session (with appropriate permissions), enabling collaborative work or troubleshooting scenarios.

Screen remains useful to know for legacy environments, but for new workflows, tmux is recommended due to its active development, better performance, and more features.

### Byobu

Byobu is a wrapper around tmux (or screen) that provides a more beginner friendly interface with enhanced status notifications and F-key shortcuts.
While Byobu was installed by default on Ubuntu Server up until 25.04 Plucky, it now needs to be installed if you want to use it:

```bash
sudo apt install byobu
```

Byobu uses tmux as its backend if available.

Invoke it with:

```bash
byobu
```

Bring up the configuration menu by pressing {kbd}`F9`:

- Help -- Quick Start Guide
- Toggle status notifications
- Change the escape sequence
- Byobu currently does not launch at login (toggle on)

Byobu provides a menu which displays the Ubuntu release, processor information, memory information, and the time and date. Using the *"Byobu currently does not launch at login (toggle on)"* option will cause Byobu to be executed any time a terminal is opened. Changes made to Byobu are on a per-user basis.

**Scrollback mode** in Byobu: Press {kbd}`F7` to enter scrollback mode, which allows you to navigate past output using vi-like commands:

- {kbd}`h` - Move the cursor left by one character
- {kbd}`j` - Move the cursor down by one line
- {kbd}`k` - Move the cursor up by one line
- {kbd}`l` - Move the cursor right by one character
- {kbd}`0` - Move to the beginning of the current line
- {kbd}`$` - Move to the end of the current line
- {kbd}`G` - Moves to the specified line (defaults to the end of the buffer)
- {kbd}`/` - Search forward
- {kbd}`?` - Search backward
- {kbd}`n` - Moves to the next match, either forward or backward

While Byobu can be helpful for beginners, learning tmux directly provides more flexibility and is more transferable across different systems.
