# Configures a web server for deployment of web_static.

# Nginx configuration file
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://jtechofficial.tech/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Install Nginx package
package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
} ->

# Create directories
file { '/data':
  ensure => 'directory',
} ->

file { '/data/web_static':
  ensure => 'directory',
} ->

file { '/data/web_static/releases':
  ensure => 'directory',
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory',
} ->

file { '/data/web_static/shared':
  ensure => 'directory',
} ->

# Create index.html for the test release
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>\n",
} ->

# Create a symbolic link to the test release
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
} ->

# Change ownership of /data/ to 'ubuntu:ubuntu'
exec { 'chown -R ubuntu:ubuntu /data/':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => ['/usr/bin/', '/usr/local/bin/', '/bin/'],
} ->

# Create necessary directories under /var/www/
file { '/var/www':
  ensure => 'directory',
} ->

file { '/var/www/html':
  ensure => 'directory',
} ->

# Create index.html and 404.html files
file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "<html>
  <head>
  </head>
  <body>
    Hello World!
  </body>
</html>\n",
} ->

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
} ->

# Configure Nginx default site
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
} ->

# Restart Nginx service
exec { 'nginx restart':
  command => '/etc/init.d/nginx restart',
  }
