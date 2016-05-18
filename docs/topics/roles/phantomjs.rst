PhantomJS
=======

Installs `PhantomJS <http://phantomjs.org/>`_, a headless WebKit browser.


Dependencies
------------
Microsoft TrueType fonts are installed so that rendering performed by PhantomJS can visually match what is seen in a typical browser running on Mac OSX or Windows.

The package installed is ``ttf-mscorefonts-installer``.


Ansible Keys
------------

* **[phantomjs-nodes]** - The machines to install PhantomJS binaries to.


Verify Your Installation
------------------------

#. Navigate to the installation directory ``/opt/phantomjs``

#. Run PhantomJS: ``./default/bin/phantomjs --version``