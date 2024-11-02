# ABSENSI

## Running on Live
http://103.127.138.36:8000/docs

## Requirements
- Python 3.12
- Poetry 1.8.3 (see https://python-poetry.org/docs/)
- Postgres 16

## Installation (development)
1. install all depedencies using poetry `poetry install`
1. copy .env.example to .env fill .env based on your postgres and jwt configuration (set ENVIRONTMENT as dev for development)
1. run migration `poetry run alembic -c alembic.ini upgrade head`
1. add initial data `poetry run python cli.py initial-data`
1. run the application `poetry run uvicorn main:app --port 8000 --reload`

## Demo
Data yang diseeder dan dapat digunakan adalah:
### User
- Username (email): admin@absensi.py
- Password: 12qwaszx
### Role
- Admin
- Operator
- Guru

## Testing
WARNING: menjalankan test akan menghapus semua data dan table di database pada .env! PASTIKAN TEST TIDAK DIJALANKAN DI DATABASE PRODUCTION !!!
- Run all test `poetry run pytest .`
- Run all test inside folder `poetry run pytest ./{path}/{to}/{folder}` example `poetry run pytest ./routes/tests/`
- Run all test inside file `poetry run pytest ./{path}/{to}/{folder}/{filename}.py` example `poetry run pytest ./routes/tests/test_auth.py`
- Run all test inside class `poetry run pytest ./{path}/{to}/{folder}/{filename}.py::{classname}` example `poetry run pytest ./routes/tests/test_auth.py::TestAuth`
- Run single test function `poetry run pytest ./{path}/{to}/{folder}/{filename}.py::{classname}::{function name}` example `poetry run pytest ./routes/tests/test_auth.py::TestAuth::test_login`
- Run test verbosely show print `poetry run pytest ./{path}/{to}/{folder}/{filename}.py::{classname}::{function name} -s` example `poetry run pytest ./routes/tests/test_auth.py::TestAuth::test_login -s`

## Folder Structure
- common/: untuk menyimpan fungsi yang dipakai disemua module
- migrations/: untuk menyimpan migrasi SQL
- migrations/factories/: menyimpan factory model menggunakan factory_boy
- models/: struktur tabel sql
- repository/: untuk menyimpan yang berhubunga koneksi ke database, redis, api
- routes/: menghubungkan route ke service, swagger
- schemas/: pydantic model schema response, schema request
- seeders/: menyimpan initial_data yang akan di run oleh cli.py setelah migrasi dan fungsi-fungsi untuk inisialisasi data
- .env: menyimpan konfigurasi aplikasi (dipakai ketika development saja)
- main.py: runner server
- cli.py: runner untuk typer cli
- settings.py: membaca data .env

## Migration
### Create new migration postgresql
1. Tambah atau edit file pada folder models
1. generate migration secara otomatis `poetry run alembic -c alembic.ini revision --autogenerate -m "{nama migrasi}"`. File migrasi akan ditambahkan pada folder migrations/versions.
1. review file yang digenerate oleh alembic
1. apply migrasi `poetry run alembic -c alembic.ini upgrade head`

## Deployment
### Using docker
1. Pastikan .env.example telah tercopy menjadi .env
1. Copy docker-compose.yaml.example menjadi docker-compose.yaml
1. Buka Docker Desktop
1. Buka Powershell atau Terminal
1. Pada Terminal, Masuk ke direktori Absensi yang telah terdownload
1. Pastikan Docker Engine telah run
1. Ketikkan perintah `docker-compose up -d --build`
1. Tunggu hingga selesai
1. Setelah Docker di build, silahkan buka di Browser http://localhost:8000/docs untuk menguji API
1. Untuk menghentikan service, jalankan `docker-compose down`
### Note:
- Setelah docker dibuild, silahkan jalankan perintah `docker-compose up -d`
- Untuk mengecek apakah service telah berjalan pada docker, ketikkan perintah `docker-compose ps`