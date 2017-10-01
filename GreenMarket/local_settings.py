# Replace this values with your local settings
import os
import dj_database_url

# Please change this value when deploying to heroku
is_deployed = False

if is_deployed:
    DATABASE_DICT = dj_database_url.config(default=os.environ.get('DATABASE_URL', ''))
else:
    DATABASE_DICT = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'green_market3',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
