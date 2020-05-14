import sqlalchemy
from sqlalchemy import exc
from modules.config import DB_USER, DB_PASS, DB_NAME, CLOUD_SQL_CONNECTION_NAME


db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        query={"unix_socket": "/cloudsql/{}".format(CLOUD_SQL_CONNECTION_NAME)},
    ),
)


def create_table(table_name):
    """
    Creates a table based on the given table name.
    """

    try:
        with db.connect() as conn:
            conn.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} "
                "(id int NOT NULL AUTO_INCREMENT, title CHAR(30) NOT NULL UNIQUE, details VARCHAR(3000), PRIMARY KEY (id));"
            )
    except Exception as e:
        print("ERROR create", e)


def insert_record(table_name, **properties):
    """
    Inserts a new record into the given table.
    """

    fields = tuple(key for key in properties)
    values = tuple(value for value in properties.values())
    query = f"INSERT INTO {table_name} (title, details) VALUES {values};"

    try:
        with db.connect() as conn:
            return conn.execute(query)
    except exc.IntegrityError:
        raise Exception(f"Record {values[0]} already exists.")
    except exc.DataError:
        raise Exception("Text is too long.")


def update_record(table_name, **properties):
    """
    Updates an existing record with the given properties.
    """

    record_id = properties.get("id")
    title = properties.get("title")
    details = properties.get("details")
    query = f"UPDATE {table_name} \
             SET title = '{title}', details = '{details}' \
             WHERE id = '{record_id}';"

    try:
        with db.connect() as conn:
            conn.execute(query)
    except exc.IntegrityError:
        raise Exception(f"Record {title} already exists.")


def search_table(table_name, *columns):
    """
    Searches the table for specific column(s).
    """

    with db.connect() as conn:
        columns = ", ".join(columns) if len(columns) > 1 else columns[0]
        records = conn.execute(f"SELECT {columns} FROM {table_name};").fetchall()
    return records


def show_record(table_name, title):
    """
    Selects one specific record from the table.
    """

    with db.connect() as conn:
        try:
            records = conn.execute(f"SELECT id, title, details FROM {table_name} WHERE title = '{title}';").fetchall()[0]
        except Exception as err:
            records = str(err)
    return records


def search_record(table_name, title):
    """
    Searches for records with values similar to the given title.
    """

    with db.connect() as conn:
        records = conn.execute(f"SELECT title, details FROM {table_name} WHERE title LIKE '%%{title}%%';").fetchall()
    return records


def delete_record(table_name, title):
    """
    Deletes a record from a given table.
    """

    with db.connect() as conn:
        conn.execute(f"DELETE FROM {table_name} WHERE title = '{title}';")


def drop_table(table_name):
    """
    Removes a table.
    """

    with db.connect() as conn:
        conn.execute(f"DROP TABLE {table_name};")
