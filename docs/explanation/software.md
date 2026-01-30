---
myst:
  html_meta:
    description: Understanding package management in Ubuntu Server including APT, third-party repositories, and software update best practices.
---

(explanation-managing-software)=
# Managing software

This section explains how software is managed on Ubuntu Server and outlines recommended best practices.

## Package sources

* {ref}`Third party repository usage <third-party-repository-usage>` gives some best practices and guidance if you need to use Third Party software

```{toctree}
:hidden:

Third party repository usage <software/third-party-repository-usage>
```

## Configuration

There are many different ways to configure the software on your machine.

* {ref}`Changing package files <changing-package-files>`
* {ref}`Configuration managers <config-managers>`

```{toctree}
:hidden:

Changing package files <software/changing-package-files>
Configuration managers <software/config-managers>
```

## Updates

* {ref}`About apt upgrade and phased updates <about-apt-upgrade-and-phased-updates>` explains phased updates and why you may see related messages.
* {ref}`Advance testing of updates in best practice server deployments <advance-testing-of-updates-in-best-practice-server-deployments>` helps you to avoid updates being rolled out on your production systems without them being tested first.

```{toctree}
:hidden:

About apt upgrade and phased updates <software/about-apt-upgrade-and-phased-updates>
Advance testing of updates in best practice server deployments <software/advance-testing-of-updates-in-best-practice-server-deployments>
```

## See also

* How-to: {ref}`how-to-managing-software`
