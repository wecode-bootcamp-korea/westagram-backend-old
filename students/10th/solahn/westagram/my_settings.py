DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.mysql',
          'NAME': 'mysql_test',
          'USER': 'root',
          'PASSWORD': '1234',
          'HOST':'localhost',
          'PORT': '3306',
          'OPTIONS':{
                  'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
              }
       }
 }
