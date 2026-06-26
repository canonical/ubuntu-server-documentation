---
myst:
  html_meta:
    description: Understand QEMU/KVM live migration and machine types on Ubuntu, the supported migration paths, and how to upgrade the machine type of an existing guest.
---

(live-migration)=
# Live migration with libvirt/QEMU

Live migration has been available for quite some time. Despite the complexities of
testing live migration across a variety of releases, machine types, and
architectures, live migration continues to get better. Yet it still sometimes causes
issues, especially when migrating between different host versions. For example, in the
past we ran into issues like [bug 1291321](https://bugs.launchpad.net/ubuntu/+source/libvirt/+bug/1291321) related to that - even worse, a few of them even seemed to resurface.

The purpose of this page is to focus on the quality and user
experience of live migration in Ubuntu. There is a good summary of the general
steps taken during a migration at the [Red Hat live migration overview](https://developers.redhat.com/blog/2015/03/24/live-migrating-qemu-kvm-virtual-machines/) if you want to refresh your knowledge (especially the chapters
on `vmstate`, updating devices, and their subsections).

Live migration with QEMU and libvirt is the process of moving a running virtual machine from one physical server to another with near-zero downtime.

During this process:

- QEMU acts as the engine, actively streaming the VM's live memory (RAM) and CPU state across the network. It can work without libvirt. A live migration can be triggered using QEMU Monitor Protocol (QMP).

- libvirt acts as the manager, coordinating the setup, security, and handoff between the two physical servers so the guest operating system and its applications keep running without interruption.

Migration can happen across hosts with different hardware and software versions (for example, different QEMU versions). Two mechanisms make this possible:

- **Versioned machine types**, which keep the guest's virtual hardware layout stable across QEMU versions.
- A **CPU model baseline**, which exposes only the CPU features common to both hosts.

## Machine types

The QEMU machine type defines the exact virtual hardware blueprint (chipset, PCI slots, ACPI tables) of a virtual machine. For a live migration to succeed, both the source and destination servers must use the exact same machine type version (e.g., pc-q35-8.2). If they don't match, the migration will fail, or worse, the VM will crash immediately after the handoff.
Why the Machine Type Matters

When you live-migrate a VM, you are taking a snapshot of a running system's RAM and CPU state and sending it over the wire. The destination host must have a virtual hardware environment that matches that state down to the very last byte.

When you upgrade the QEMU software on your physical servers, the default machine type usually changes to the newest version. If Server A is upgraded to a newer QEMU version and Server B is still running an older version, Server B will not understand the newer default machine type. The Solution (Versioned Machine Types): QEMU includes backwards-compatible machine types for this exact reason. Even if Server A is running a brand new version of QEMU, it can still launch a VM using an older machine type (e.g., pc-q35-6.0) so that it can safely migrate back and forth to Server B.


## Use cases

There are two use cases that drive the need. First, we'd like to support users
who have deployed VMs on Ubuntu LTSes to be able to live migrate their VMs to the
next LTS. This means that a QEMU VM launched with a machine of `pc-1.0` should
be the same on an LTS and on LTS-next. In the past, `pc-XX` upstream types
changed and still have no requirement to remain stable between QEMU releases ([bug 1291321](https://bugs.launchpad.net/ubuntu/+source/libvirt/+bug/1291321)), so we could not rely upon unversioned upstream machine names. Therefore, in the past
we introduced a downstream release name ([bug 1294823](https://bugs.launchpad.net/ubuntu/+source/qemu/+bug/1294823)). Unlike other downstreams ([Red Hat bug 895959](https://bugzilla.redhat.com/show_bug.cgi?id=895959)) we did so on top of the upstream types. For backward compatibility we are
obliged to keep any released types around for as long as they are supported.

By contrast, Debian and Fedora have just the machine classes as they are upstream.

We are an outlier in that we keep the upstream types and only add our
own ones.

Today's upstream "versioned" machine names should be fairly safe since 2.x (see this [discussion](https://lists.nongnu.org/archive/html/qemu-devel/2014-06/msg05376.html)), at least if all devices made a full transition to `vmstate`. But that is only
true if we - as a downstream - add or backport no patches affecting that.

This is not as rare as one might hope. An example of such a change, which is even
common across all SCSI-using architectures, can be seen in the
[QEMU source for the CVE-2014-6351 patch](https://launchpad.net/ubuntu/+source/qemu/2.0.0+dfsg-2ubuntu1.26).

Up to today, the default machine type is:

```text
$MACHINE_ARCH-$DISTRO_RELEASE
```

```text
pc-i440fx-resolute   Ubuntu 26.04 PC (i440FX + PIIX, 1996) (default)
pc-i440fx-questing-v2 Ubuntu 25.10 PC v2 (i440FX + PIIX, + 10.1 machine, 1996)
pc-i440fx-questing   Ubuntu 25.10 PC (i440FX + PIIX, 1996)
pc-i440fx-plucky     Ubuntu 25.04 PC (i440FX + PIIX, 1996)
pc-i440fx-oracular   Ubuntu 24.10 PC (i440FX + PIIX, 1996)
pc-i440fx-noble-v2   Ubuntu 24.04 PC v2 (i440FX + PIIX, arch-caps fix, 1996)
```

Each following release keeps the previously defined aliases to the specific
types for compatibility. Adding a delta requires making sure to not only add a new
type, but also to maintain compatibility for the old type.

In general we want to make it a distribution-specific type on any release.
One could argue that we could instead evaluate whether there is a diff that actually
causes any divergence from the usual types. But doing so severely increases the
maintenance effort and skill requirement on one hand. On the other hand, it makes a
type overview very inconsistent - "where is the one type missing in between
those releases?"

The second use case where the distro-release machine type helps is when, in the
same release, we introduce (via a Stable Release Update, or SRU) new functions that require an update to the
machine type. An example here is on ppc64el, where we backported a feature from
QEMU 2.6 which adds a new hardware device that users need to be available by
default when creating a machine. If this feature was added to the `pseries-2.5` type,
then we have the same issue again of an "old" VM with type `pseries-2.5` which
does not match an updated QEMU where `pseries-2.5` now has a new element;
migration would fail - and even updates might.

This second case drives the need for a "point-release" element in the
downstream names. This is not tied to a usual Ubuntu LTS point release, but to
anything introducing a delta to the machine type / `vmstate`. Similar to CentOS/RHEL,
we want:

```text
$MACHINE_ARCH-$QEMU_VERSION-$DISTRO_RELEASE-${increment for SRU}
```

There are two kinds of SRU/backport to consider differently
here.

The first is a feature backport that should be added into an LTS release. These
are planned tasks and should be batched together (as much as possible) to match
the sub-releases of an LTS. This avoids too much proliferation of those
subtypes. Of course, if there was no change in a given dot release, there is no
need to add a new increment.

The other case is an SRU for a security or severe bug. These are usually
unplanned and have to be taken as an emergency measure. In that case, users are usually
encouraged to restart their workload to pick up the change, just as
you might for some kernel fixes. [VENOM](https://access.redhat.com/articles/1444903), for example, affected the floppy device. Note in particular the resolution
details, which indicate the need to run the new binary by stopping and starting, or by
migration (which invokes the new binary). This supports exactly the case
here: when fixing a CVE, it is desirable to retain the same machine type to
support no-downtime "restart" of the binary. There is also no good reason
to keep the old "broken" machine type around - you don't want the ability to
say "I can still start this with the CVE not fixed". So for these cases there
is no bump to the machine type. Users are unable to migrate from an old
broken system to a new fixed one, but they are supposed to restart anyway.
This again prevents a proliferation of types, but more importantly ensures we
are not forced to keep broken types around if we consider them bad enough that
they should go away.

Finally, at some point in the future one has to stop adding an ever-growing delta.
The thought is to clean out old machine types once they are no longer supported, and leave
the migration paths roughly matching the supported upgrade paths. That means an
LTS unifies former releases and upgrades have to "go through" them.

## Machine type handling summary

Machine types are handled by:

- Adding a distribution-release-specific suffix to the default type(s)
  of each major architecture. Examples for Xenial:
  - x86: `pc-i440fx-xenial` and `pc-q35-xenial`
  - s390x: `s390-ccw-virtio-xenial`
  - ppc64el: `pseries-xenial`
  - arm64: `virt-xenial`
- Feature backports add a `-%d` suffix to the affected types.
  - To avoid a proliferation of these types, such changes should be bundled roughly
    along LTS dot releases.
  - The `-%d` suffix does not have to match the related dot release it was released
    with (it is just an increment).
- Bugfix/security SRUs affecting this do not add an increment.
  - They either do not affect it anyway (no-op),
  - or they are so important that users have to restart the guests anyway to pick up the
    fix.
- The default, if no machine type is specified, always points to the latest
  distribution-specific machine type.
- We do not drop upstream types; they are provided as-is without further
  guarantees.
  - Cross-vendor/downstream migrations might work for upstream types, but are
    considered unsupported. This has always been the case, but package documentation
    might need updating to reflect this.
- Cleanup matches the usual supported distribution upgrade paths.
  - Drop former non-LTS release definitions after the next LTS.
  - Drop former LTS release definitions when out of support.

## Example

An example flow through releases and upgrades.

A release that has a machine type / `vmstate` diff for all x86-based machines, but
none for others:

```text
pc-i440fx-2.5-xenial
pc-q35-2.6-xenial
```

It gets a Xenial feature-backport SRU on an LTS dot release, but it only affects q35-based
machines:

```text
pc-i440fx-2.5-xenial
pc-q35-2.5-xenial
+pc-q35-2.6-xenial-1
```

It gets an SRU for a CVE; users are supposed to restart to pick the fix up:

```text
<no change>
```

It gets another feature-backport SRU that affects all types on the next dot release:

```text
pc-i440fx-2.5-xenial
+pc-i440fx-2.5-xenial-1
pc-q35-2.5-xenial
pc-q35-2.6-xenial-1
+pc-q35-2.6-xenial-2
```

## Support matrix

This section lists the migration paths that are expected to work. In general these
should match the Ubuntu upgrade paths. So an interim release can
migrate to the following interim release for as long as it is supported. Later on, those are
unified by the LTS release - and always LTS to following LTS.
Of course, migrations from a release to "itself" are supported as well.

| from v / to > | LTS | Int | Int+1 | Int+2 | LTS+1 | Int+3 | Int+4 | Int+5 | LTS+2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LTS   | Y | Y |   |   | Y |   |   |   | Y |
| Int   |   | Y | Y |   |   |   |   |   |   |
| Int+1 |   |   | Y | Y |   |   |   |   |   |
| Int+2 |   |   |   | Y | Y |   |   |   |   |
| LTS+1 |   |   |   |   | Y | Y |   |   | Y |
| Int+3 |   |   |   |   |   | Y | Y |   |   |
| Int+4 |   |   |   |   |   |   | Y | Y |   |
| Int+5 |   |   |   |   |   |   |   | Y | Y |
| LTS+2 |   |   |   |   |   |   |   |   | Y |

Other paths might work as well - in fact, quite a few do - but only those listed are
officially considered supported.

The same applies when thinking not about live migrations, but instead stopping
(and maybe moving) a guest and starting it on another host or after an upgrade. But
in that case you don't have to give up if the upgrade path isn't supported as
above. Instead, in most cases you just have to update your guest
configuration to lift it to a newer machine type. At least, Linux guests mostly
auto-detect the new features and work fine. A short guide is in the
{ref}`upgrade-machine-type` section below.

Backward migrations in particular are not considered supported by upstream.
Both upstream and the packaging of fixes try to keep things working, but expect
any backward migration to be risky. See [bug 1536487](https://bugs.launchpad.net/ubuntu/+source/qemu/+bug/1536487) for a discussion of that case.

Sometimes, when reaching a state where the initial guest was created on a now
unsupported release, the administrator has to upgrade the machine type from
the unsupported one to a newer one - see the section below for details.

(upgrade-machine-type)=
## Upgrade machine type

You might want to update the machine type of an existing defined guest to:

- pick up the latest security fixes and features, or
- continue using a guest created on a now-unsupported release.

In general, it is recommended to update machine types when upgrading QEMU/KVM to
a new major version. But this can likely never be an automated task, as this change is
guest-visible: the guest devices might change in appearance, new features are announced to
the guest, and so on. Linux is usually very good at tolerating such changes, but it
depends so much on the setup and workload of the guest that this has to be evaluated by the
owner/admin of the system. Other operating systems are known to often experience severe
impacts when changing the hardware. Consider a machine type change similar to replacing all
devices and firmware of a physical machine with the latest revision: all considerations
that apply there apply to evaluating a machine type upgrade as well.

As usual with major configuration changes, it is wise to back up your guest
definition and disk state so you can roll back if needed.

There is no integrated single command to update the machine type via {manpage}`virsh(1)` or
similar tools. The machine type is a normal part of your machine definition, and is
therefore updated the same way as most others.

First, shut down your machine and wait
until it has reached that state:

```{terminal}
:copy:
:user:
:host:
:dir:
virsh shutdown <yourmachine>
# wait
virsh list --inactive
# should now list your machine as "shut off"
```

Then edit the machine definition and find the type in the `type` tag of the
`machine` attribute:

```{terminal}
:copy:
:user:
:host:
:dir:
virsh edit <yourmachine>
```

```xml
<type arch='x86_64' machine='pc-i440fx-xenial'>hvm</type>
```

Change this to the value you want. If you need to check which types are available,
use `-M ?`. Note that, while upstream types are provided as a convenience, only Ubuntu types are
supported. The list also shows what the current default would be.
In general, it is strongly recommended that you change to newer types if possible,
to take advantage of newer features and to benefit from bugfixes that only apply to
the newer device virtualization:

```{terminal}
:copy:
:user:
:host:
:dir:
kvm -M ?
# lists machine types, e.g.
pc-i440fx-xenial       Ubuntu 16.04 PC (i440FX + PIIX, 1996) (default)
...
```

After this you can start your guest again.
You can check the current machine type from the guest and host, depending on your
needs:

```{terminal}
:copy:
:user:
:host:
:dir:
virsh start <yourmachine>
# check from host, via dumping the active xml definition
virsh dumpxml <yourmachine> | xmllint --xpath "string(//domain/os/type/@machine)" -
# or from the guest via dmidecode
sudo dmidecode | grep Product -A 1
        Product Name: Standard PC (i440FX + PIIX, 1996)
        Version: pc-i440fx-xenial
```

If you keep non-live definitions around, such as XML files, remember to update those
as well.

## Further reading

* [Live migrating QEMU/KVM virtual machines (Red Hat Developer)](https://developers.redhat.com/blog/2015/03/24/live-migrating-qemu-kvm-virtual-machines/)
* [QEMU documentation](https://www.qemu.org/documentation/)
* [libvirt documentation](https://libvirt.org/)
</content>
</invoke>
