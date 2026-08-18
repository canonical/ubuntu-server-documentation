---
myst:
  html_meta:
    description: "Reference documentation for migrated tools outlining differences to the former, to guide users of Ubuntu Server on the new implementations."
---

# Migrated tools

The “oxidisation” of Ubuntu (see [Ubuntu Discourse](https://discourse.ubuntu.com/t/carefully-but-purposefully-oxidising-ubuntu/56995)) has changed the providers of a number of packages that are installed by default.
This page provides guidance for Ubuntu Server users on the new implementations

(rust-coreutils)=
## rust-coreutils

uutils is the default coreutils provider as of Ubuntu 25.10. This section lists
helpful resources and tips regarding the migration.

Refer to the [uutils Coreutils Documentation](https://uutils.org/coreutils/docs/index.html) for information about uutils.

### Exceptions per releases

Due to known incompatibilities, some utilities in `rust-coreutils` are still
provided by GNU for the Ubuntu 25.10 and 26.04 releases. Redirected utilities
per release are as follows:

| Release | Utilities still provided by GNU |
|---|---|
| **Ubuntu 25.10** ([reference][ubuntu-25.10-reference]) | `chmod`, `chown`, `cp`, `df`, `mv`, `rm`, `true` |
| **Ubuntu 26.04** ([reference][ubuntu-26.04-reference]) | `cp`, `df`, `mv`, `rm`, `true` |
| **Ubuntu 26.10 and later** | — |

[ubuntu-25.10-reference]: https://git.launchpad.net/ubuntu/+source/coreutils-from/tree/debian/coreutils-from-uutils.links?h=ubuntu/questing-devel
[ubuntu-26.04-reference]: https://git.launchpad.net/ubuntu/+source/coreutils-from/tree/debian/coreutils-from-uutils.links?h=ubuntu/resolute-devel

### Changing provider

The installed `coreutils-from-*` package determines which coreutils provider is
used on the system.

**To switch to GNU coreutils:**

```shell
sudo apt install coreutils-from-gnu coreutils-from-uutils- --allow-remove-essential
```

**To switch to back to rust-coreutils:**

```shell
sudo apt install coreutils-from-uutils coreutils-from-gnu- --allow-remove-essential
```

(sudo-rs)=
## sudo-rs

This section serves as a reference for the key differences between `sudo.ws` and `sudo-rs`.

Note: Both projects are under active development, so it is not possible to maintain a fully up-to-date list of differences.
This is a list of major differences as of the Ubuntu 25.10 and 26.04 releases, to help users upgrading to those.

For the most accurate and current information, refer to
`sudo-rs --help` for a list of supported options in your installed version.
Refer to `man sudoers-rs` for the `/etc/sudoers` configuration options supported by `sudo-rs`.

### Differences

1. Start with the official documentation from the `sudo-rs` project.

   * [differences-from-original-sudo](https://github.com/trifectatechfoundation/sudo-rs#differences-from-original-sudo)
   * [aim-of-the-project](https://github.com/trifectatechfoundation/sudo-rs?tab=readme-ov-file#aim-of-the-project)

2. `sudo-rs` prompt.

   This is the most common error users encounter when using Expect-based automation. The error often is a TIMEOUT because Expect is pattern matching on the `sudo.ws` prompt.

   `sudo.ws` prompt for password says `[sudo] password for <USERNAME>`, whereas `sudo-rs` prompt says `[sudo: authenticate] <METHOD>:`. `sudo-rs` transparently prints whatever PAM says such as `Password:`, `PIN:`, etc.

   You can use `--prompt ""` in Expect-based scripts to skip the regex-based matching of the prompt.

   [See more information](https://github.com/trifectatechfoundation/sudo-rs/issues/1242)

3. I/O logging and `sudoreplay` is not supported. The discontinued programs are `sudo_logsrvd`, `sudo_sendlog`, and `sudoreplay`.

4. There is no `sudoers.ldap`. You need to use [LDAP authentication via PAM](https://github.com/trifectatechfoundation/sudo-rs/issues/445).

5. The `sudo-rs` team maintains the list of [CLI flags parity](https://github.com/trifectatechfoundation/sudo-rs/issues/129) with `sudo.ws`
