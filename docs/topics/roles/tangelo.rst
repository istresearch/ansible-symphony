Tangelo
=======

Installs the `Tangelo Web Framework <http://tangelo.readthedocs.org>`_.


Ansible Keys
------------

* **[tangelo-node]** - The machine to deploy the Tangelo web server instance to. Multiple machines here specify multiple distinct instances, no cluster support.

UI Ports
--------

* **<tangelo_node>:9090** - The main Tangelo web port

Verify Your Installation
------------------------

#. Navigate to the main web server host at port ``9090``

#. The default page should display the following

    ::

        It works!

        This a dummy landing page for your Tangelo Web Server.