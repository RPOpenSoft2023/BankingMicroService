# BankingMicroService
## Required Packages:
- View [requirements.txt](https://github.com/RPOpenSoft2023/BankingMicroService/blob/main/requirements.txt)

## Instructions to build & install the software:
- Clone the repository

  ```
  git clone https://github.com/RPOpenSoft2023/BankingMicroService.git
  ```
- Install Python 3.10 from source

  ```
  https://www.python.org/downloads/release/python-3109/
  ```
- Install virtualenv

  ```
  pip install virtualenv
  ```
- Create virtual environment

  ```
  python -m virtualenv myenv
  ```
- Activate the virtual environment

  Windows:
  
  ```
  ./myenv/Scripts/activate
  ```
  Linux:
  
  ```
  source myenv/bin/activate
  ```
- Add environment variables for connecting to Postgres Database and Users Microservice token verification
  
  Windows:
  
  ```
  [System.Environment]::SetEnvironmentVariable('DATABASE_USER', 'postgres')
  [System.Environment]::SetEnvironmentVariable('DATABASE_PASSWORD', 'demo')
  [System.Environment]::SetEnvironmentVariable('DATABASE_NAME', 'banking-db')
  [System.Environment]::SetEnvironmentVariable('USERS_MICROSERVICE_LINK', 'http://localhost:8000/user/api/verify_token')
  ```
  Linux:
  
  ```
  export DATABASE_USER='postgres'
  export DATABASE_PASSWORD='demo'
  export DATABASE_NAME='banking-db'
  export USERS_MICROSERVICE_LINK='http://localhost:8000/user/api/verify_token'
  ```
- Change directory to the cloned folder i.e. BankingMicroService

  ```
  cd BankingMicroService
  ```
- Install all the required packages

  ```
  pip install -r requirements.txt
  ```
- Make migrations

  ```
  python manage.py makemigrations
  ```
- Migrate to create the tables inside the database

  ```
  python manage.py migrate
  ```
- Create superuser to use django admin panel

  ```
  python manage.py createsuperuser
  ```
  
## Instructions to run the software:
- Run the server

  ```
  python manage.py runserver 8001
  ```
- To access the django admin panel use following url

  ```
  localhost:8001/admin
  ```
