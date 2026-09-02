---
myst:
  html_meta:
    description: Inspect, copy, and delete container images between registries and local storage with Skopeo on Ubuntu Server.
---

(skopeo)=
# Skopeo for system admins

[Skopeo](https://github.com/containers/skopeo) works with container images and image registries. It needs no daemon and no root privileges. You can inspect a remote image before you deploy it, copy images between registries or into local storage, mirror whole repositories, and delete images from a registry.

## Install Skopeo

{manpage}`skopeo(1)` is available in Ubuntu:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install skopeo
```

## Image names

Many Skopeo commands take an image name prefixed by a transport, which specifies where the image lives:

`docker://`
: An image in a remote registry, for example `docker://docker.io/ubuntu:26.04`.

`docker-daemon:`
: An image in the local Docker daemon storage.

`containers-storage:`
: An image in the local storage used by [Podman](https://podman.io/) and [Buildah](https://buildah.io/).

`dir:`
: An image unpacked into a local directory.

`oci:` and `oci-archive:`
: An image in an {term}`OCI` layout directory or `tar` archive.

See {manpage}`containers-transports(5)` for the full list and the exact syntax of each transport.

## Inspect a remote image

{manpage}`skopeo-inspect(1)` downloads only the image metadata, not its layers, so you can check what an image contains before you pull it:

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo inspect docker://docker.io/ubuntu:26.04

{
    "Name": "docker.io/library/ubuntu",
    "Digest": "sha256:2260313b31c8c011cd2eebe728008efac1b3982be73eb71348ea2648d2c0e09b",
    "RepoTags": [
        "24.04",
        "25.10",
        "26.04",
        "latest"
    ],
    "Created": "2026-08-17T09:00:47.315779976Z",
    "DockerVersion": "",
    "Labels": {
        "org.opencontainers.image.created": "2026-08-17T09:02:45.677319+00:00",
        "org.opencontainers.image.title": "ubuntu",
        "org.opencontainers.image.version": "26.04"
    },
    "Architecture": "amd64",
    "Os": "linux",
    "Layers": [
        "sha256:06e9d71331fb2b620a4f6c8064e0f84b284bb69a42c7c57b1c962bd4a4cdee76",
        "sha256:f3db1cd940786339b09d8a60e47c66fea9502d788e6fab5bec91a4a77d4ced1c"
    ],
    "LayersData": [
        {
            "MIMEType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "Digest": "sha256:06e9d71331fb2b620a4f6c8064e0f84b284bb69a42c7c57b1c962bd4a4cdee76",
            "Size": 41569203,
            "Annotations": {
                "ci.umo.uncompressed_blob_size": "111523840"
            }
        },
        {
            "MIMEType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "Digest": "sha256:f3db1cd940786339b09d8a60e47c66fea9502d788e6fab5bec91a4a77d4ced1c",
            "Size": 393,
            "Annotations": {
                "ci.umo.uncompressed_blob_size": "10240"
            }
        }
    ],
    "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    ]
}
```

You can use {manpage}`skopeo-list-tags(1)` to list the available tags in a repository.

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo list-tags docker://docker.io/ubuntu

{
    "Repository": "docker.io/library/ubuntu",
    "Tags": [
        "22.04",
        "24.04",
        "26.04",
        "latest"
    ]
}
```

## Authenticate to a registry

Public images need no credentials. For a private registry, log in with {manpage}`skopeo-login(1)`. Skopeo stores the credentials in `${XDG_RUNTIME_DIR}/containers/auth.json` (see {manpage}`containers-auth.json(5)`):

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo login registry.example.com

Username: myuser
Password:
Login Succeeded!
```

Alternatively, pass credentials per command with `--creds user:password` (for `inspect` and `delete`), or `--src-creds` and `--dest-creds` (for `copy`).

Skopeo can also automatically use authentication credentials set by `docker login`, `podman login` or `buildah login`.

## Copy images

### Between registries

Copying an image into an internal registry with {manpage}`skopeo-copy(1)` doesn't require a local daemon, and the image is never unpacked while copying:

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo copy \
docker://docker.io/ubuntu:26.04 \
docker://registry.example.com/mirror/ubuntu:26.04

Getting image source signatures
Copying blob 06e9d71331fb done
Copying blob f3db1cd94078 done
Copying config af52039db3 done
Writing manifest to image destination
```

By default, Skopeo only copies the image that matches the architecture of your machine. Add `--all` to copy every architecture of a multi-architecture image.

Both `copy` and `sync` can sign the images they write with `--sign-by` or `--sign-by-sigstore`, but the signatures are only checked if you configure a trust policy. Refer to {manpage}`containers-policy.json(5)` and {manpage}`containers-registries.d(5)` for more details.

### To and from local storage

Copy a remote image into the local Docker daemon:

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo copy docker://docker.io/ubuntu:26.04 docker-daemon:ubuntu:26.04
```

Or save it as an OCI archive:

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo copy docker://docker.io/ubuntu:26.04 oci-archive:ubuntu-26.04.tar:ubuntu:26.04
```

The same command works in reverse, with the archive as the source and a registry as the destination.

## Mirror multiple images

`copy` handles one image at a time, while {manpage}`skopeo-sync(1)` copies a set of images in a single run and leaves out anything the destination already has. When using `sync`, specify the transports with `--src` and `--dest` instead of prefixing the image names.

To sync a single image, or a whole repository, into an internal registry:

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo sync --src docker --dest docker docker.io/ubuntu:26.04 registry.example.com/mirror

INFO[0000] Tag presence check                            imagename="docker.io/ubuntu:26.04" tagged=true
INFO[0000] Copying image ref 1/1                         from="docker://ubuntu:26.04" to="docker://registry.example.com/mirror/ubuntu:26.04"
Getting image source signatures
Copying blob 06e9d71331fb done
Copying blob f3db1cd94078 done
Copying config af52039db3 done
Writing manifest to image destination
INFO[0005] Synced 1 images from 1 sources
```

A source repository without a tag syncs every tag in it.

You can also sync to a directory. The `--scoped` option keeps the source registry name in the path so that images from different registries cannot collide:

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo sync --src docker --dest dir --scoped docker.io/ubuntu:26.04 /media/usb
```

This writes the image to `/media/usb/docker.io/library/ubuntu:26.04`. To sync it back into a registry, use `--src dir --dest docker`.

### Syncing from a YAML file

When you run the same mirror repeatedly, list the images in a {term}`YAML` file and pass `--src yaml`. You can name tags one by one, or match them with a regular expression:

```yaml
docker.io:
  images:
    ubuntu:
      - "24.04"
      - "26.04"
  images-by-tag-regex:
    nginx: ^1\.2[0-9]-alpine$
```

Check what a sync would do before you run it with `--dry-run`:

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo sync --src yaml --dest docker --dry-run sync.yaml registry.example.com/mirror

INFO[0000] Processing repo                               registry=docker.io repo=ubuntu
INFO[0000] Processing repo                               registry=docker.io repo=nginx
INFO[0000] Querying registry for image tags              registry=docker.io repo=nginx
INFO[0000] Getting tags                                  image=docker.io/library/nginx
WARN[0001] Running in dry-run mode
INFO[0001] Would have copied image ref 1/2               from="docker://ubuntu:24.04" to="docker://registry.example.com/mirror/ubuntu:24.04"
INFO[0001] Would have copied image ref 2/2               from="docker://ubuntu:26.04" to="docker://registry.example.com/mirror/ubuntu:26.04"
INFO[0001] Would have copied image ref 1/10              from="docker://nginx:1.20-alpine" to="docker://registry.example.com/mirror/nginx:1.20-alpine"
INFO[0001] Would have copied image ref 2/10              from="docker://nginx:1.21-alpine" to="docker://registry.example.com/mirror/nginx:1.21-alpine"
INFO[0001] Would have copied image ref 3/10              from="docker://nginx:1.22-alpine" to="docker://registry.example.com/mirror/nginx:1.22-alpine"
INFO[0001] Would have copied image ref 4/10              from="docker://nginx:1.23-alpine" to="docker://registry.example.com/mirror/nginx:1.23-alpine"
INFO[0001] Would have copied image ref 5/10              from="docker://nginx:1.24-alpine" to="docker://registry.example.com/mirror/nginx:1.24-alpine"
INFO[0001] Would have copied image ref 6/10              from="docker://nginx:1.25-alpine" to="docker://registry.example.com/mirror/nginx:1.25-alpine"
INFO[0001] Would have copied image ref 7/10              from="docker://nginx:1.26-alpine" to="docker://registry.example.com/mirror/nginx:1.26-alpine"
INFO[0001] Would have copied image ref 8/10              from="docker://nginx:1.27-alpine" to="docker://registry.example.com/mirror/nginx:1.27-alpine"
INFO[0001] Would have copied image ref 9/10              from="docker://nginx:1.28-alpine" to="docker://registry.example.com/mirror/nginx:1.28-alpine"
INFO[0001] Would have copied image ref 10/10             from="docker://nginx:1.29-alpine" to="docker://registry.example.com/mirror/nginx:1.29-alpine"
INFO[0001] Would have synced 12 images from 2 sources
```

Add `--keep-going` if you want the sync to carry on when one image fails instead of stopping.

## Delete an image from a registry

Use {manpage}`skopeo-delete(1)` to remove an image:

```{terminal}
:copy:
:user:
:host:
:dir:
skopeo delete docker://registry.example.com/mirror/ubuntu:26.04
```

This deletes the manifest, so the tag stops resolving. The registry only reclaims the layers when it runs garbage collection.

## Further reading

* [Skopeo upstream documentation](https://github.com/containers/skopeo)
* {ref}`container-tools-in-the-ubuntu-space`
