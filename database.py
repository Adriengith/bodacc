import psycopg2
from psycopg2 import OperationalError
import getpass

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database = db_name,
            user = db_user,
            password = db_password,
            host = db_host,
            port = db_port,
        )
        print("Connection to BODACC_DB as successful")
    except OperationalError as e:
        print(f"The error '{e}' as occured")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}'as occured")

def create_companies():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name TEXT,
                ape_code TEXT,
                siren TEXT,
                created_at DATE,
                updated_at DATE
            );""")

def create_places():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS places(
                id SERIAL PRIMARY KEY,
                address TEXT,
                zipcode BIGINT,
                city TEXT,
                department BIGINT,
                created_at DATE,
                updated_at DATE,
                geo_api_id TEXT
            );""")

def create_transactions():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS transactions(
                id SERIAL PRIMARY KEY,
                date DATE,
                seller_id BIGINT REFERENCES companies(id),
                buyer_id BIGINT REFERENCES companies(id),
                place_id BIGINT REFERENCES places(id),
                created_at DATE,
                updated_at DATE,
                address TEXT,
                geo_api_id TEXT,
                price_cents BIGINT,
                zipcode BIGINT,
                city TEXT,
                journal_id TEXT
            );""")

def create_creations():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS creations(
                id SERIAL PRIMARY KEY,
                companie_id BIGINT REFERENCES companies(id),
                place_id BIGINT REFERENCES places(id),
                date_start_activity DATE,
                activity TEXT,
                capital_cents BIGINT,
                created_at DATE,
                updated_at DATE,
                journal_id TEXT
            );""")

def insert_companies(name, ape_code, siren, created_at, updated_at):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO companies(name, ape_code, siren, created_at, updated_at) VALUES (%s, %s, %s, %s, %s);",(name, ape_code, siren, created_at, updated_at))

def insert_places(address, zipcode, city, department, created_at, updated_at, geo_api_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO places(address, zipcode, city, department, created_at, updated_at, geo_api_id) VALUES (%s ,%s ,%s ,%s ,%s ,%s, %s);",(address, zipcode, city, department, created_at, updated_at, geo_api_id))

def insert_transactions(date, seller_id, buyer_id, place_id, created_at, updated_at, address, geo_api_id, price_cents, zipcode, city, journal_id):
    with connection:
        with connection.cursor() as cursor: 
            cursor.execute("INSERT INTO transactions(date, seller_id, buyer_id, place_id, created_at, updated_at, address, geo_api_id, price_cents, zipcode, city, journal_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",(date, seller_id, buyer_id, place_id, created_at, updated_at, address, geo_api_id, price_cents, zipcode, city, journal_id))

def insert_creations(companie_id, place_id, date_start_activity, activity, capital_cents, created_at, updated_at, journal_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO creations(companie_id, place_id, date_start_activity, activity, capital_cents, created_at, updated_at, journal_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",(companie_id, place_id, date_start_activity, activity, capital_cents, created_at, updated_at, journal_id))

def check_if_companie_is_in_db(siren):
    id_compagnie_in_db = -1
    if siren != "Null":
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM companies WHERE siren = '{siren}'")
            list_id_compagnie_in_db = cursor.fetchone()
            if list_id_compagnie_in_db is None:
                companie_is_in_db = False
            else:
                companie_is_in_db = True
                id_compagnie_in_db = list_id_compagnie_in_db[0]
    else:
        companie_is_in_db = False
    return companie_is_in_db, id_compagnie_in_db

def check_if_place_is_in_db(geo_api_id):
    id_place_in_db = -1
    if geo_api_id != "Null":
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM places WHERE geo_api_id ='{geo_api_id}'")
            list_id_place_in_db = cursor.fetchone()
            if list_id_place_in_db is None:
                place_is_in_db = False
            else:
                place_is_in_db = True
                id_place_in_db = list_id_place_in_db[0]
    else:
        place_is_in_db = False
    return place_is_in_db, id_place_in_db

def check_if_transaction_is_in_db(journal_id):
    with connection.cursor() as cursor: 
        cursor.execute(f"select id from transactions where journal_id = '{journal_id}'")
        check_if_exist = cursor.fetchone()
        if check_if_exist is None:
            tansaction_is_in_db = False
        else:
            tansaction_is_in_db = True #remettre True
            print("Transaction already exist in db :", journal_id)
    return tansaction_is_in_db

def check_if_creation_is_in_db(journal_id):
    with connection.cursor() as cursor: 
        cursor.execute(f"select id from creations where journal_id = '{journal_id}'")
        check_if_exist = cursor.fetchone()
        if check_if_exist is None:
            creation_is_in_db = False
        else:
            creation_is_in_db = True #remettre True
            print("Creation already exist in db :", journal_id)
    return creation_is_in_db

def update_companies(id_compagnie_in_db, name, ape_code, siren, updated_at):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE companies SET name = %s, ape_code = %s, siren = %s, updated_at = %s WHERE id = '{id_compagnie_in_db}';",(name, ape_code, siren, updated_at))

def update_places(id_place_in_db, address, zipcode, city, department, updated_at):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE places SET address = %s , zipcode = %s, city = %s , department = %s , updated_at = %s WHERE id = '{id_place_in_db}';",(address, zipcode, city, department, updated_at))

def search_actual_id_compagnie():
    id_compagnie_in_db = -1
    with connection.cursor() as cursor:
        cursor.execute("SELECT id from companies ORDER BY id DESC limit 1;")
        list_id_compagnie_in_db = cursor.fetchone()
        id_compagnie_in_db = list_id_compagnie_in_db[0]
    return id_compagnie_in_db

def search_actual_id_place():
    id_place_in_db = -1
    with connection.cursor() as cursor:
        cursor.execute("SELECT id from places ORDER BY id DESC limit 1;")
        list_id_place_in_db = cursor.fetchone()
        id_place_in_db = list_id_place_in_db[0]
    return id_place_in_db




#connection = create_connection("d19nvp3s8hnj9u","kicskmjwseqhsg","c304db353b41b95a83753f64c5e7d61f66d00a3bf489354a4290486c91991155","ec2-52-48-65-240.eu-west-1.compute.amazonaws.com","5432")
#connection = create_connection("bodacc_scrap","steeven2","toto","127.0.0.1","5432")
connection = create_connection("bodacc","adrienfontaine","postgres","127.0.0.1","5432")
