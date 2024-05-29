# Ubuntu Server reference


Our *reference* section is used for quickly checking what software and commands are available, and how to interact with various tools.

## Server installation

|||
|--|--|
| Installation requirements
|| [System requirements](reference/system-requirements.md) |
|||

The Ubuntu installer now has its own documentation for automatic (or “hands-off” installations). For more guidance on auto-installing Ubuntu with the installer, you can refer to the following guides from the Ubuntu installer documentation (note: these pages will redirect you outside of the Server Guide).

|||
|--|--|
| Automatic installation ||
|| [Autoinstall config file reference](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html) |
|| [Autoinstall JSON schema](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-schema.html) |



## Cloud images

|||
|--|--|
| Cloud images ||
|| [Overview](reference/cloud-images.md) |
| Find cloud images for...| |
|| [Amazon EC2*](https://canonical-aws.readthedocs-hosted.com/en/latest/aws-how-to/instances/find-ubuntu-images/) |
|| [Google Compute Engine (GCE)*](https://canonical-gcp.readthedocs-hosted.com/en/latest/google-how-to/gce/find-ubuntu-images/) |
|| [Microsoft Azure*](https://canonical-azure.readthedocs-hosted.com/en/latest/azure-how-to/instances/find-ubuntu-images/) |

\* Note: these starred links will redirect you outside the Server Guide to the officially maintained versions of this documentation

## High availability

|||
|--|--|
| Migrate from `crmsh` to `pcs` ||
|| [Reference table of corresponding commands](reference/migrate-from-crmsh-to-pcs.md) |
|||

## Backups and version control

|||
|--|--|
| Example scripts ||
|| [Basic backup shell script](reference/basic-backup-shell-script.md) |
|| [Archive rotation shell script](reference/archive-rotation-shell-script.md) |
|||

## ROCK images

|||
|--|--|
|| [Intro to ROCK images](reference/introduction-to-rock-images.md) |
|| [ROCK customisation with Docker](reference/rock-customisation-with-docker.md) |
|| [Multi-node configuration with Docker-Compose](reference/multi-node-rock-configuration-with-docker-compose.md) |
|||

## Debugging

These pages are for those interested in packaging and Ubuntu development

|||
|--|--|
|| [About debuginfod](reference/about-debuginfod.md) |
|| [Debug symbol packages](reference/debug-symbol-packages.md) |
|||

## Other tools

|||
|--|--|
|| [Byobu](reference/byobu.md) |
|| [pam_motd](reference/pam-motd.md) |
|||


```{toctree}
:hidden:
reference/system-requirements.md
reference/cloud-images.md
reference/migrate-from-crmsh-to-pcs.md
reference/basic-backup-shell-script.md
reference/archive-rotation-shell-script.md
reference/about-debuginfod.md
reference/debug-symbol-packages.md
reference/byobu.md
reference/pam-motd.md
reference/introduction-to-rock-images.md
reference/rock-customisation-with-docker.md
reference/multi-node-rock-configuration-with-docker-compose.md
```