from pgapi import Database
from pgapi.utils import sqlite3
import pytest
import psycopg

CREATE_TABLES = """
create table Gosh (c1 text, c2 text, c3 text);
create table Gosh2 (c1 text, c2 text, c3 text);
"""

DB_TEST_NAME = "testpgapi"

def pytest_configure(config):
    import sys

    sys._called_from_test = True


@pytest.fixture
def fresh_db():
    with psycopg.connect(f"dbname={DB_TEST_NAME}") as conn:
        cur = conn.cursor()
        cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        conn.commit()

    db = Database(f"dbname={DB_TEST_NAME}")
    return db


@pytest.fixture
def existing_db():
    raise NotImplementedError("FLO! Fix existing_db()")
    database = Database(memory=True)
    database.executescript(
        """
        CREATE TABLE foo (text TEXT);
        INSERT INTO foo (text) values ("one");
        INSERT INTO foo (text) values ("two");
        INSERT INTO foo (text) values ("three");
    """
    )
    return database


@pytest.fixture
def db_path(tmpdir):
    path = str(tmpdir / "test.db")
    db = sqlite3.connect(path)
    db.executescript(CREATE_TABLES)
    return path
