\set PG_USER `python -c "import os; print(os.getenv('PG_USER'))"`
\set PG_DB `python -c "import os; print(os.getenv('PG_DB'))"`
\set PG_PASS `python -c "import os; print(os.getenv('PG_PASS'))"`

CREATE USER :PG_USER WITH PASSWORD :PG_PASS;
CREATE DATABASE :PG_DB;
GRANT ALL PRIVILEGES ON DATABASE :PG_DB TO :PG_USER;
