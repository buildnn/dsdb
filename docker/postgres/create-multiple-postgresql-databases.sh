#!/bin/bash

set -e

function create_user_n_db() {
	local database=$(echo $1 | tr ':' ' ' | awk  '{print $1}')
	local owner=$(echo $1 | tr ':' ' ' | awk  '{print $2}')
	local passwd=$(echo $1 | tr ':' ' ' | awk  '{print $3}')
	echo "  Creating user and its db '$database'"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	    CREATE USER $owner WITH PASSWORD '$passwd';
	    CREATE DATABASE $database;
	    GRANT ALL PRIVILEGES ON DATABASE $database TO $owner;
	EOSQL
	echo "ok"
}


if [ -n "$POSTGRES_MULTIDB" ]; then
	echo "Multi-db initialization started..."
	for db in $(echo $POSTGRES_MULTIDB | tr ',' ' '); do
		create_user_n_db $db
	done
	echo "Multi-db initialization completed."
fi
	