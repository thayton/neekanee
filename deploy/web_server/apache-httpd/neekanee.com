<VirtualHost *:80>
     ServerAdmin webmaster@neekanee.com
     ServerName neekanee.com
     ServerAlias www.neekanee.com

     DocumentRoot /srv/www/neekanee.com/public_html/

     Alias /robots.txt /srv/www/neekanee.com/public_html/robots.txt
     Alias /media/admin /usr/local/lib/python2.6/dist-packages/django/contrib/admin/static/admin/
     Alias /media /srv/www/neekanee.com/public_html/media/
     Alias /favicon.ico /srv/www/neekanee.com/public_html/favicon.ico

     WSGIScriptAlias / /srv/www/neekanee.com/neekanee/neekanee/django.wsgi
     <Directory /srv/www/neekanee.com/neekanee/neekanee/>
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

     RewriteMap lowercase int:tolower

     # http://neekanee.com to http://www.neekanee.com
     Options +FollowSymLinks
     RewriteEngine On
     RewriteCond %{HTTP_HOST} ^neekanee.com [NC]
     RewriteRule (.*) http://www.neekanee.com%{REQUEST_URI} [R=301,L]

     RewriteCond %{REQUEST_URI} ^/jobs-at-universiy-of-miami
     RewriteRule jobs-at-universiy-of-miami jobs-at-university-of-miami [R=301,L]

     RewriteCond %{REQUEST_URI} ^/companies/universiy-of-miami
     RewriteRule /companies/universiy-of-miami /companies/university-of-miami [R=301,L]

     ErrorLog /srv/www/neekanee.com/logs/error.log
     CustomLog /srv/www/neekanee.com/logs/access.log combined
</VirtualHost>

<VirtualHost 69.164.219.250:443>
     SSLEngine On

     SSLCertificateFile /etc/apache2/ssl/www.neekanee.com.crt
     SSLCertificateKeyFile /etc/apache2/ssl/www.neekanee.com.key
     SSLCertificateChainFile /etc/apache2/ssl/intermediate.crt

     ServerAdmin support@mydomain.com
     ServerName neekanee.com
     ServerAlias www.neekanee.com

     DocumentRoot /srv/www/neekanee.com/public_html/

     Alias /robots.txt /srv/www/neekanee.com/public_html/robots.txt
     Alias /media/admin /usr/local/lib/python2.6/dist-packages/django/contrib/admin/static/admin/
     Alias /media /srv/www/neekanee.com/public_html/media/
     Alias /favicon.ico /srv/www/neekanee.com/public_html/favicon.ico

     WSGIScriptAlias / /srv/www/neekanee.com/neekanee/neekanee/django.wsgi

     Options +FollowSymLinks
     RewriteEngine On
     RewriteCond %{HTTPS} on
     RewriteCond %{REQUEST_URI} !^/admin
     RewriteCond %{REQUEST_URI} !^/account
     RewriteCond %{REQUEST_URI} !^/media/admin/
     RewriteCond %{REQUEST_URI} !^/media/
     RewriteRule (.*) http://%{HTTP_HOST}%{REQUEST_URI}

     ErrorLog /srv/www/neekanee.com/logs/error.log
     CustomLog /srv/www/neekanee.com/logs/access.log combined
</VirtualHost>
