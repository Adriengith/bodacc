import functions

def transactions(data, avis, config_activate_api_gouv, config_activate_transactions, nb_files):

    if config_activate_transactions :
        #avant de traiter la donnée, on check si on a affaire à une transaction et si elle est déjà dans notre db
        is_transaction = functions.check_if_is_transaction(avis)
        transaction_is_in_db = functions.check_if_transaction_exist_in_db(avis, is_transaction)

    if config_activate_transactions and is_transaction and transaction_is_in_db is False:
        # ---------------------------- BUYER ---------------------------- #
        #reset
        data.time_created_updated_reset()
        data.companie_reset()
        data.place_reset()
        data.tansactions_id_reset()

        #on stock le siren pour l'api
        data.companie_get_siren_xml(avis)

        # API -> on vas chercher bcp de données pour companies et places
        data.gouv_api(config_activate_api_gouv)

        #si l'api n'a pas trouvé le nom, alors on le cherche dans le xml:
        data.companie_get_name_xml_if_api_is_none(avis)

        #on check si on dois update ou insert dans la db
        data.check_if_companie_is_in_db_and_get_id_if_exist()
        data.check_if_place_is_in_db_and_get_id_if_exist()

        #on update ou insert dans la db
        data.insert_or_update_companie_in_db()
        data.insert_or_update_place_in_db()

        #on save les infos de l'acheteur (serviront pr le transaction)
        data.get_buyer_companie_id()
        data.get_actual_place_id()

        #logs
        data.transactions_buyer_logs(nb_files)

        # ---------------------------- SELLER ---------------------------- #
        #reset
        data.companie_reset()
        data.place_reset()
        data.tansactions_reset()

        #on stock le siren pour l'api
        data.companie_get_siren_seller_xml(avis)

        # API -> on vas chercher bcp de données pour companies et places
        data.gouv_api(config_activate_api_gouv)

        #si l'api n'a pas trouvé le nom, alors on le cherche dans le xml:
        data.companie_get_name_seller_xml_if_api_is_none(avis)

        #on recup dans les xml :
        data.transaction_get_date_xml(avis)
        data.transaction_get_journal_id_xml(avis)
        data.transaction_get_price_cents_xml(avis)

        #on check si on dois update ou insert dans la db
        data.check_if_companie_is_in_db_and_get_id_if_exist()
        data.check_if_place_is_in_db_and_get_id_if_exist()

        #une fois le seller stocké en db on recup certaines infos
        data.get_seller_infos()

        #on update ou insert dans la db
        data.insert_or_update_companie_in_db()
        data.insert_or_update_place_in_db()

        #on save les infos du vendeur (serviront pr le transaction)
        data.get_seller_companie_id()
        data.get_seller_place_id()

        #insert transaction db
        data.insert_transaction_in_db()

        #logs
        data.transaction_final_logs(nb_files)
        
