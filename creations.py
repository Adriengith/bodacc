import functions

def creations(data, avis, config_activate_api_gouv, config_activate_creations, nb_files):

    if config_activate_creations :
        #avant de traiter la donnée, on check si on a affaire à une creation et si elle est déjà dans notre db
        is_creation = functions.check_if_is_creation(avis)
        creation_is_in_db = functions.check_if_creation_exist_in_db(avis, is_creation)

    if config_activate_creations and is_creation and creation_is_in_db is False :
        #reset
        data.time_created_updated_reset()
        data.companie_reset()
        data.place_reset()
        data.creation_reset()

        #on stock le siren pour l'api
        data.companie_get_siren_xml(avis)

        # API -> on vas chercher bcp de données pour companies et places
        data.gouv_api(config_activate_api_gouv)

        #si l'api n'a pas trouvé le nom, alors on le cherche dans le xml:
        data.companie_get_name_xml_if_api_is_none(avis)

        #on recup dans les xml :
        data.creation_get_date_start_activity_xml(avis)
        data.creation_get_activity(avis)
        data.creation_get_capital_cents_xml(avis)
        data.creation_get_journal_id_xml(avis)

        #on check si on dois update ou insert dans la db
        data.check_if_companie_is_in_db_and_get_id_if_exist()
        data.check_if_place_is_in_db_and_get_id_if_exist()

        #on update ou insert dans la db
        data.insert_or_update_companie_in_db()             
        data.insert_or_update_place_in_db()

        #on recup db les id de la place et de la companie qu'on vient d'ajouter (utile pour la table creation)
        data.get_actual_companie_id()
        data.get_actual_place_id()
        
        #insert creation db
        data.insert_creation_in_db()

        #logs
        data.creations_finals_logs(nb_files)
