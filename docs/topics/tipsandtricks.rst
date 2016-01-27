Tips and Tricks
===============

Vagrant snapshots
-----------------

Vagrant as of version 1.8 now supports Virtualbox snapshots, which is *extremely* handy for testing.  For example, when testing Ansible code it can be useful to have a **barebones** snapshot and a **fullyloaded** snapshot to work with.  To create the snapshots:

#. ``vagrant up`` to boot your brand new clean VM's
#. ``vagrant snapshot save barebones`` to have Vagrant save the state of your clean VM's.  
#. ``ansible-playbook site-infrastructure.yml -u vagrant`` to provision your VM's.
#. ``vagrant snapshot save fullyloaded``.
   
To restore a given snapshot, run ``vagrant snapshot restore <snapshot>``.


Securing sensitive information
------------------------------

When building applications, often there are is sensitive information associated with the application, whether password information, or API keys.  Putting sensitive information in code repositories is not a good idea, even if it's private.

``ansible-vault`` to the rescue!  Ansible allows to encrypt any at AES-256 bit encryption.  Run ``ansible-vault encrypt file.yml`` to encrypt it with a password.  Make sure to use this same password for any file you encrypt in the repository.

When running Ansible, you can pass the password on the command line using ``--ask-vault-password``, or add it to a file (not checked into the repo) and use the ``--vault-password-file`` option.