# Ansible Arch Dev Machine

This playbook and role aims to setup my personal dev machine running arch linux.

The following steps are required prior to the execution of the playbook

- [Install ArchLinux](https://wiki.archlinux.org/title/Installation_guide)

- Install Extra Packages:

```bash
pacman -S git openssh python3
```

- Enable sshd service

```bash
systemctl enable sshd
systemctl start sshd
```

Ensure you have the variables set up before running the playbook

Example

```yaml
ssh_banner_enabled: true    # enable ssh banner on login             [true/false]
ssh_banner_text: Arch Linux # banner text for ssh session            [default:hostname]
git_name: User Name         # same as git config --global user.name
git_email: user@email.com   # same as git config --global user.email
virtual_machine: true       # install and secure qemu-guest-agent    [true/false]
desktop_environment: true   # install desktop environment            [true/false]
```

Check also [archlinux.yml](archlinux.yml) to configure your `become_user`

Run the playbook

```bash
ansible-playbook archlinux.yml --ask-become-pass --limit <host>
```

> `--ask-become-pass` is needed to configure on the first run only
