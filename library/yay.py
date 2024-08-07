#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_command(module, cmd):
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr, 0
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def check_package_installed(package):
    cmd = ['pacman', '-Q', package]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='list', required=True),
            state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
            update_cache=dict(type='bool', required=False, default=False),
            use_sudo=dict(type='bool', required=False, default=False),
        ),
        supports_check_mode=True
    )

    params = module.params
    packages = params['name']
    state = params['state']
    update_cache = params['update_cache']
    use_sudo = params['use_sudo']

    results = {
        'changed': False,
        'original_message': '',
        'message': '',
        'stdout': '',
        'stderr': '',
        'changes': {},
        'failed_packages': {}
    }

    if update_cache:
        cmd = ['yay', '-Syu', '--noconfirm']
        if use_sudo:
            cmd.insert(0, 'sudo')
        stdout, stderr, returncode = run_command(module, cmd)
        results['stdout'] += stdout
        results['stderr'] += stderr

    for package in packages:
        if state == 'present':
            if check_package_installed(package):
                results['changes'][package] = 'already installed'
                continue
            cmd = ['yay', '-S', '--noconfirm', package]
        elif state == 'absent':
            if not check_package_installed(package):
                results['changes'][package] = 'not installed'
                continue
            cmd = ['yay', '-Rns', '--noconfirm', package]

        if use_sudo:
            cmd.insert(0, 'sudo')

        if module.check_mode:
            results['message'] += f"Would have run: {' '.join(cmd)}\n"
            results['changes'][package] = 'check mode'
            continue

        stdout, stderr, returncode = run_command(module, cmd)
        results['stdout'] += stdout
        results['stderr'] += stderr

        if returncode == 0:
            results['changed'] = True
            results['changes'][package] = 'changed'
        else:
            results['failed_packages'][package] = {
                'stdout': stdout,
                'stderr': stderr
            }

    if results['failed_packages']:
        module.fail_json(msg="Some packages failed to install/remove", **results)
    else:
        module.exit_json(**results)

if __name__ == '__main__':
    main()

