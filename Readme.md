# Installing CST-all

## Set-up guide

1. Install Ubuntu 20.10, setting hostname as required
2. `sudo apt update`
3. `sudo apt upgrade`
4. `sudo apt install openssh-server git vim`
5. `sudo systemctl enable --now ssh`
6. `ssh localhost` - if it works you can log out physically and just connect over the network from terminal boxes
7. Clone mixmixmix/dash_cst mixmixmix/monitor-eval-cst and CST-technology/cstweb
8. `sudo apt install apache2`
9. Get the box IP with `ip address`
10. On your terminal box go to your ip address in the browser of your choice - if the page says "It works", great. If not - check you haven't used https instead of old fashioned http
11. `sudo apt install php7.4 php7.4-mysql libapache2-mod-php7.4 libapache2-mod-wsgi-py3 mysql-client mysql-server phpmyadmin automysqlbackup` - this installs postfix, just use the default for the two massively pink screens that appear; after a while some pink screens will appear for phpmyadmin choose the default for both
12. `sudo apt install pipenv`
13. `sudo vim /etc/php/7.4/apache2/php.ini` - change line 388 to say `max_execution_time = 300`
14. `sudo a2enmod rewrite`
14. `sudo a2enmod wsgi`
15. `sudo vim /etc/apache2/apache2.conf` - change line 172 to say `AllowOverrise All`
16. `sudo systemctl restart apache2`
17. `cd ~/cstweb/`
18. `sudo mysql < setup_db_user.sql`
19. `sudo mysql < setup_db.sql`
20. `sudo ln -sT ~/cstweb /var/www/html/app`
21. `sudo chown -RL user:www-data /var/www/html/app` - replace `user` with your username
22. `sudo chmod -R 774 /var/www/app`
23. `sudo ln -sT ~/dash_cst/app /var/www/html/dash`
24. `sudo chown -RL user:www-data /var/www/html/dash` - replace `user` with your username
25. `sudo chmod -R 774 /var/www/html/dash`
27. `cd /var/www/html/dash`
27. `vim app.wsgi`:
```python
#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/dash")
from dash import app as application
```
28. `pipenv install --ignore-pipfile --system`
29. `sudo vim /etc/apache2/sites-available/000-default.conf`:
```
<VirtualHost *:80>
        ServerName <<REPLACE>>

        DocumentRoot /var/www/html

        <Directory /var/www/html>
                Order allow,deny
                allow from all
        </Directory>

        # Build WSGI for Flask app
        WSGIDaemonProcess app threads=5
        WSGIScriptAlias /dash /var/www/html/dash/app/app.wsgi
        WSGIApplicationGroup %{GLOBAL}

        <Directory /var/www/html/dash/app>
                WSGIProcessGroup app
                WSGIApplicationGroup %{GLOBAL}
                Order allow,deny
                allow from all
        </Directory>

        Alias /dash/static /var/www/html/dash/app/static
        <Directory /var/www/html/dash/app/static/>
                Order allow,deny
                allow from all
        </Directory>

        <Directory /var/www/html/app>
                Options Indexes FollowSymLinks
                AllowOverride All
                Require all granted
        </Directory>

        ErrorLog /var/log/apache2/error.log
        LogLevel info

        CustomLog /var/log/apache2/access.log combined
</VirtualHost>
```
30. `sudo service apache2 restart`
31. On your terminal box go to your ip address in the browser of your choice, add `/dash` - if the page works, great. If not - check you haven't used https instead of old fashioned http
31. On your terminal box go to your ip address in the browser of your choice, add `/app` - if the page works, great. If not - check you haven't used https instead of old fashioned http
