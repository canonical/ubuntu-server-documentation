(enable-nested-virtualisation)=
# How to enable nested virtualisation

> **Disclaimer**:
> Nested virtualisation is enabled by default on Ubuntu. If you are using Ubuntu, it's unlikely that you will need to manually enable the feature. If you check (using the steps below) and discover that nested virtualisation is enabled, then you will not need to do anything further.

There may be use cases where you need to enable nested virtualisation so that you can deploy instances inside other instances. The sections below explain how to check if nested virtualisation is enabled/available and how to enable it if that is not the case. Bear in mind that currently nested virtualisation is only supported in Ubuntu on `x86` machine architecture. 

## Check if nested virtualisation is enabled

Check if the required kernel module for your CPU is already loaded. Hosts with Intel CPUs require the `kvm_intel` module while {term}`AMD` hosts require `kvm_amd` instead:
  
```bash
$ lsmod | grep -i kvm
kvm_intel               204800  0
kvm                  1347584  1 kvm_intel
```

### If the module is loaded

If the module is already loaded, you can check if nested virtualisation is enabled by running the following command:

```bash
cat /sys/module/<module>/parameters/nested
```

As an example for AMD hosts:

```bash
$ cat /sys/module/kvm_amd/parameters/nested
1
```

If the output is either `1` or `Y` then nested virtualisation is enabled and you will not need to manually enable the feature (this should be the case for Ubuntu users).

### If the module is not loaded

If the module your host requires is not loaded you can load it using `modprobe` and add the property `nested=1` to enable nested virtualisation as shown below for Intel hosts:

```bash
modprobe kvm-intel nested=1
```

Or as follows for AMD hosts: 

```bash
modprobe kvm-amd nested=1
```


## Enable nested virtualisation 

If the above checks indicate that nested virtualisation is not enabled, you can follow the below steps to enable it.

  * Create a file in `/etc/modprobe.d` -e.g., `/etc/modprobe.d/kvm.conf`- and add the line `options kvm-intel nested=1` to that file (replace `kvm-intel` with `kvm-amd` for AMD hosts).

  * Reload the kernel module to apply the changes:

  ```bash
    sudo modprobe -r <module>
  ```

  Example for Intel hosts:

  ```bash
    sudo modprobe -r kvm-intel
  ```

  * You should now be able to see nested virtualisation enabled:

  Example for Intel hosts:
  ```bash
    $ cat /sys/module/kvm_intel/parameters/nested
    Y
  ```

## Check and enable nested virtualisation inside an instance

Once the host is ready to use nested virtualisation it is time to check if the guest instance where the other instance(s) are going to run is able to host these nested VMs. 

To determine if an instance can host another instance on top, run the below command within the instance:

```bash
egrep "svm|vmx" /proc/cpuinfo
``` 

If any of these are present in the output (depending on whether the host is AMD or Intel respectively), then virtualisation is available in that instance. If this is not the case you will need to edit the instance CPU settings:

  * Shut down the instance
  * Edit the instance XML definition file executing: `virsh edit <instance>`
  * Search the `cpu mode` parameter in and set its value to either `host-model` or `host-passthrough` (details about these modes can be found [here](https://wiki.openstack.org/wiki/LibvirtXMLCPUModel)).

    Sample `cpu mode` parameter in XML with nested virtualisation: 
    ```xml
      <cpu mode='host-model' check='partial'/>
    ```
  * Save the modifications and start the instance

## Limitations of nested virtualisation

Nested virtualisation has some key limitations you'd need to consider. Namely, not all KVM features will be available for instances running nested VMs and actions such as migrating or saving the parent instance will not be possible until the nested instance is stopped.
