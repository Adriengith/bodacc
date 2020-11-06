import folium
import psycopg2
from psycopg2 import OperationalError
import gouv_api_folium
from random import random
import time
import sys

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

def graph1_all_buyer_group_by_transactions():
    #-----config-----#
    black_color = 1000
    darkred_color = 250
    red_color = 125
    orange_color = 50
    darkgreen_color = 25
    green_color = 12.5
    lightgreen = 0
    inc = 0


    with connection.cursor() as cursor:
        cursor.execute("""select companies.id, companies.name, companies.siren, places.address, sum(transactions.price_cents) AS total_transactions_price_cents, count(companies.siren) AS transactions_nb 
                        FROM transactions 
                        INNER JOIN companies ON companies.id = transactions.buyer_id 
                        INNER JOIN places ON places.id = transactions.place_id
                        group by companies.name, companies.id, places.address
                        order by total_transactions_price_cents
                        DESC LIMIT 1000;""")
        fetchall = cursor.fetchall()

        c = folium.Map(location=[47.0833814, 2.3934824],zoom_start=6)

        for one_transaction in fetchall :
            boycott = False
            print("-"*120)
            print(one_transaction)
            data = gouv_api_folium.gouv_api(one_transaction[2], -1, boycott)
            cords = [data[0], data[1]]
            boycott = data[2]
            if boycott == False :
                inc += 1

                id_companie_buyer = one_transaction[0]
                name_companie_buyer = one_transaction[1]
                siren_companie_buyer = one_transaction[2]
                address_companie_buyer = one_transaction[3]

                total_transactions = one_transaction[4]
                total_transactions = float(total_transactions) / 100000000
                total_transactions = round(total_transactions,3)
                

                nb_transactions = one_transaction[5]

                if total_transactions > black_color :
                    color='black'

                elif total_transactions > darkred_color :
                    color='darkred'

                elif total_transactions > red_color :
                    color='red'

                elif total_transactions > orange_color :
                    color='orange'

                elif total_transactions > darkgreen_color :
                    color='darkgreen'

                elif total_transactions > green_color :
                    color='green'

                elif total_transactions > lightgreen :
                    color='lightgreen'
                else:
                    color='white'



                print("> add to map",)
                time.sleep(0.15)
                print(inc)
                folium.Marker(location=cords, tooltip=f"<center>Acheteur : <strong>{name_companie_buyer}</strong><br>ID acheteur : <strong>{id_companie_buyer}</strong><br>Siren : <strong>{siren_companie_buyer}</strong><br>Adresse : <strong>{address_companie_buyer}</strong><br>Nombres d'achats de places : <strong>{nb_transactions}</strong><br>Montant total des achats : <strong>{total_transactions} M €</strong></center>",icon=folium.Icon(color=color)).add_to(c)
                
                random_save = random() <= 0.1
                if random_save :
                    print("Save graph1_all_buyer_group_by_transactions")
                    c.save('graph1_all_buyer_group_by_transactions.html')
                

            else :
                print("> BOYCOTTED API NOT FOUND")

    print("save ok")



    c.save('graph1_all_buyer_group_by_transactions.html')









