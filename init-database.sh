#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER sw_app WITH ENCRYPTED PASSWORD '123456';
    CREATE DATABASE starwars;
    GRANT ALL PRIVILEGES ON DATABASE starwars TO sw_app;
EOSQL
