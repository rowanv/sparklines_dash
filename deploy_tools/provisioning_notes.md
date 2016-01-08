Provisioning the dashboard
==========================

## Required packages:

* nginx
* Python 3
* Git
* Pip
* virtualenv

e.g., on Ubuntu:

	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with domain name, e.g. staging.my-domain.com


# Automated deploy
## on my machine

fab deploy --host=rowan@sparklines-dash.rowanv.com


## Then on the actual server, within source for the website

sed "s/SITENAME/sparklines-dash.rowanv.com/g" \
    deploy_tools/nginx.template.conf | sudo tee \
    /etc/nginx/sites-available/sparklines-dash.rowanv.com

sudo ln -s ../sites-available/sparklines-dash.rowanv.com \
    /etc/nginx/sites-enabled/sparklines-dash.rowanv.com

sed "s/SITENAME/sparklines-dash.rowanv.com/g" \
    deploy_tools/gunicorn-upstart.template.conf | sudo tee \
    /etc/init/gunicorn-sparklines-dash.rowanv.com.conf

sudo service nginx reload
#sudo start gunicorn-sparklines-dash.rowanv.com
# or once have started:
sudo restart gunicorn-sparklines-dash.rowanv.com
# Actually, currently starting gunicorn with:
# ../virtualenv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app -D
# To view running gunicorn processes:
# ps ax|grep gunicorn
