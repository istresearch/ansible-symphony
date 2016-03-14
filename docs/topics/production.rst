Running in Production
=====================

Running in production shouldn't be much different than running on your Vagrant VM's.  Just fill out your ``production.inventory`` inventory file, set up your **group_vars** if necessary, and pass ``-i production.inventory`` as part of the ``ansible-playbook`` command.