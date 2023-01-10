# skiwidgets build documentation


At a bash console as root. Update, install pip and venv.

apt-get update

apt-get upgrade

apt-get install python3-pip

apt-get install python3-venv


# Firewall

On an Ubuntu instance in Oracle cloud, firewall management is required, this is probably not needed on other systems.

apt-get install firewalld

systemctl enable firewalld

and for testing purposes:

firewall-cmd --permanent --zone=public --add-port=8000/tcp

and for normal operation:

firewall-cmd --permanent --zone=public --add-port=80/tcp

firewall-cmd --permanent --zone=public --add-port=443/tcp

firewall-cmd --reload


# add user bernard who will run the skiwidgets site

adduser bernard

record the password


## Install git, and clone skiwidgets repository

Then as user bernard create an ssh key

runuser -l bernard

# For full github write access

ssh-keygen -t rsa -b 4096 -C "set email address here"

copy contents of .ssh/id_rsa.pub to github

# clone the skiwidgets repository

git clone git@github.com:bernie-skipole/skiwidgets.git

copy /home/bernard/skiwidgets to /home/bernard/www without the .git and .gitignore

(this rsync command can be used to update /www whenever git pull is used to update /skiwidgets)

rsync -ua --exclude=".*" ~/skiwidgets/ ~/www/

The file ~/www/skiwidgets.py should be edited to remove skiadmin, and enable waitress rather than the development server.

The project should be served on port 8000

# clone the cloudeserver repository

git clone git@github.com:bernie-skipole/cloudserver.git

copy /home/bernard/cloudserver to /home/bernard/cserv without the .git and .gitignore

(this rsync command can be used to update /cserv whenever git pull is used to update /cloudserver)

rsync -ua --exclude=".*" ~/cloudserver/ ~/cserv/

The file ~/cserv/cloudserver.py should be edited to remove skiadmin, and enable waitress rather than the development server.

The project should be served on port 8001


# Create a python venv

Running skiwidgets in a python virtual environment is not strictly necessary, but I prefer to do it.

python3 -m venv ~/skiwidgetenv

source skiwidgetenv/bin/activate

The skiwidgets Python program requires the skipole package and waitress

pip install skipole

pip install waitress

It should now be possible to run skiwidgets

python ~/www/skiwidgets.py

It should also be possible to run this without starting the virtual env using

skiwidgetenv/bin/python www/skiwidgets.py

Use ctrl-c to exit, and set up a service to run this automatically

## Install skiwidgets.service

Edit the www/skiwidgets.service file 

so the ExecStart line reads:

ExecStart=/home/bernard/skiwidgetenv/bin/python /home/bernard/www/skiwidgets.py

as root, copy the file

cp /home/bernard/www/skiwidgets.service /lib/systemd/system

Enable the service with

systemctl daemon-reload

systemctl enable skiwidgets.service

systemctl start skiwidgets

This starts /home/bernard/www/skiwidgets.py on boot up.


## Install cloudserver.service

Edit the cserv/cloudserver.service file 

so the ExecStart line reads:

ExecStart=/home/bernard/skiwidgetenv/bin/python /home/bernard/cserv/cloudserver.py

as root, copy the file

cp /home/bernard/cserv/cloudserver.service /lib/systemd/system

Enable the service with

systemctl daemon-reload

systemctl enable cloudserver.service

systemctl start cloudserver

This starts /home/bernard/cserv/cloudserver.py on boot up.

## Install nginx

apt-get install nginx

So nginx is running and serving a default web page. We now need it to proxy requests to the backend servers. The ubuntu system has two directories:

/etc/nginx/sites-available

/etc/nginx/sites-enabled

You will see under sites-available a default configuration file, and under sites-enabled a link to that file, which is the current enabled default site.

Copy skiwidgets.conf to sites-available

Then, within directory /etc/nginx/sites-enabled delete the default link, and create a new link to skiwidgets.conf:

rm default

ln -s /etc/nginx/sites-available/skiwidgets.conf /etc/nginx/sites-enabled/

Now reboot the server or restart nginx with command "service nginx restart"




