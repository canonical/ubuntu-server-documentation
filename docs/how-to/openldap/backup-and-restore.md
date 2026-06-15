---
myst:
  html_meta:
    description: Back up and restore OpenLDAP configuration and data using slapcat and systemd timers.
---

(ldap-backup-and-restore)=
# Backup and restore OpenLDAP

Once you have LDAP running the way you want, it is time to ensure you can save all your work and restore it as needed.

What we need is a way to back up the directory database(s) -- specifically the configuration backend (`cn=config`) and the {term}`DIT` (`dc=example,dc=com`).

## Backup script

Create `/usr/local/bin/ldapbackup` with the following content:

```bash
#!/bin/bash
set -euo pipefail

BACKUP_PATH=/export/backup
CONFIG_BACKUP=f${BACKUP_PATH}/config.ldif"
DATA_BACKUP="${BACKUP_PATH}/example.com.ldif"

# create and secure backup files
touch "$CONFIG_BACKUP" "$DATA_BACKUP"
chmod 600 "$CONFIG_BACKUP" "$DATA_BACKUP"

# Backup server config
nice slapcat -b cn=config > "$CONFIG_BACKUP"
# Backup directory tree
nice slapcat -b dc=example,dc=com > "$DATA_BACKUP"

# Optionally, use a backup tool like borgbackup to store the backups off-site
```

Make it executable:

```bash
sudo chmod +x /usr/local/bin/ldapbackup
```

:::{note}
These files are uncompressed text files containing everything in your directory including the tree layout, usernames, and every password. Consider making `/export/backup` an encrypted partition and even having the script encrypt files as it creates them.
:::

## Schedule backups with systemd

Create a systemd service unit at `/etc/systemd/system/ldapbackup.service`:

```ini
[Unit]
Description=LDAP backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/ldapbackup
```

Create a timer unit at `/etc/systemd/system/ldapbackup.timer`:

```ini
[Unit]
Description=Run LDAP backup daily

[Timer]
OnCalendar=*-*-* 22:45:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ldapbackup.timer
```

Verify the timer is active:

```bash
systemctl list-timers ldapbackup.timer
```

Now the files are created, they should be copied to a backup server.

## Restore script

Assuming a fresh reinstall of LDAP, create `/usr/local/bin/ldaprestore`:

```bash
#!/bin/bash
set -euo pipefail

BACKUP_PATH=/export/backup

if [ -n "$(ls -l /var/lib/ldap/* 2>/dev/null)" ] || [ -n "$(ls -l /etc/ldap/slapd.d/* 2>/dev/null)" ]; then
    echo "Existing database found. Run the following to remove it:"
    echo "  sudo systemctl stop slapd.service"
    echo "  sudo rm -rf /etc/ldap/slapd.d/* /var/lib/ldap/*"
    exit 1
fi

sudo systemctl stop slapd.service || :
sudo slapadd -F /etc/ldap/slapd.d -b cn=config -l ${BACKUP_PATH}/config.ldif
sudo slapadd -F /etc/ldap/slapd.d -b dc=example,dc=com -l ${BACKUP_PATH}/example.com.ldif
sudo chown -R openldap:openldap /etc/ldap/slapd.d/
sudo chown -R openldap:openldap /var/lib/ldap/
sudo systemctl start slapd.service
```

This is a basic backup strategy shown here as a reference for the tooling available for backups and restores.
