(introduction-to-cloud-init)=

# Introduction to cloud-init

Managing and configuring cloud instances and servers can be a complex and
time-consuming task. [Cloud-init](https://docs.cloud-init.io/en/latest/) is
the industry-standard open source tool designed to automate getting systems up
and running with preconfigured settings in a repeatable way across instances and platforms.

Although it’s commonly used to automatically configure public or private cloud
instances, it can also be used to deploy virtual machines and physical machines
on a network. By automating all the routine setup tasks, systems can be
initialized efficiently and reliably, whether you’re a developer spinning up
virtual machines or containers, or a system administrator managing
infrastructure.

## How does it work?

Cloud-init works by taking the initial configuration that you supply, and
applying it at boot time so that when the instance is launched it’s already
configured the way you want.

Your configuration can be used and re-used as often as you want to get the exact same VM environment every time, or to deploy an
entire fleet of machines in exactly the same way. You get consistent results with a fraction of the time and effort it would take to do
so manually.

It can handle a range of tasks that normally happen when a new instance is
created, such as setting the {term}`hostname`, configuring network interfaces, creating
user accounts, and even running custom scripts.

## Related products

Cloud-init can automatically detect the source platform it is being run on
([the datasource](https://docs.cloud-init.io/en/latest/reference/datasources.html)).
It is widely-supported and works with:

* Most public cloud offerings (including Amazon EC2, Azure, Google Compute Engine)
* Private clouds
* MAAS and OpenStack
* Common virtualization and VM software such as LXD, libvirt, and QEMU

You can also use it on other Linux distributions (such as RedHat, OpenSUSE, and
Alpine), or in concert with popular configuration managers (like Ansible, Chef,
and Puppet). It even supports the Windows Subsystem for Linux (WSL)!

To learn more about cloud-init and try it out for yourself,
[check out their tutorials](https://docs.cloud-init.io/en/latest/tutorial/index.html).

