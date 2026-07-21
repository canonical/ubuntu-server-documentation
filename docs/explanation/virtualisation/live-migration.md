---
myst:
  html_meta:
    description: Understand QEMU/libvirt live migration.
---

(live-migration)=
# Live migration with libvirt/QEMU

Live migration with QEMU and libvirt is the process of moving a running virtual machine from one physical server to another with near-zero downtime.

During this process:

- QEMU acts as the engine, actively streaming the VM's live memory (RAM) and CPU state across the network. It can work without libvirt. A live migration can be triggered using QEMU Monitor Protocol (QMP).

- libvirt acts as the manager, coordinating the setup, security, and handoff between the two physical servers so the guest operating system and its applications keep running without interruption.

Although migration is a complex process, it generally works well if you migrate VMs between source and destination hosts with very similar capabilities, both on hardware (CPU model) and software (QEMU version) levels. But the reality is that the infrastructure is very often heterogeneous, with CPUs and virtualization software stacks at different generations or versions. Migration can still happen across hosts with different hardware and software versions (for example, different QEMU versions). Two mechanisms make this possible:

- **Versioned machine types**, which keep the guest's virtual hardware layout stable across QEMU versions.
- **CPU model + named features**, which allows the CPU to be expressed as a baseline model name +/- named features.

## Versioned machine types

The QEMU machine type defines the exact virtual hardware blueprint (chipset, PCI slots, ACPI tables) of a virtual machine. This allows QEMU to offer VMs a well-defined and stabilized foundation they can run on, so they are not impacted by changes that happen "under the hood" on the virtualization software stack. The machine types are useful to ensure live migration succeeds, especially inside heterogeneous infrastructure.

When you live-migrate a VM, you are taking a snapshot of a running system's RAM and CPU state and sending it over the wire. The destination host must have a virtual hardware environment that matches that state down to the very last byte; this is possible by keeping the machine type unchanged. However, when the QEMU software is upgraded, machine types can evolve and get new features that might be incompatible with the migrated virtual machine. The solution is to version the machine types by creating a new version of the machine type for each supported QEMU version.

For more detail on Ubuntu machine types and how to upgrade the machine type of an existing guest, see {ref}`qemu-machine-types`.

## CPU baseline and named features

Versioned machine types keep the virtual platform stable, but they do not control the CPU that the guest sees. The CPU is exposed separately, and it is the second mechanism that makes migration across heterogeneous hosts possible.

Libvirt and QEMU allow the CPU to be expressed in ways that ease migration between hosts in heterogeneous infrastructures. While a libvirt VM configured with `host-passthrough` or `maximum` (the equivalents in QEMU are `-cpu host` and `-cpu max` respectively) gets the most out of the hardware, it exposes the guests to all available host capabilities. Therefore, migration to another host is much more restricted, because it needs to be able to present the very same environment to the guest. To do so it needs a clear definition that helps to ensure both sides of the migration can present the same. Therefore it is preferred to specifying the CPU capabilities as a baseline CPU model +/- a list of features to ensure compatibility. In QEMU, it comes down to this example `-cpu` argument:

```text
-cpu EPYC-Turin,x2apic=on,tsc-deadline=on,hypervisor=on,tsc-adjust=on,
 spec-ctrl=on,stibp=on,flush-l1d=on,ssbd=on,cmp-legacy=on,virt-ssbd=on,
 tsa-sq-no=on,tsa-l1-no=on,pcid=off,la57=off
```

Or in a level higher, you can ask libvirt to build the CPU for you by using the `host-model` CPU mode.
This will detect the current CPU with all its features, but automatically expresses it as baseline CPU model +/- a list of features.

```xml
...
  <cpu mode='host-model' check='partial'/>
...
```

or you might prefer even more control and provide the exact CPU specification:

```xml
...
  <cpu mode='custom' match='exact' check='full'>
    <model fallback='forbid'>EPYC-Turin</model>
    <vendor>AMD</vendor>
    <feature policy='require' name='x2apic'/>
    <feature policy='require' name='tsc-deadline'/>
    ...
    <feature policy='require' name='tsa-l1-no'/>
    <feature policy='disable' name='pcid'/>
    <feature policy='disable' name='la57'/>
...
```

While the first approach of just using `host-passthrough` and even `host-model` seems easier and more appealing, it is not suitable for heterogeneous infrastructure. To retain full control over migratability across every host in the migration pool a CPU should be modeled.
You can check the capabilities of every host in your pool and define the CPU definition to only advertise CPU features to the guest that are guaranteed to exist on every host in the pool.
This creates a stable "lowest common denominator" CPU that looks identical on both the source and the destination, so the guest never comes to rely on a feature that could disappear after a migration.


### Determining the lowest common CPU denominator


Finding the lowest denominator seems to be a complex task. Fortunately, libvirt provides a command to compute it (see {manpage}`virsh(1)` and its `hypervisor-cpu-baseline` command) by taking the CPU definitions of every host in the pool and returning a single baseline CPU that all of them can support.

First, collect the host CPU definition from each host in the pool. The `<cpu>` block reported by `virsh capabilities` describes what the host CPU offers:

```text
virsh capabilities > host1-caps.xml
```

Then feed all the files to `hypervisor-cpu-baseline`. Libvirt extracts the `<cpu>` element from each file and computes the baseline:

```text
virsh hypervisor-cpu-baseline --migratable host1-caps.xml host2-caps.xml
```

The `--migratable` option restricts the result to features that are safe to migrate, excluding those that cannot be preserved across a migration. The command prints a `<cpu>` block similar to this:

```xml
<cpu mode='custom' match='exact'>
  <model fallback='forbid'>EPYC-Turin</model>
  <vendor>AMD</vendor>
  <feature policy='require' name='x2apic'/>
  <feature policy='require' name='tsc-deadline'/>
  ...
</cpu>
```

This block is the lowest common denominator CPU for the pool. Drop it into the domain XML of the VMs you intend to migrate, so that these VMs see the same CPU regardless of which host they run on.

## Further reading

* [QEMU documentation on migration](https://www.qemu.org/docs/master/devel/migration/main.html)
* [libvirt documentation on migration](https://libvirt.org/migration.html)