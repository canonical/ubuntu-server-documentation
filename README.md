# Ubuntu Server documentation

Ubuntu Server is a version of the Ubuntu operating system designed and
engineered as a backbone for the internet.

Ubuntu Server brings economic and technical scalability to your datacenter,
public or private. Whether you want to deploy an OpenStack cloud, a Kubernetes
cluster or a 50,000-node render farm, Ubuntu Server delivers the best value
scale-out performance available.

## Project and community

Ubuntu Server is a member of the Ubuntu family. It's an open source project
that welcomes community projects, contributions, suggestions, fixes and
constructive feedback.

If you find any errors or have suggestions for improvements to pages, please
file an issue against this repository, or use the "Give feedback" link from the
documentation. There you can share your comments or let us know about problems
with any page.

* [Read our Code of Conduct](https://ubuntu.com/community/code-of-conduct)
* [Get support](https://ubuntu.com/support/community-support)
* [Join the Discourse forum](https://discourse.ubuntu.com/c/server/17)
* [Download Ubuntu Server](https://ubuntu.com/server)
* [Find out how to contribute](https://documentation.ubuntu.com/server/contributing/)

## Offline version

You can [build this documentation locally](https://documentation.ubuntu.com/server/contributing/build-locally), or you can
access [the PDF version](https://documentation.ubuntu.com/server/) of this
documentation from Read the Docs.

## Automated maintenance

This repository includes automated workflows to maintain documentation quality:

### Update Redirecting Links

A weekly GitHub Action automatically updates links that redirect to new URLs. The
[`update_redirecting_links.py`](update_redirecting_links.py) script:

- Runs every Monday at 9:00 AM UTC
- Identifies links that redirect to other URLs
- Updates them to point directly to the final destination
- Creates a PR for human review before merging

See [UPDATE_REDIRECTING_LINKS.md](UPDATE_REDIRECTING_LINKS.md) for details on how
this works and how to run it manually.
