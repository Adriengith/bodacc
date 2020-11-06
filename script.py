from lxml import etree
from time import gmtime, strftime
import database
import os
from data import Data
from creations import creations
from transactions import transactions
import functions



#---------------- config ----------------#
config_max_avis = 50000000000000
config_activate_auto_restart_avis = True    #reprend le script là ou il a stop
config_activate_api_gouv = True
config_activate_creations = False
config_activate_transactions = True
config_forder_name = "BODACC_xml"
config_str_error = "Null"
config_int_error = -1
config_date_error = "0001-01-01"
#----------------------------------------#

save_nb_avis = functions.auto_restart_avis(config_activate_auto_restart_avis)

show_logs = 0
nb_years = 0
nb_files = 0
nb_avis = 0

database.create_companies()
database.create_places()
database.create_transactions()
database.create_creations()

data = Data(config_str_error, config_int_error, config_date_error)

folders_list = os.listdir(config_forder_name)

for one_folder in folders_list:  #on regarde les dossiers des années un par un
    nb_years += 1
    xml_list = []
    xml_rcs_list = []
    actual_folder_year = config_forder_name + "/" + one_folder

    xml_list = os.listdir(actual_folder_year)
    xml_rcs_list = functions.append_list(xml_list, xml_rcs_list)

    for one_xml_rca in xml_rcs_list :  #on regarde les fichiers un par un
        nb_files += 1

        tree = etree.parse(actual_folder_year + '/' + one_xml_rca)
        root = tree.getroot()

        for avis in root.findall('.//avis'):  #On regarde les avis un par un
            nb_avis += 1

            if nb_avis >= save_nb_avis :
                functions.auto_restart_save(nb_avis)

                #----------------------- CREATIONS -----------------------#
                creations(data, avis, config_activate_api_gouv, config_activate_creations, nb_files)

                #---------------------- TRANSACTIONS ----------------------#
                transactions(data, avis, config_activate_api_gouv, config_activate_transactions, nb_files)

                
                #logs + arret
                if nb_avis == config_max_avis:
                    data.final_logs(nb_avis, nb_files, nb_years)
            else:
                show_logs = functions.auto_restart_logs(nb_avis, show_logs, save_nb_avis)

data.final_logs(nb_avis, nb_files, nb_years)

