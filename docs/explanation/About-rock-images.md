(About-rock-images)=
# About rock images

A rock is an [Ubuntu-based container image](https://canonical-rockcraft.readthedocs-hosted.com/en/latest/explanation/rocks/#). Rocks are [OCI-compliant](https://opencontainers.org/) and thus compatible with all popular container management tools (such as Docker and Kubernetes) and container registries (such as Docker Hub and Amazon ECR). They are built to be secure and stable by design.

Rocks are [created using Rockcraft](https://canonical-rockcraft.readthedocs-hosted.com/en/latest/explanation/rockcraft/), which in turn [uses Chisel](https://canonical-rockcraft.readthedocs-hosted.com/en/latest/explanation/chisel/) to extract the relevant parts of Debian packages needed to form a minimal container image. By keeping rocks small and specific, their exposure to vulnerabilities is minimised.

Although rocks can be useful for anyone using containers, in the Ubuntu Server context they are particularly helpful for system administrators who want to use containers to manage their infrastructure. To find out how to run rocks on your server, refer to [our how-to guide](https://discourse.ubuntu.com../reference/multi-node-rock-configuration-with-docker-compose.md). Alternatively, to find out more about rocks and Rockcraft, refer to the [official Rockcraft documentation](https://canonical-rockcraft.readthedocs-hosted.com/en/latest/).
