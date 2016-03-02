Spark
========

.. warning:: The documentation for this role is not complete.


Ansible Keys
------------


Ports
-----

* **<master>:7077** - Spark Master Port

* **<master>:18080** - Spark Master UI

* **<spark-driver>:4040** - Spark Application UI. Note that this auto-increments based on the number of jobs running concurrently per spark-driver. The first job on driver-1 takes 4040 and the second on driver-1 takes 4041. However, if a new job is run on driver-2 then its application UI runs on <driver-2>:4040.

Verify Your Installation
------------------------

#. step 1

#. Change user to ``user``

# other steps
