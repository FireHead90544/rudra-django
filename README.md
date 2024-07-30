# rudra-django
My Awesome Portfolio Website Built w/ Django & TailwindCSS

# Features
- Awesome & Neat UI
- Blog w/ likes & comments
- IP based blogpost view count
- A fully fledged authentication system
- A cool dashboard to manage everything
- A neat portfolio with project showcase
- Recaptcha enabled contact/hire-me form
- Hire requests integration w/ discord channel
- And a lot more cool stuffs which you should yourself figure out.

# Installation
The following steps are tested against ubuntu 20.04 LTS.
- Update the mirrors & packages
  ```bash
  sudo apt update && sudo apt upgrade -y && sudo apt update
  ```
- Install `pip` & `virtualenv`
  ```bash
  sudo apt install python3-pip python3-virtualenv -y
  ```
- Clone the repository
  ```bash
  git clone https://github.com/FireHead90544/rudra-django
  ```
- Activate the virtualenv & Install the requirements
  ```bash
  cd rudra-django && virtualenv venv && source venv/bin/activate && sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib -y && pip install -r requirements.txt
  ```
- Setup Postgres Database
  ```bash
  sudo -u postgres psql
  ```
  ```sql
  CREATE DATABASE <DB_NAME>;
  CREATE USER <DB_USER> WITH PASSWORD '<YOUR_PASSWORD>';
  ALTER ROLE <DB_USER> SET client_encoding TO 'utf8';
  ALTER ROLE <DB_USER> SET default_transaction_isolation TO 'read committed';
  ALTER ROLE <DB_USER> SET timezone TO 'UTC';
  GRANT ALL PRIVILEGES ON DATABASE <DB_NAME> TO <DB_USER>;
  \q
  ```
- Set up environment variables however you prefer (an `example.env` is present in the repository as a template).
- Create the migrations, admin user & start the server.
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver 0.0.0.0:8000
  ```
- Set `DJANGO_DEBUG` environment variable to `False`.
- Collect the static files so that it can be served using nginx.
  ```bash
  python manage.py collectstatic
  ```
- Create a gunicorn socket and a service to use that socket.
  ```bash
  sudo nano /etc/systemd/system/gunicorn.socket
  ```
  ```ini
  [Unit]
  Description=Django Gunicorn Socket
  
  [Socket]
  ListenStream=/run/gunicorn.sock
  
  [Install]
  WantedBy=sockets.target
  ```
  ```bash
  sudo nano /etc/systemd/system/gunicorn.service
  ```
  ```ini
  [Unit]
  Description=Django Gunicorn Daemon
  Requires=gunicorn.socket
  After=network.target
  
  [Service]
  User=<SSH_USER>
  Group=www-data
  WorkingDirectory=/home/<SSH_USER>/rudra-django
  ExecStart=/home/<SSH_USER>/rudra-django/venv/bin/gunicorn \
            --access-logfile - \
            --workers 3 \
            --bind unix:/run/gunicorn.sock \
            rudra.wsgi:application
  
  [Install]
  WantedBy=multi-user.target
  ```
- Start and enable the service you just created
  ```bash
  sudo systemctl start gunicorn.socket
  sudo systemctl enable gunicorn.socket
  sudo systemctl status gunicorn.socket
  sudo systemctl status gunicorn
  sudo systemctl daemon-reload
  sudo systemctl restart gunicorn
  ```
- Install nginx
  ```bash
  sudo apt install nginx -y
  ```
- Serve the gunicorn socket using nginx
  ```bash
  sudo nano /etc/nginx/sites-available/<SITE_NAME>
  ```
  ```nginx
  server {
    listen 80;
    server_name <EXTERNAL_IP>;
    client_max_body_size 500M;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/<SSH_USER>/rudra-django;
    }

    location /media/ {
        root /home/<SSH_USER>/rudra-django;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
  }
  ```
- Enable the site and allow nginx behind firewall
  ```bash
  sudo ln -s /etc/nginx/sites-available/<SITE_NAME> /etc/nginx/sites-enabled
  sudo nginx -t
  sudo systemctl restart nginx
  sudo ufw allow 'Nginx Full'
  ```
- If you have custom domains, link them by setting `server_name domain.tld www.domain.tld` in the enabled site configuration. Make sure to update the `ALLOWED_HOSTS` environment variable too & restart the server.
  ```bash
  sudo systemctl restart gunicorn nginx
  ```
- If you linked the domains, enable ssl
  ```bash
  sudo apt install certbot python3-certbot-nginx
  sudo certbot --nginx -d domain.tld -d www.domain.tld
  ```
- Redirect `http` to `https` by editing the nginx site configuration so that it looks like this.
  ```bash
  sudo nano /etc/nginx/sites-available/<SITE_NAME>
  ```
  ```nginx  
  server {
    server_name domain.tld www.domain.tld;
    client_max_body_size 500M;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/<SSH_USER>/rudra-django;
    }

    location /media/ {
        root /home/<SSH_USER>/rudra-django;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/domain.tld/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/domamin.tld/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
  }
  
  server {
      if ($host = domain.tld) {
          return 301 https://$host$request_uri;
      }
      if ($host = www.domain.tld) {
        return 301 https://$host$request_uri;
      }
  
      listen 80;
      server_name domain.tld www.domain.tld;
      return 404; # managed by Certbot
  }
  ```
- Test the automatic ssl renewal utlity & restart the server.
  ```bash
  sudo certbot renew --dry-run
  sudo systemctl restart gunicorn nginx
  ```

Even though I have spoonfed almost everything which took me some time to figure out when I first deployed this website, but that made me learn so many stuffs. I'd suggest you to do the same before blindly following these instructions. And as always, if you get any issues you are free to create an issue or you can leverage some LLM to help you out.
And to end with, I don't plan on but you can compile all this in a single bash script and automate everything with a single script execution :)
