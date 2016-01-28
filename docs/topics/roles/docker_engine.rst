Docker Engine
=============

Installs `Docker Engine <https://www.docker.com/products/docker-engine>`_

Ansible Keys
------------

* **[docker-engine]** - The hosts to provision docker engine on to.


Verify Your Installation
------------------------

#. SSH on to your machine

#. Change user to ``root``

#. Run

::

    docker run docker/whalesay cowsay hello
