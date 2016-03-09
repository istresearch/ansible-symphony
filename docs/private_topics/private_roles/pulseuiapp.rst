Pulse UI App
============

Installs the Pulse UI platform.

Ansible Keys
------------

* **[pulse-ui-node]** - The machine to deploy the Pulse instance to.

UI Ports
--------

* **<pulse-ui-node>:80** - The non-secure Pulse UI.
* **<pulse-ui-node>:443** - The SSL-protected Pulse UI.

Verify Your Installation
------------------------

#. In a browser, navigate the Pulse UI website at **<pulse-ui-node>/pulse**. You should see:

.. figure:: ./img/pulse_ui_app.png
   :alt: Pulse UI App
   :align: center
   :width: 600
