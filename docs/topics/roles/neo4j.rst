Neo4j
=====

Deploys `Neo4j <http://neo4j.com/>`_ Community Edition.

Ansible Keys
------------

* **[neo4j-node]** - The machine to deploy the Neo4j instance to. Note that because we are using the community edition, multiple machines here specify multiple distinct instances, no cluster support.


UI Ports
--------

* **<neo4j_node>:7474** - The main Neo4j UI

Verify Your Installation
------------------------

#. Navigate to the main user interface at port ``7474``

#. Log in as user ``neo4j``, password is located in the comments at ``roles/neo4j/defaults/main.yml`` file.

#. In the command line at the top, run ``:play movie graph`` and follow the tutorial.
