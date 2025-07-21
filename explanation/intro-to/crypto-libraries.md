(introduction-to-crypto-libraries)=
# Introduction to cryptographic libraries 

When choosing a crypto library, the following aspects should be considered to maintain security and compliance. Typically, you will want to answer questions such as: How can we ensure legacy crypto systems with known vulnerabilities are not being used? How can we enforce minimum key size requirements? And what criteria should we use to accept X.509 certificates when connecting to remote servers?

However, the cryptographic library landscape is vast and complex, and there are many crypto libraries available on an Ubuntu system. When an application developer chooses a crypto library, they will consider many aspects, such as:

  * Technical requirements
  * Language bindings
  * License
  * Community
  * Ease of use
  * General availability
  * Upstream maintenance

Among the most popular and widely used libraries and frameworks are:

  * OpenSSL
  * {term}`GnuTLS`
  * NSS
  * GnuPG
  * {term}`gcrypt`

Each one of these has its own implementation details, API, behavior, configuration file, and syntax.

## Determining which libraries are being used by an application

Ultimately, the only reliable way to determine how an application uses cryptography is by reading its documentation or inspecting its source code. But even then, you may discover that the code is not available and sometimes the documentation might lack this information. If you are having problems finding answers to your crypto-related questions, there are some practical checks that can be made.

To find out what libraries are being used, one generally needs to check all of the installed crypto implementations and their respective configurations. To make things even more complicated, sometimes an application implements its own crypto, without using anything external.

If you are having problems finding answers to your crypto-related questions, there are some practical checks that can be made.


### Follow dynamic links

This is the most common way, and very easy to spot via package dependencies and helper tools. A detailed example of this approach to determining crypto is discussed later in this page.
 
### Check static linking

This is harder, as there is no dependency information in the binary package, and this usually requires inspection of the source package to see build dependencies. A detailed example of this approach is shown later in this page.

### Look at the plugins

The main binary of an application can not depend directly on a crypto library, but it could load dynamic plugins which do. Usually these would be packaged separately, and then we fall under the dynamic or static linking cases above. Note that via such a plugin mechanism, an application could depend on multiple external cryptographic libraries.

### Examine the execution of external binaries

The application could just plain call external binaries at runtime for its cryptographic operations, like calling out to `openssl` or `gnupg` to encrypt/decrypt data. This will hopefully be expressed in the dependencies of the package. If it's not, then it's a bug that should be reported.

### Indirect use of libraries or executables

The application could be using a third party library or executable which in turn could fall into any of the above categories.

### Check documentation more carefully

Read the application documentation again. It might have crypto options directly in its own configuration files, or point at specific crypto configuration files installed on the system. This may also clarify whether the application uses external crypto libraries or it has its own implementation of crypto.

## Detailed examples of how to locate crypto libraries

### Use dpkg to check package dependencies

Since package dependencies are a good way to check what is needed at runtime by the application, you can find out which package owns what file with the `dpkg -S` command. For example:

```bash
$ dpkg -S /usr/bin/lynx
lynx: /usr/bin/lynx
```

Now that you have the package name, check the package's dependencies. You should also look for `Recommends`, as they are installed by default. Using the current example, we can now do the following:

```bash
$ dpkg -s lynx | grep -E "^(Depends|Recommends)"
Depends: libbsd0 (>= 0.0), libbz2-1.0, libc6 (>= 2.34), libgnutls30 (>= 3.7.0), libidn2-0 (>= 2.0.0), libncursesw6 (>= 6), libtinfo6 (>= 6), zlib1g (>= 1:1.1.4), lynx-common
Recommends: mime-support
```

Now we can see that `lynx` links with `libgnutls30`, which answers our question: `lynx` uses the GnuTLS library for its cryptography operations.

### Using ldd to list dynamic libraries

If a dynamic library is needed by an application, it should always be correctly identified in the list of application package dependencies. When that is not the case, or you need to identify what is needed by some plugin that is not part of the package, you can use some system tools to help identify the dependencies.

In this situation, you can use the `ldd` tool, which is installed in all Ubuntu systems. It lists all the dynamic libraries needed by the given binary, including dependencies of dependencies, i.e. the command is recursive. Going back to the `lynx` example:

```bash
$ ldd /usr/bin/lynx
    linux-vdso.so.1 (0x00007ffffd2df000)
    libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007feb69d77000)
    libbz2.so.1.0 => /lib/x86_64-linux-gnu/libbz2.so.1.0 (0x00007feb69d64000)
    libidn2.so.0 => /lib/x86_64-linux-gnu/libidn2.so.0 (0x00007feb69d43000)
    libncursesw.so.6 => /lib/x86_64-linux-gnu/libncursesw.so.6 (0x00007feb69d07000)
    libtinfo.so.6 => /lib/x86_64-linux-gnu/libtinfo.so.6 (0x00007feb69cd5000)
    libgnutls.so.30 => /lib/x86_64-linux-gnu/libgnutls.so.30 (0x00007feb69aea000)
    libbsd.so.0 => /lib/x86_64-linux-gnu/libbsd.so.0 (0x00007feb69ad0000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007feb698a8000)
    libunistring.so.2 => /lib/x86_64-linux-gnu/libunistring.so.2 (0x00007feb696fe000)
    libp11-kit.so.0 => /lib/x86_64-linux-gnu/libp11-kit.so.0 (0x00007feb695c3000)
    libtasn1.so.6 => /lib/x86_64-linux-gnu/libtasn1.so.6 (0x00007feb695ab000)
    libnettle.so.8 => /lib/x86_64-linux-gnu/libnettle.so.8 (0x00007feb69565000)
    libhogweed.so.6 => /lib/x86_64-linux-gnu/libhogweed.so.6 (0x00007feb6951b000)
    libgmp.so.10 => /lib/x86_64-linux-gnu/libgmp.so.10 (0x00007feb69499000)
    /lib64/ld-linux-x86-64.so.2 (0x00007feb69fe6000)
    libmd.so.0 => /lib/x86_64-linux-gnu/libmd.so.0 (0x00007feb6948c000)
    libffi.so.8 => /lib/x86_64-linux-gnu/libffi.so.8 (0x00007feb6947f000)
```

