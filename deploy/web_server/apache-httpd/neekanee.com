<VirtualHost *:80>
     ServerAdmin webmaster@neekanee.com
     ServerName neekanee.com
     ServerAlias www.neekanee.com

     DocumentRoot /srv/www/neekanee.com/public_html/

     Alias /robots.txt /srv/www/neekanee.com/public_html/robots.txt
     Alias /media/admin /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media/
     Alias /media /srv/www/neekanee.com/public_html/media/
     Alias /favicon.ico /srv/www/neekanee.com/public_html/favicon.ico

     WSGIScriptAlias / /srv/www/neekanee.com/jobsearch/django.wsgi
     <Directory /srv/www/neekanee.com/jobsearch/>
       Order allow,deny
       Allow from all
     </Directory>

     <Location "/admin">
       RewriteEngine On
       RewriteCond %{REQUEST_URI} ^/admin
       RewriteRule .* https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
     </Location>

     <Location "/account">
       RewriteEngine On
       RewriteCond %{REQUEST_URI} ^/account
       RewriteRule .* https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
     </Location>

     ErrorLog /srv/www/neekanee.com/logs/error.log
     CustomLog /srv/www/neekanee.com/logs/access.log combined
</VirtualHost>

<VirtualHost 69.164.219.250:443>
     SSLEngine On

     SSLCertificateFile /etc/apache2/ssl/apache.pem
     SSLCertificateKeyFile /etc/apache2/ssl/apache.key

     ServerAdmin support@mydomain.com
     ServerName neekanee.com
     ServerAlias www.neekanee.com

     DocumentRoot /srv/www/neekanee.com/public_html/

     Alias /robots.txt /srv/www/neekanee.com/public_html/robots.txt
     Alias /media/admin /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media/
     Alias /media /srv/www/neekanee.com/public_html/media/
     Alias /favicon.ico /srv/www/neekanee.com/public_html/favicon.ico

     WSGIScriptAlias / /srv/www/neekanee.com/jobsearch/django.wsgi

     ErrorLog /srv/www/neekanee.com/logs/error.log
     CustomLog /srv/www/neekanee.com/logs/access.log combined
</VirtualHost>
