# Language quiz back end

This is the back end of a language quiz application made with Django 3.1. The front end is made with Vue.js and the Github repository is [here](https://github.com/Mutusen/language-quiz-vue).

The quiz application is demonstrated [here](https://quiz.apprenti-polyglotte.net/).

## How to install locally

Rename `languagequiz/local_settings.py.template` to `local_settings.py` and change your configuration there.
```

## Deploying

Create the virtual environment in the project root folder with:

```console
$ python3 -m venv venv
```

Install the required packages:

```console
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Apply migrations, collect static files, create a superuser:

```console
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py createsuperuser
```

## Apache configuration

Here is an example of working Apache config:

```apache
<VirtualHost *:80>
	ServerName languagequiz.domain.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/languagequiz
	
	Alias /static /var/www/languagequiz/static

	<Directory /var/www/languagequiz/static>
		Require all granted
	</Directory>
	
	<Directory /var/www/languagequiz/languagequiz>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>
	
	WSGIDaemonProcess quiz python-home=/var/www/languagequiz/venv python-path=/var/www/tradukejo
	WSGIProcessGroup quiz
	WSGIScriptAlias / /var/www/languagequiz/languagequiz/wsgi.py

	ErrorLog ${APACHE_LOG_DIR}/languagequiz.error.log
	CustomLog ${APACHE_LOG_DIR}/languagequiz.access.log combined
</VirtualHost>
```

Do not forget to reload Apache after each change of Python files:

```console
# systemctl reload apache2
```
