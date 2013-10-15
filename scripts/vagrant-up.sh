#! /bin/bash

echo "-----> Setting up Vagrant"
vagrant up

echo "-----> Waiting for VirtualBox Additions to finish installing after reboot"
sleep 30 # Wait for box to reboot after vagrant up is finished

while [ ! `vagrant ssh --command "pgrep -f VBoxService"` ]; do
    sleep 5
    echo "Waiting.."
done

vagrant reload

echo "-----> Building docker containers"
vagrant ssh --command "/bin/bash /vagrant/scripts/docker-up.sh"

echo "Done!"