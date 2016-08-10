-----------------------------------------------------------------------------
Running
From the ansible-symphony-ist root directory:
vagrant up
confirm ssh works
ansible-playbook site-infrastructure.yml -u vagrant --tags deps-grawler --limit grawler-nodes

cp private_roles/grawler/templates/grawler-config-deploy.yml .
ansible-playbook -u vagrant grawler-config-deploy.yml

-----------------------------------------------------------------------------
Testing
Note - to be updated when REST API becomes available

ssh vagrant@vagrant-ist-01
sudo su
tail -f /var/log/supervisor/00*

Do the same in a different terminal, except tail the 01 process
tail -f /var/log/supervisor/01*

This can be done on your VM if git installed, or on your dev box:
git clone git@github.com:istresearch/grawler.git
cd grawler/grawler

Open the python shell, python

from graph import Facebook

The following commands are examples of adding a crawl for the given facebook page. The crawls get added to the shared_graph_q in redis on vagrant-ist-01
Facebook('00').crawl(id="ist.research.corp")
Facebook('00').crawl(id="BenenatiLaw")
Facebook('00').crawl(id="beregovichlaw")
Facebook('00').crawl(id="coyelawfirm")
Facebook('00').crawl(id="381837098464")
Facebook('00').crawl(id="ChaseLawAZ")

