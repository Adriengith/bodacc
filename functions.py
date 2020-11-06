import database
from random import random

def check_if_is_transaction(avis):
    try :  
        search_precedentProprietairePP = avis.find('.//precedentProprietairePP')
        search_precedentProprietairePP.find('numeroImmatriculation')
        is_transaction = True
    except :
        try:
            search_precedentProprietairePM = avis.find('.//precedentProprietairePM')
            search_precedentProprietairePM.find('numeroImmatriculation')
            is_transaction = True
        except:
            is_transaction = False
    return is_transaction

def check_if_is_creation(avis):
    try :
        search_creation = avis.find('.//creation')
        search_creation.find('dateCommencementActivite')
        is_creation = True
    except :
        is_creation = False
    return is_creation

def check_if_transaction_exist_in_db(avis, is_transaction):
    if is_transaction:
        journal_id = avis.find('nojo').text
        transaction_is_in_db = database.check_if_transaction_is_in_db(journal_id)
    else:
        transaction_is_in_db = False
    return transaction_is_in_db

def check_if_creation_exist_in_db(avis, is_creation):
    if is_creation:
        journal_id = avis.find('nojo').text
        creation_is_in_db = database.check_if_creation_is_in_db(journal_id)
    else:
        creation_is_in_db = False
    return creation_is_in_db

def append_list(xml_list, xml_rcs_list):
    for one_xml in xml_list:
        if one_xml[0:5] == "RCS-A":
            xml_rcs_list.append(one_xml)
    return xml_rcs_list

def auto_restart_avis(config_activate_auto_restart_avis):
    fichier = open("auto_restart_avis.txt", "r")
    save_nb_avis = fichier.read()
    save_nb_avis = int(save_nb_avis)
    fichier.close()
    if config_activate_auto_restart_avis is False:
        save_nb_avis = 0
    return save_nb_avis

def auto_restart_save(nb_avis):
    random_save = False
    random_save = random() <= 0.02
    if random_save :
        nb_avis = str(nb_avis)
        fichier = open("auto_restart_avis.txt", "w")
        fichier.close()
        fichier = open("auto_restart_avis.txt", "a")
        fichier.write(nb_avis)
        fichier.close()

def auto_restart_logs(nb_avis, show_logs, save_nb_avis):
    show_logs += 1
    if show_logs == 10000:
        print("Avis",nb_avis,"/",save_nb_avis)
        show_logs = 0
    return show_logs
