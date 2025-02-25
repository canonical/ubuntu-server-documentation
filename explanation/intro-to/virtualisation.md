(introduction-to-virtualization)=
# Introduction to virtualization

Virtualization is a technology that allows you to create safe, isolated environments on your server. Developers can use virtualization to create self-contained sandboxes for development and testing that cannot negatively affect the host machine. System administrators can use virtualization to scale network resources to meet changing demand, giving greater control and flexibility in managing infrastructure.

The **virtualization stack** uses layers of abstraction to help users work with virtualization more easily. Each layer of abstraction hides the complexity of layers below it, allowing the user to work with a more high-level view.

## Virtual machines

Virtual machines (VMs) are essentially computers-within-computers. A VM provides strong isolation and reduces the need for additional hardware when running different operating system environments. A VM includes its own operating system and simulated resources, making it completely independent of the host machine and other VMs. To find out more, see this overview of {ref}`the different VM tools and technologies <vm-tools-in-the-ubuntu-space>` available in the Ubuntu space.

## Containers

Containers are a lightweight virtualization technology. Unlike a VM, they share the operating system of the host machine so they are fast to provision when demand for resources is high. 

Containers are also useful for running and packaging applications because they contain all of the application's dependencies and libraries. Containers ensure consistency across different environments. 

Containers come in two main types: **system** containers, and **application** containers.

### System containers

System containers simulate a full machine like a VM, but use the operating system of the host machine. They are often used for separating user spaces.

### Application containers

Application containers package the components required for a specific application to run, including all dependencies and libraries. This allows the application to be run easily in different environments. Application containers are particularly useful for running microservices.

For more details about container tools available in the Ubuntu space, {ref}`take a look at this overview <container-tools-in-the-ubuntu-space>`.
