
![Logo](https://user-images.githubusercontent.com/40059374/244954060-9bca36cf-8d66-4165-99b2-1772f8cc8d44.png)


# Financeapp.tel

Personal Finance app that will help you manage your Personal finance. this app is still in development, if you want to contribute contact me on my email mentioned below in the Auth section.


## Prerequisites 
1. Python 3.9 + 
2. Django 4
3. libmysql-client
5. Mysql 5.6 + 

## Installation

1. make sure that you have Prerequisites installed 

```bash
  sudo apt install libmysqlclient-dev
  sudo apt istall python3.10
  sudo apt install python3-pip
  sudo apt install mysql-server

```
2. now clone this repo 
```bash
    git clone https://github.com/raj1rana/financeapp_tel.git
    cd financeapp_tel

```
3. python virtual enviroment setup 
```bash
    pip3 install virtualenv 
    virtuaenv venv
    source venv/bin/activate # activate the virtual enviroment 
```

4. setting up the app and env 
```bash
    echo "DB_USER=" >> .env  
    echo "DB_HOST=" >> .env
    echo "DB_PASS=" >> .env
    echo "DB_NAME=" >> .env
    echo "DB_PORT=" >> .env
    echo "SECRET_KEY=" >> .env
    echo "APP_URL=http://localhost:8000" >> .env
```
- Create app key with this script 
```bash
    python key_generate.py # this command will updat ehe APP_URL in .env 
```
- then open the .env file in any text editor and add he rest of the info like DB_HOST, DB_NAME etc..

5. after setting up .env install dependencies 
```bash
    pip install -r requirements.txt  
```

6. run the migrations 
```bash
    python manage.py makemigrations
    python manage.py migrate
```
7. create a superuser for yourself
```bash
    python manage.py createsuperuser
    # provide name, email and password
```
8. Enjoy the app 
```bash
    python manage.py runserver
```

#### NOTE:- will soon release docs for production deployment 
## License

[AApache License]( http://www.apache.org/licenses/)


## Authors

- [@raj1rana](https://www.github.com/raj1rana)


## Screenshot

![App Screenshot](https://user-images.githubusercontent.com/40059374/244955850-1c3d70d8-a36a-4da7-a59b-50678342f62a.svg)

