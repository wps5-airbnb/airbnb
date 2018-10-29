# airbnb lmitating server

## Install Dependencies

* Ubuntu Install

  ```bash
  sudo apt install build-essential
  sudo apt-get install libmysqlclient-dev
  ```

* Anaconda

  ```bash
  wget https://repo.continuum.io/archive/Anaconda3-4.4.0-Linux-x86_64.sh 
  chmod +x Anaconda3-4.4.0-Linux-x86_64.sh
  Anaconda3-4.4.0-MacOSX-x86_64.sh
  ```

* creating virtual environment for python & activate

  ```bash
  conda create -n airbnb python python=3.6.2
  source activate airbnb
  ```

* install python dependencies in local(PIP)

  ```
  pip install -r .requirements/debug.txt
  ```



## Environment Variable Settings

* create `.config_secret` folder in `airbnb` folder

* create `settings_common.json` in `.config_secret` folder and then write like a below.

  ```json
  {
    "django": {
      "secret_key": "put django secret key here",
      "default_superuser": {
        "email": "airbnb_admin@gmail.com",
        "password": "12345678"
      }
    },
    "facebook": {
      "facebook_app_id": "app id",
      "facebook_secret_code": "secret_code"
    }
  }
  ```

* also create `settings_debug.json` in `.config_secret` folder and then write like a below.

  ```json
  {
    "django": {
      "allowed_hosts" : [
        "localhost",
        "127.0.0.1",
        "testserver"
      ]
    }
  }
  ```

* activate environment variables

  ```bash
  cd django_app
  export DJANGO_SETTINGS_MODULE=config.settings.debug
  ```

  

## Databases

* for local databases

  ```bash
  cd django_app
  ./manage.py migrate
  ```

* create superuser

  ```
  ./manage.py createsu
  ```

  then, you can create ID: airbnb_admin@gmail.com PW: camp1017