# BankingMicroService

## Installation using virtualenv package:
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
- Change directory to the cloned folder i.e. ApnaInsti_deployed

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
- Run the server

  ```
  python manage.py runserver
  ```
- To access the django admin panel use following url

  ```
  localhost:8001/admin
  ```
