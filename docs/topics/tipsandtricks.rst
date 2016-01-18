Tips and Tricks
===============

When building applications, often there are is sensitive information associated with the application, whether password information, or API keys.  Putting sensitive information in code repositories is not a good idea, even if it's private.

``ansible-vault`` to the rescue!  Ansible allows to encrypt any at AES-256 bit encryption.  Run ``ansible-vault encrypt file.yml`` to encrypt it with a password.  Make sure to use this same password for any file you encrypt in the repository.

When running Ansible, you can pass the password on the command line using ``--ask-vault-password``, or add it to a file (not checked into the repo) and use the ``--vault-password-file`` option.