def graph2_all_places_selled():
    #-----config-----#
    black_color = 500
    darkred_color = 250
    red_color = 125
    orange_color = 50
    darkgreen_color = 25
    green_color = 12.5
    lightgreen = 0
    inc = 0


    with connection.cursor() as cursor:
        cursor.execute("""SELECT companies.name, transactions.address, companies.siren, transactions.price_cents, transactions.seller_id, transactions.journal_id, transactions.date 
                        FROM transactions
                        INNER JOIN companies On  companies.id = transactions.seller_id
                        ORDER BY price_cents
                        DESC LIMIT 1500;""")
        fetchall = cursor.fetchall()

        c = folium.Map(location=[47.0833814, 2.3934824],zoom_start=6)


        for one_transaction in fetchall :
            
            
            boycott = False
            print("-"*120)
            print(one_transaction)
            
            data = gouv_api_folium.gouv_api(one_transaction[2], -1, boycott)
            cords = [data[0], data[1]]
            boycott = data[2]

            if boycott == False :
                inc += 1

                name_seller = one_transaction[0]

        

                address_seller = one_transaction[1]
                siren_seller = one_transaction[2]


                price_cents = one_transaction[3]
                price_cents = float(price_cents) / 100000000
                price_cents = round(price_cents,3)
                
                seller_id = one_transaction[4]
                journal_id = one_transaction[5]
                date = one_transaction[6]

                with connection.cursor() as cursor:
                    cursor.execute(f"""SELECT companies.name, companies.siren, companies.id FROM transactions
                                    INNER JOIN companies ON companies.id = transactions.buyer_id
                                    WHERE seller_id = {seller_id} ;""")
                    fetchone = cursor.fetchone()
 
                    name_buyer = fetchone[0]
                    siren_buyer = fetchone[1]
                    id_buyer = fetchone[2]
                    print(inc, name_buyer,siren_buyer,id_buyer)


                if price_cents > black_color :
                    color='black'

                elif price_cents > darkred_color :
                    color='darkred'

                elif price_cents > red_color :
                    color='red'

                elif price_cents > orange_color :
                    color='orange'

                elif price_cents > darkgreen_color :
                    color='darkgreen'

                elif price_cents > green_color :
                    color='green'

                elif price_cents > lightgreen :
                    color='lightgreen'
                else:
                    color='white'

                time.sleep(0.15)
                folium.Marker(location=cords, tooltip=f"<center>ID journal : <strong>{journal_id}</strong><br>Vendeur : <strong>{name_seller}</strong><br>ID vendeur: <strong>{seller_id}</strong><br>Siren vendeur: <strong>{siren_seller}</strong><br>Adresse vendeur: <strong>{address_seller}</strong><br><br>Acheteur : <strong>{name_buyer}</strong><br>ID acheteur : <strong>{id_buyer}</strong><br>Siren acheteur : <strong>{siren_buyer}</strong><br><br>Montant de la transaction : <strong>{price_cents} M €</strong><br>Date de la transaction : <strong>{date}</strong></center>",icon=folium.Icon(color=color)).add_to(c)
                
                random_save = random() <= 0.1
                if random_save :
                    print("Save graph2_all_places_selled")
                    c.save('graph2_all_places_selled.html')
                


            else :
                print("> BOYCOTTED API NOT FOUND")
    print("save ok")


    c.save('graph2_all_places_selled.html')







