---
myst:
  html_meta:
    description: "Reference page for Ubuntu’s Rust-based replacements for sudo and GNU coreutils, highlighting differences, release-specific exceptions, and important changes."
---

# System utility replacements

Starting with Ubuntu 25.10, the "oxidization" of Ubuntu (see [Ubuntu
Discourse](https://discourse.ubuntu.com/t/carefully-but-purposefully-oxidising-ubuntu/56995))
changed the providers of the system utilities `coreutils` and `sudo` to new
Rust-based implementations. Previous Ubuntu releases retain their existing
default providers.

- **`coreutils`**: changed from [GNU Coreutils](https://www.gnu.org/software/coreutils/manual) to [uutils Coreutils](https://uutils.org/coreutils/docs)
- **`sudo`**: changed from [`sudo.ws`](https://www.sudo.ws/docs/man/sudo.man/) to [`sudo-rs`](https://github.com/trifectatechfoundation/sudo-rs)

For most users, no changes are required for normal usage. The new Rust-based
implementations are intended to be drop-in replacements for the existing
utilities, so existing commands and usage should generally continue to work
as before. This page describes known differences, incompatibilities, and other
considerations that may affect specific use cases.

GNU Coreutils and `sudo.ws` continue to receive maintenance in Ubuntu releases
where they are the default providers. In newer releases where the Rust-based
implementations are the default, **GNU Coreutils and sudo.ws remain available
as providers**, while the Rust-based implementations are the primary ones
going forward.

(rust-coreutils)=
## rust-coreutils

This section lists helpful resources and tips regarding the new Rust-based
implementation of `coreutils`, provided by the `rust-coreutils` package.
The `rust-coreutils` package is available for installation on Ubuntu 24.04 LTS
and later.

Refer to the [uutils Coreutils Documentation](https://uutils.org/coreutils/docs/index.html) for information about its usage.

### Release-specific exceptions

The `rust-coreutils` package provides implementations of all `coreutils`
utilities, which can also be invoked through its `coreutils` multi-call binary.
However, starting with Ubuntu 25.10, the `coreutils-from-<provider>` packages
control which implementation is used by the standard utility commands such as
`cp` and `chmod`.

Due to known incompatibilities, `coreutils-from-uutils` configures some
commands to continue using GNU Coreutils in Ubuntu 25.10 and Ubuntu 26.04 LTS.

| Release | Utilities configured to use GNU Coreutils |
|---|---|
| **Ubuntu 24.04 LTS and earlier** | **All** |
| **Ubuntu 25.10** | `chmod`, `chown`, `cp`, `df`, `mv`, `rm`, `true` |
| **Ubuntu 26.04 LTS** | `cp`, `df`, `mv`, `rm`, `true` |
| **Ubuntu 26.10 and later** | **None** |

:::{note}
Although the `rust-coreutils` package is available in Ubuntu 24.04 LTS, it
cannot be configured as the default `coreutils`. The
`coreutils-from-<provider>` packages required to switch the provider are only
available starting with Ubuntu 25.10.
:::

### Switching the coreutils provider (Ubuntu 25.10 and later)

The `coreutils-from-<provider>` packages are available starting with Ubuntu
25.10 and determine which coreutils provider is used on the system. By
default, the `coreutils-from-uutils` package is installed.

When switching providers, the `--allow-remove-essential` option is required
because `apt` sees the currently active `coreutils` package as `Essential`.
Switching providers therefore requires explicitly allowing `apt` to remove that
package.

:::{note}
`update-alternatives` is not currently suitable for switching between GNU
Coreutils and uutils Coreutils, as alternatives are not safe for `Essential`
packages. Instead, use the `coreutils-from-<provider>` packages to switch
providers.
:::

**To switch to GNU Coreutils:**

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install coreutils-from-gnu coreutils-from-uutils- --allow-remove-essential
```

**To switch back to `rust-coreutils`:**

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install coreutils-from-uutils coreutils-from-gnu- --allow-remove-essential
```

### `build-essential` dependency

The `build-essential` package has a direct dependency on the package providing
the default `coreutils` implementation. This ensures that the coreutils
implementation used in the Ubuntu archive build environment is consistent.

In Ubuntu 25.10 and later, this dependency resolves to `coreutils-from-uutils`.
In earlier releases, it resolves to the package providing GNU Coreutils.
This dependency is intentionally specific to `build-essential`: allowing either
GNU Coreutils or uutils Coreutils could result in build failures or
inconsistent build behavior due to differences between the two implementations.

Some packages also declare a dependency on `build-essential` without requiring
its full set of build tools. This can result in an indirect dependency on
`coreutils-from-uutils` in Ubuntu 25.10 and later.

:::{note}
As a result, these packages may currently conflict with `coreutils-from-gnu`
when switching the coreutils provider.
:::

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
