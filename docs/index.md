# Container build documentation

This documents creating a container on webparametrics.co.uk, for the full build of the server, see

[https://bernie-skipole.github.io/webparametrics/](https://bernie-skipole.github.io/webparametrics/)

This container will serve widgets produced by the skipole framework.

On server webparametrics.co.uk, as user bernard

lxc launch ubuntu:20.04 skiwidgets

lxc list

This gives container ip address 10.105.192.??

lxc exec skiwidgets -- /bin/bash

This gives a bash console as root in the skiwidgets container. Update, install pip and add a user, in this case 'bernard'.

apt-get update

apt-get upgrade

apt-get install python3-pip

adduser bernard

record the password


## Install git, and clone skiwidgets repository

Then as user bernard create an ssh key

runuser -l bernard

ssh-keygen -t rsa -b 4096 -C "bernie@skipole.co.uk"

copy contents of .ssh/id_rsa.pub to github

clone any required repositories

git clone git@github.com:bernie-skipole/skiwidgets.git

copy /home/bernard/skiwidgets to /home/bernard/www without the .git and .gitignore
(this rsync command can be used to update /www whenever git pull is used to update /skiwidgets)

rsync -ua --exclude=".*" ~/skiwidgets/ ~/www/

The skiwidgets Python program requires the skipole package
and waitress

python3 -m pip install --user skipole

python3 -m pip install --user waitress

It should now be possible to run skiwidgets

python3 ~/www/skiwidgets.py

And you should get the message

Serving skiwidgets on port 8000

Use ctrl-c to exit, and set up a service to run this automatically

## Install skiwidgets.service

as root, copy the file

cp /home/bernard/www/skiwidgets.service /lib/systemd/system

Enable the service with

systemctl daemon-reload

systemctl enable skiwidgets.service

systemctl start skiwidgets

This starts /home/bernard/www/skiwidgets.py on boot up.

The site will be visible at.

[https://webparametrics.co.uk/skiwidgets](https://webparametrics.co.uk/skiwidgets)



