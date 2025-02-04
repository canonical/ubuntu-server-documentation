(introduction-to-ebpf)=
# Introduction to eBPF

[eBPF](https://ebpf.io/) is a powerful tool for server and system
administrators, often described as a lightweight, sandboxed virtual
machine within the kernel. It is commonly used for performance monitoring,
security, and network traffic processing without the need to modify or rebuild
the kernel.

Since it runs in the kernel space, there is no need for context-switching,
making it very fast compared to solutions implemented in user-space. It also
has access to the kernel data structures, providing more capabilities than
tools limited to the interfaces exposed to user-space.

BPF, which stands for "Berkeley Packet Filter", was originally designed to
perform network packet filtering. Over time, its capabilities were extended far
beyond that scope -- this is reflected in the current name, *extended Berkeley
Packet Filter* (eBPF). It now uses more registers, supports 64-bit registers,
data stores (Maps), and more.  Such enhancements allowed eBPF to be decoupled
from the kernel networking subsystem and transformed it into a tool with
broader scope, capable of enhancing not only the networking experience, but
also tracing, profiling, observability, security, etc.  The terms eBPF and BPF
are now used interchangeably, but refer to eBPF -- which has become a
standalone term that no longer refers to *extended Berkeley Packet Filter* due
to its aforementioned broader scope.

## How it works

User-space applications can load eBPF programs into the kernel as eBPF
bytecode. Although you could write eBPF programs in bytecode, there are several
tools which provide abstraction layers on top of eBPF so you do not need to
write bytecode manually. These tools will then generate the bytecode which will
in turn be loaded into the kernel.

Once the eBPF program is loaded, it is then verified by the kernel before it
can run. These checks include:

* verifying if the eBPF program halts and will never get stuck in a loop,
* verifying that the program will not crash by checking the registers and stack
  state validity throughout the program, and
* ensuring the process loading the eBPF program has all the capabilities
  required by the eBPF program to run.

After the verification step, the bytecode is Just-In-Time (JIT) compiled into
machine-code to optimize the program's execution.

## eBPF in Ubuntu Server

In Ubuntu, you can leverage tools like the BPF Compiler Collection (BCC) or
`bpftrace` to identify bottlenecks, investigate performance degradation, trace
specific function calls, or create custom monitoring tools to collect data on
specific kernel or user-space processes without disrupting running services.

Since Ubuntu 24.04, `bpftrace` and `bpfcc-tools` (BCC) are available in every
Ubuntu Server installation by default as part of our efforts to [enhance the
application developer's and sysadmin's experience in
Ubuntu](https://discourse.ubuntu.com/t/spec-include-performance-tooling-in-ubuntu/43134).

`bpftrace` and `bpfcc-tools` install a range of tools with a variety of
different functionalities. Apart from the `bpftrace` tool itself, you can fetch
a comprehensive list of these tools with the following command:

```bash
$ dpkg -L bpftrace bpfcc-tools | grep -E '/s?bin/.*$' | xargs -n1 basename
```

Most of the tools listed above are quite well documented. Their manpages
usually include good examples you can try immediately. The tools ending in
`.bt` are installed by `bpftrace` and refer to `bpftrace` scripts (they are
text files, hence, you could read them to understand how they are achieving
specific tasks). The ones ending in `-bpfcc` are BCC tools (from `bpfcc`)
written in Python (you can also inspect those as you would inspect the `.bt`
files).

These `bpftrace` scripts are often a great start on how something complex can
be achieved in simple ways. The `-bpfcc` variants are often a bit more
advanced, often providing more options and customizations.

You will also find several text files describing use-case examples and the
output for `bpftrace` tools in
`/usr/share/doc/bpftrace/examples/` and for `bpfcc-tools` in
`/usr/share/doc/bpfcc-tools/examples/`.

For instance,

```bash
# bashreadline.bt
```

will print bash commands for all running bash shells in your system. Note that
the information you can get via eBPF is always potentially confidential, so you
need to run any of it as root.  You may notice that there is also a
`bashreadline-bpfcc` tool available from `bpfcc-tools`. Both of them provide
similar features. The former is implemented in python with BCC while the latter
is a `bpftrace` script, as described above. You will see that many of these
tools have both a `-bpfcc` and a `.bt` version. Do read their manpages (and
perhaps the scripts) to choose which suits you best.

## Example - What commands are executed?

A trivial, yet powerful command of these tools is `execsnoop-bpfcc` which
allows one to answer common questions that should not be common - like "what
other programs this action eventually calling?". It makes it rather easy to
identify if for example a program calls another tool too often or something
that you'd not expect. It has become a common helper to ensure one understands
well what happens on execution of a maintainer script in a .deb package in
Ubuntu.

For that you'd run `execsnoop-bpfcc` with the following arguments:

* `-Uu root` - to reduce the noisy output only to things done in root context (like here the package install)
* `-T` - to get time info along the log

```bash
# In one console run:
$ sudo execsnoop-bpfcc -Uu root -T

# In another trigger what you want to watch for
$ sudo apt install --reinstall vim-nox

# Execsnoop in the first console will now report probably more than you expected:
TIME     UID   PCOMM            PID     PPID    RET ARGS
10:58:07 1000  sudo             1323101 1322857   0 /usr/bin/sudo apt install --reinstall vim-nox
10:58:10 0     apt              1323107 1323106   0 /usr/bin/apt install --reinstall vim-nox
10:58:10 0     dpkg             1323108 1323107   0 /usr/bin/dpkg --print-foreign-architectures
...
10:58:12 0     sh               1323134 1323107   0 /bin/sh -c /usr/sbin/dpkg-preconfigure --apt || true
...
10:58:13 0     tar              1323155 1323152   0 /usr/bin/tar -x -f  --warning=no-timestamp
10:58:14 0     vim-nox.prerm    1323157 1323150   0 /var/lib/dpkg/info/vim-nox.prerm upgrade 2:9.1.0016-1ubuntu7.3
10:58:14 0     dpkg-deb         1323158 1323150   0 /usr/bin/dpkg-deb --fsys-tarfile /var/cache/apt/archives/vim-nox_2%3a9.1.0016-1ubuntu7.3_amd64.deb
...
10:58:14 0     update-alternat  1323171 1323163   0 /usr/bin/update-alternatives --install /usr/bin/vimdiff vimdiff /usr/bin/vim.nox 40
...
10:58:17 0     snap             1323218 1323217   0 /usr/bin/snap advise-snap --from-apt
10:58:17 1000  git              1323224 1323223   0 /usr/bin/git rev-parse --abbrev-ref HEAD
10:58:17 1000  git              1323226 1323225   0 /usr/bin/git status --porcelain
10:58:17 1000  vte-urlencode-c  1323227 1322857   0 /usr/libexec/vte-urlencode-cwd
```

## You can modify it to your needs

Let us look at another practical application of eBPF. This time meant to show
another use-case, but also evolve it into more by modifying it.

### Which files is my QEMU loading?

Let’s say you want to verify which binary files are
loaded with a particular command line of QEMU. That is a truly complex program
and sometimes it can be hard to make the connection from a command line to the
files used from /usr/share/qemu. This is already hard to answer when you define
the QEMU command line, but even more when more useful layers of abstraction are
used like libvirt or LXD or even things on top like OpenStack.

You could definitely use `strace` to do so, but that would add quite some
overhead to the investigation process (since `strace` uses `ptrace`, and context
switching may be required).
Furthermore, if you would want to generally monitor a system for this,
especially on a host running many VMs, `strace` quickly reaches its limits.

Instead, you can use `opensnoop` to trace `open()` syscalls. We use
`opensnoop-bpfcc` to have more parameters to tune it to our needs. The example
will use the following arguments:

* `--full-path` - Show full path for open calls using a relative path.
* `--name qemu-system-x86` - only care about files opened by QEMU; The mindful
  reader will wonder why this isn't qemu-system-x86_64, but you'd see in
  unfiltered output of opensnoop that it is length limited, so only the shorter
  qemu-system-x86 can be used.

```bash
# This will collect a log of files opened by QEMU
$ sudo /usr/sbin/opensnoop-bpfcc --full-path --name qemu-system-x86
#
# If now you in another console or anyone on this system in general runs QEMU,
# this would log the files opened
#
# For example calling LXD for an ephemeral VM
$ lxc launch ubuntu-daily:n n-vm-test --ephemeral --vm
#
# Will in opensnoop deliver a barrage of files opened
1308728 qemu-system-x86    -1   2 PID    COMM               FD ERR PATH
/snap/lxd/current/zfs-2.2/lib/glibc-hwcaps/x86-64-v3/libpixman-1.so.0
1308728 qemu-system-x86    -1   2 /snap/lxd/current/zfs-2.2/lib/glibc-hwcaps/x86-64-v2/libpixman-1.so.0
1308728 qemu-system-x86    -1   2 /snap/lxd/current/zfs-2.2/lib/tls/haswell/x86_64/libpixman-1.so.0
...
1313104 qemu-system-x86    58   0 /sys/dev/block/230:16/queue/zoned
1313104 qemu-system-x86    20   0 /dev/fd/4
```

Of course the QEMU process opens plenty of things: shared libraries, config
files, entries in `/{sys,dev,proc}`, and much more. But here we can see them all
as they happen across the whole system.

### But I'm only interested in a particular kind of file

Imagine you only wanted to verify which `.bin` files this is loading. Of course, 
we could just use `grep` on the output, but this whole section is about showing
eBPF examples to get you started. So here we make the simplest change --
modifying the python wrapper around the tracing eBPF code.
Once you understand how to do this, you can go further in adapting them to your
own needs by delving into the eBPF code itself, and from there to create your
very own eBPF solutions from scratch.

So while `opensnoop-bpfcc` as of right now has no option to filter on the file
names, it could ...

```bash
$ sudo cp /usr/sbin/opensnoop-bpfcc /usr/sbin/opensnoop-bpfcc.new
$ sudo vim /usr/sbin/opensnoop-bpfcc.new
...
$ diff -Naur /usr/sbin/opensnoop-bpfcc /usr/sbin/opensnoop-bpfcc.new
--- /usr/sbin/opensnoop-bpfcc	2024-11-12 09:15:17.172939237 +0100
+++ /usr/sbin/opensnoop-bpfcc.new	2024-11-12 09:31:48.973939968 +0100
@@ -40,6 +40,7 @@
     ./opensnoop -u 1000                # only trace UID 1000
     ./opensnoop -d 10                  # trace for 10 seconds only
     ./opensnoop -n main                # only print process names containing "main"
+    ./opensnoop -c path                # only print paths containing "fname"
     ./opensnoop -e                     # show extended fields
     ./opensnoop -f O_WRONLY -f O_RDWR  # only print calls for writing
     ./opensnoop -F                     # show full path for an open file with relative path
@@ -71,6 +72,9 @@
 parser.add_argument("-n", "--name",
     type=ArgString,
     help="only print process names containing this name")
+parser.add_argument("-c", "--contains",
+    type=ArgString,
+    help="only print paths containing this string (implies --full-path)")
 parser.add_argument("--ebpf", action="store_true",
     help=argparse.SUPPRESS)
 parser.add_argument("-e", "--extended_fields", action="store_true",
@@ -83,6 +87,8 @@
     help="size of the perf ring buffer "
         "(must be a power of two number of pages and defaults to 64)")
 args = parser.parse_args()
+if args.contains is not None:
+    args.full_path = True
 debug = 0
 if args.duration:
     args.duration = timedelta(seconds=int(args.duration))
@@ -440,6 +446,12 @@
         if args.name and bytes(args.name) not in event.comm:
             skip = True
 
+        paths = entries[event.id]
+        paths.reverse()
+        entire_path = os.path.join(*paths)
+        if args.contains and bytes(args.contains) not in entire_path:
+            skip = True
+
         if not skip:
             if args.timestamp:
                 delta = event.ts - initial_ts
@@ -458,9 +470,7 @@
             if not args.full_path:
                 printb(b"%s" % event.name)
             else:
-                paths = entries[event.id]
-                paths.reverse()
-                printb(b"%s" % os.path.join(*paths))
+                printb(b"%s" % entire_path)
 
         if args.full_path:
             try:
```

Running the modified version now allows to probe for specific file names, like
all the .bin files:

```bash
$ sudo /usr/sbin/opensnoop-bpfcc.new --contains '.bin' --name qemu-system-x86
PID     COMM               FD ERR PATH
1316661 qemu-system-x86    21   0 /snap/lxd/current/share/qemu//kvmvapic.bin
1316661 qemu-system-x86    39   0 /snap/lxd/current/share/qemu//vgabios-virtio.bin
1316661 qemu-system-x86    39   0 /snap/lxd/current/share/qemu//vgabios-virtio.bin
```

### Use it elsewhere, the limit is your imagination

And just like with all the other tools and examples, the limit is your
imagination. Wanted to know which files in `/etc` your complex intertwined
apache config is really loading?

```bash
$ sudo /usr/sbin/opensnoop-bpfcc.new --name 'apache2' --contains '/etc'
PID     COMM               FD ERR PATH
1319357 apache2             3   0 /etc/apache2/apache2.conf
1319357 apache2             4   0 /etc/apache2/mods-enabled
1319357 apache2             4   0 /etc/apache2/mods-enabled/access_compat.load
...
1319357 apache2             4   0 /etc/apache2/ports.conf
1319357 apache2             4   0 /etc/apache2/conf-enabled
1319357 apache2             4   0 /etc/apache2/conf-enabled/charset.conf
1319357 apache2             4   0 /etc/apache2/conf-enabled/localized-error-pages.conf
...
1319357 apache2             4   0 /etc/apache2/sites-enabled/000-default.conf
```

## Limitations

You might have realized reading the example code change above that - just like
the existing `--name` option - this is filtering on the reporting side, not on
the event generation.  Which brings us to another topic that you might have
seen in your recreation of these examples, being aware and understanding
messages like:

```text
Possibly lost 84 samples
```

eBPF programs produce events on a ring buffer, if that is exceeding the pace
the userspace process can consume them it will lose some events (overwritten
since it's a ring).  The "Possibly lost .. samples" message is a hint about
this happening.  This is conceptually the same for almost all kernel tracing
facilities, they are not allowed to slow down the kernel, you can't really say
"wait until I've consumed".  Most of the time this is fine, but advanced users
might need to aggregate on the eBPF side to reduce what needs to be picked up by
userspace.  And despite having lower overhead, eBPF tools still need to find
their balance between buffering, dropping events and consuming CPU.  See the
[same discussion](https://github.com/iovisor/bcc/issues/1033) in the example
tools shown above.

## Conclusion

eBPF offers a vast array of options to monitor, debug, and secure your systems
directly in kernel-space (i.e., fast and omniscient), with no need to disrupt
running services. It is an invaluable tool for system administrators and
software engineers.

## References

* [Introduction to eBPF video, given at the as part of The Ubuntu summit
  2024](https://www.youtube.com/live/byPpJW5l6pg?t=30314s), eventually
  presenting an eBPF based framework for Kubernetes called Inspector Gadget.
* For a deeper introduction into eBPF concepts consider reading [what is
  eBPF](https://ebpf.io/what-is-ebpf/) by the eBPF community.
* For a complete documentation on eBPF, its internals and interfaces, please
  check the [upstream documentation](https://docs.kernel.org/bpf/).
* The eBPF community also has a [list of eBPF based
  solutions](https://ebpf.io/applications/), many of which are related to the
  Kubernetes ecosystem.