def graph3_all_places_selled_by_departement():
    #-----config-----#
    config_zipcode = 33440
    black_color = 10
    darkred_color = 2
    red_color = 1
    orange_color = 0.5
    darkgreen_color = 0.25
    green_color = 0.175
    lightgreen = 0
    inc = 0


    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT companies.name, transactions.address, companies.siren, transactions.price_cents, transactions.seller_id, transactions.journal_id, transactions.date 
                        FROM transactions
                        INNER JOIN companies ON  companies.id = transactions.seller_id
                        WHERE transactions.zipcode = {config_zipcode}
                        ORDER BY transactions.price_cents DESC
                        LIMIT 1000;""")
        fetchall = cursor.fetchall()

        c = folium.Map(location=[47.0833814, 2.3934824],zoom_start=6)


        for one_transaction in fetchall :
            
            
            boycott = False
            print("-"*120)
            print(one_transaction)
            
            data = gouv_api_folium.gouv_api(one_transaction[2], -1, boycott)
            cords = [data[0], data[1]]
            boycott = data[2]

            if boycott == False :
                inc += 1

                name_seller = one_transaction[0]

        

                address_seller = one_transaction[1]
                siren_seller = one_transaction[2]


                price_cents = one_transaction[3]
                price_cents = float(price_cents) / 100000000
                price_cents = round(price_cents,3)
                
                seller_id = one_transaction[4]
                journal_id = one_transaction[5]
                date = one_transaction[6]

                with connection.cursor() as cursor:
                    cursor.execute(f"""SELECT companies.name, companies.siren, companies.id FROM transactions
                                    INNER JOIN companies ON companies.id = transactions.buyer_id
                                    WHERE seller_id = {seller_id} ;""")
                    fetchone = cursor.fetchone()
 
                    name_buyer = fetchone[0]
                    siren_buyer = fetchone[1]
                    id_buyer = fetchone[2]
                    print(inc, name_buyer,siren_buyer,id_buyer)


                if price_cents > black_color :
                    color='black'

                elif price_cents > darkred_color :
                    color='darkred'

                elif price_cents > red_color :
                    color='red'

                elif price_cents > orange_color :
                    color='orange'

                elif price_cents > darkgreen_color :
                    color='darkgreen'

                elif price_cents > green_color :
                    color='green'

                elif price_cents > lightgreen :
                    color='lightgreen'
                else:
                    color='white'



                time.sleep(0.15)
                folium.Marker(location=cords, tooltip=f"<center>ID journal : <strong>{journal_id}</strong><br>Vendeur : <strong>{name_seller}</strong><br>ID vendeur: <strong>{seller_id}</strong><br>Siren vendeur: <strong>{siren_seller}</strong><br>Adresse vendeur: <strong>{address_seller}</strong><br><br>Acheteur : <strong>{name_buyer}</strong><br>ID acheteur : <strong>{id_buyer}</strong><br>Siren acheteur : <strong>{siren_buyer}</strong><br><br>Montant de la transaction : <strong>{price_cents} M €</strong><br>Date de la transaction : <strong>{date}</strong></center>",icon=folium.Icon(color=color)).add_to(c)
                
                random_save = random() <= 0.1
                if random_save :
                    print("Save graph3_all_places_selled_by_departement")
                    c.save('graph3_all_places_selled_by_departement.html')
                


            else :
                print("> BOYCOTTED API NOT FOUND")
    print("save ok")


    c.save('graph3_all_places_selled_by_departement.html')







def graph4_all_places_selled_by_date():
    #-----config-----#
    config_date = '2020-01-01'
    black_color = 20
    darkred_color = 10
    red_color = 5
    orange_color = 3
    darkgreen_color = 2
    green_color = 1
    lightgreen = 0
    inc = 0


    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT companies.name, transactions.address, companies.siren, transactions.price_cents, transactions.seller_id, transactions.journal_id, transactions.date 
                        FROM transactions
                        INNER JOIN companies ON  companies.id = transactions.seller_id
                        WHERE transactions.date > '{config_date}' AND transactions.date <> '0001-01-01'
                        ORDER BY transactions.price_cents DESC
                        LIMIT 1000;""")
        fetchall = cursor.fetchall()

        c = folium.Map(location=[47.0833814, 2.3934824],zoom_start=6)


        for one_transaction in fetchall :
            
            
            boycott = False
            print("-"*120)
            print(one_transaction)
            
            data = gouv_api_folium.gouv_api(one_transaction[2], -1, boycott)
            cords = [data[0], data[1]]
            boycott = data[2]

            if boycott == False :
                inc += 1

                name_seller = one_transaction[0]

        

                address_seller = one_transaction[1]
                siren_seller = one_transaction[2]


                price_cents = one_transaction[3]
                price_cents = float(price_cents) / 100000000
                price_cents = round(price_cents,3)
                
                seller_id = one_transaction[4]
                journal_id = one_transaction[5]
                date = one_transaction[6]

                with connection.cursor() as cursor:
                    cursor.execute(f"""SELECT companies.name, companies.siren, companies.id FROM transactions
                                    INNER JOIN companies ON companies.id = transactions.buyer_id
                                    WHERE seller_id = {seller_id} ;""")
                    fetchone = cursor.fetchone()
 
                    name_buyer = fetchone[0]
                    siren_buyer = fetchone[1]
                    id_buyer = fetchone[2]
                    print(inc, name_buyer,siren_buyer,id_buyer)


                if price_cents > black_color :
                    color='black'

                elif price_cents > darkred_color :
                    color='darkred'

                elif price_cents > red_color :
                    color='red'

                elif price_cents > orange_color :
                    color='orange'

                elif price_cents > darkgreen_color :
                    color='darkgreen'

                elif price_cents > green_color :
                    color='green'

                elif price_cents > lightgreen :
                    color='lightgreen'
                else:
                    color='white'



                time.sleep(0.15)
                folium.Marker(location=cords, tooltip=f"<center>ID journal : <strong>{journal_id}</strong><br>Vendeur : <strong>{name_seller}</strong><br>ID vendeur: <strong>{seller_id}</strong><br>Siren vendeur: <strong>{siren_seller}</strong><br>Adresse vendeur: <strong>{address_seller}</strong><br><br>Acheteur : <strong>{name_buyer}</strong><br>ID acheteur : <strong>{id_buyer}</strong><br>Siren acheteur : <strong>{siren_buyer}</strong><br><br>Montant de la transaction : <strong>{price_cents} M €</strong><br>Date de la transaction : <strong>{date}</strong></center>",icon=folium.Icon(color=color)).add_to(c)
                
                random_save = random() <= 0.1
                if random_save :
                    print("Save graph4_all_places_selled_by_date")
                    c.save('graph4_all_places_selled_by_date.html')
                


            else :
                print("> BOYCOTTED API NOT FOUND")
    print("save ok")


    c.save('graph4_all_places_selled_by_date.html')









#connection = create_connection("d19nvp3s8hnj9u","kicskmjwseqhsg","c304db353b41b95a83753f64c5e7d61f66d00a3bf489354a4290486c91991155","ec2-52-48-65-240.eu-west-1.compute.amazonaws.com","5432")
connection = create_connection("bodacc","adrienfontaine","postgres","127.0.0.1","5432")

#graph1_all_buyer_group_by_transactions()

graph2_all_places_selled()

#graph3_all_places_selled_by_departement()

#graph4_all_places_selled_by_date()