We again see the GnuTLS library (via `libgnutls.so.30`) in the list, and can reach the same conclusion.

Another way to check for such dependencies (without recursion) is via `objdump`. You may need to install it with the `binutils` package, as it's not mandatory.
The way to use it is to grep for the `NEEDED` string:

```bash
$ objdump -x /usr/bin/lynx|grep NEEDED
  NEEDED               libz.so.1
  NEEDED               libbz2.so.1.0
  NEEDED               libidn2.so.0
  NEEDED               libncursesw.so.6
  NEEDED               libtinfo.so.6
  NEEDED               libgnutls.so.30
  NEEDED               libbsd.so.0
  NEEDED               libc.so.6
```

Finally, if you want to see the dependency *tree*, you can use `lddtree` from the `pax-utils` package:

```bash
$ lddtree /usr/bin/lynx
lynx => /usr/bin/lynx (interpreter => /lib64/ld-linux-x86-64.so.2)
    libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1
    libbz2.so.1.0 => /lib/x86_64-linux-gnu/libbz2.so.1.0
    libidn2.so.0 => /lib/x86_64-linux-gnu/libidn2.so.0
        libunistring.so.2 => /lib/x86_64-linux-gnu/libunistring.so.2
    libncursesw.so.6 => /lib/x86_64-linux-gnu/libncursesw.so.6
    libtinfo.so.6 => /lib/x86_64-linux-gnu/libtinfo.so.6
    libgnutls.so.30 => /lib/x86_64-linux-gnu/libgnutls.so.30
        libp11-kit.so.0 => /lib/x86_64-linux-gnu/libp11-kit.so.0
            libffi.so.8 => /lib/x86_64-linux-gnu/libffi.so.8
        libtasn1.so.6 => /lib/x86_64-linux-gnu/libtasn1.so.6
        libnettle.so.8 => /lib/x86_64-linux-gnu/libnettle.so.8
        libhogweed.so.6 => /lib/x86_64-linux-gnu/libhogweed.so.6
        libgmp.so.10 => /lib/x86_64-linux-gnu/libgmp.so.10
        ld-linux-x86-64.so.2 => /lib64/ld-linux-x86-64.so.2
    libbsd.so.0 => /lib/x86_64-linux-gnu/libbsd.so.0
        libmd.so.0 => /lib/x86_64-linux-gnu/libmd.so.0
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
```

### Check package headers for static linking

Identifying which libraries were used in a static build is a bit more involved. There are two ways, and they are complementary most of the time:

* look for the `Built-Using` header in the binary package
* inspect the `Build-Depends` header in the source package


For example, let's try to discover which crypto libraries, if any, the `rclone` tool uses. First, let's try the packaging dependencies:

```bash
$ dpkg -s rclone | grep -E "^(Depends|Recommends)"
Depends: libc6 (>= 2.34)
```

Uh, that's a short list. But `rclone` definitely supports encryption, so what is going on? Turns out this is a tool written in the Go language, and that uses static linking of libraries. So let's try to inspect the package data more carefully, and this time look for the `Built-Using` header:

```bash
$ dpkg -s rclone | grep Built-Using
Built-Using: go-md2man-v2 (= 2.0.1+ds1-1), golang-1.18 (= 1.18-1ubuntu1), golang-bazil-fuse (= 0.0~git20160811.0.371fbbd-3), ...
```

Ok, this time we have a lot of information (truncated above for brevity, since it's all in one very long line). If we look at the full output carefully, we can see that `rclone` was built statically using the `golang-go.crypto` package, and documentation about that package and its crypto implementations is what we should look for.

If the `Built-Using` header was not there, or didn't yield any clues, we could try one more step and look for the build dependencies. These can be found in the `debian/control` file of the source package. In the case of `rclone` for Ubuntu Jammy, that can be seen at https://git.launchpad.net/ubuntu/+source/rclone/tree/debian/control?h=ubuntu/jammy-devel#n7, and a quick look at the `Build-Depends` list shows us the `golang-golang-x-crypto-dev` build dependency, whose source package is `golang-go.crypto` as expected:

```bash
$ apt-cache show golang-golang-x-crypto-dev | grep ^Source:
Source: golang-go.crypto
```

```{note}
If there is no `Source:` line, then it means the name of the source package is the same as the binary package that was queried.
```

## What's next?

Once you have uncovered which library your application is using, the following guides may help you to understand the associated configuration files and what options you have available (including some handy examples).

* {ref}`OpenSSL guide <openssl>` 
* {ref}`GnuTLS guide <gnutls>`
* {ref}`Troubleshooting TLS/SSL <troubleshooting-tls-ssl>`
