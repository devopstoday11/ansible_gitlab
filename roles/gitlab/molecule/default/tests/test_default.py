import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_package(host):
    if host.system_info.distribution == 'centos':
        pkg = ["gitlab-ce"]
    else:
        pkg = ["gitlab-ce"]

    assert host.package(pkg).is_installed


def test_service_is_running(host):
    assert host.service('gitlab').is_running
    assert host.service('gitlab').is_enabled


def test_sockets_open(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening


def test_file_exist(host):
    f = host.file("/etc/gitlab/gitlab.rb")
    assert f.exists
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.contains("ansible manage")
