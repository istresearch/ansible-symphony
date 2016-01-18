# -*- mode: ruby -*-
# vi: set ft=ruby :

CENTOS_BOX = 'box-cutter/centos65'
UBUNTU_BOX = 'ubuntu/trusty64'

Vagrant.require_version ">= 1.8.1"

Vagrant.configure(2) do |config|

  # Configure general VM options
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 4096
    vb.cpus = 4
  end

  # Configuration applying to all VMs
  config.vm.provision :shell, inline: "cat /vagrant/vagrant_hosts > /etc/hosts"
  config.vm.provision :shell, inline: "cat /vagrant/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys"

  # Set up IP addresses and hostnames from 'hosts' file
  # It assumes 'localhost' is on the first line
  hosts = File.readlines('vagrant_hosts')
  hosts[1..-1].each do |h|
    unless /(#|^\s*$)/.match(h)   # ignore commented out hosts and blank lines
      config.vm.define h.split(%r{\s+})[1] do |node|
        if h.split(%r{\s+})[-1] == 'centos'
          node.vm.box = CENTOS_BOX
        elsif h.split(%r{\s+})[-1] == 'ubuntu'
          node.vm.box = UBUNTU_BOX
          node.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
        end
        node.vm.hostname = h.split(%r{\s+})[1]
        node.vm.network "private_network", ip: h.split(%r{\s+})[0]
        node.vm.provision "shell", inline: "service supervisord restart || true", run: "always"
      end
    end
  end
end
