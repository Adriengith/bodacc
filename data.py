from gouv_api import gouv_api
from datetime import datetime
import database
import sys
import re

class Data:
    def __init__(self, config_str_error, config_int_error, config_date_error):
        self.id_compagnie = 0
        self.id_place = 0
        self.id_transaction = 0
        self.id_creation = 0
        self.companies_errors_logs = {"name":0, "ape_code":0, "siren":0}
        self.companies_sucess_logs = {"name":0, "ape_code":0, "siren":0} 
        self.places_errors_logs = {"address":0, "zipcode":0, "city":0, "department":0, "geo_api_id":0}
        self.places_sucess_logs = {"address":0, "zipcode":0, "city":0, "department":0, "geo_api_id":0}
        self.transactions_errors_logs = {"date":0, "price_cents":0, "journal_id":0}
        self.transactions_sucess_logs = {"date":0, "price_cents":0, "journal_id":0}
        self.creations_errors_logs = {"date_start_activity":0,"activity":0,"capital_cents":0,"journal_id":0}
        self.creations_sucess_logs = {"date_start_activity":0,"activity":0,"capital_cents":0,"journal_id":0}
        self.config_str_error = config_str_error
        self.config_int_error = config_int_error
        self.config_date_error = config_date_error

    def time_created_updated_reset(self):
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = self.created_at

    def companie_reset(self):
        self.id_compagnie += 1
        self.companie_id = self.config_int_error
        self.name = self.config_str_error
        self.ape_code = self.config_str_error
        self.siren = self.config_str_error

    def place_reset(self):
        self.id_place += 1
        self.place_id = self.config_int_error
        self.address = self.config_str_error
        self.zipcode = self.config_int_error
        self.city = self.config_str_error
        self.department = self.config_int_error
        self.geo_api_id = self.config_str_error

    def creation_reset(self):
        self.id_creation += 1
        self.place_id = self.config_int_error
        self.date_start_activity = self.config_date_error
        self.activity = self.config_str_error
        self.capital_cents = self.config_int_error
        self.journal_id = self.config_str_error

    def tansactions_id_reset(self):
        self.seller_id = self.config_int_error
        self.buyer_id = self.config_int_error
        self.place_seller_id = self.config_int_error

    def tansactions_reset(self):
        self.id_transaction += 1
        self.date = self.config_date_error
        self.address = self.config_str_error
        self.geo_api_id = self.config_str_error
        self.price_cents = self.config_int_error
        self.zipcode = self.config_int_error
        self.city = self.config_str_error
        self.journal_id = self.config_str_error

    def companie_get_siren_xml(self, avis):
        try :  
            search_siren = avis.find('.//personneMorale')
            search_numeroImmatriculation = search_siren.find('numeroImmatriculation')
            self.siren = search_numeroImmatriculation.find('numeroIdentification').text
            self.siren = self.siren.replace(" ","") 
            self.companies_sucess_logs["siren"] += 1
        except :
            try:
                search_siren = avis.find('.//personnePhysique')
                search_numeroImma = search_siren.find('numeroImmatriculation')
                self.siren = search_numeroImma.find('numeroIdentification').text
                self.siren = self.siren.replace(" ","") 
                self.companies_sucess_logs["siren"] += 1
            except:
                self.companies_errors_logs["siren"] += 1

    def companie_get_siren_seller_xml(self, avis):
        try :  
            search_precedentProprietairePP = avis.find('.//precedentProprietairePP')
            search_numeroImmatriculation = search_precedentProprietairePP.find('numeroImmatriculation')
            self.siren = search_numeroImmatriculation.find('numeroIdentification').text
            self.siren = self.siren.replace(" ","") 
            self.companies_sucess_logs["siren"] += 1
        except :
            try:
                search_precedentProprietairePM = avis.find('.//precedentProprietairePM')
                search_numeroImma = search_precedentProprietairePM.find('numeroImmatriculation')
                self.siren = search_numeroImma.find('numeroIdentification').text
                self.siren = self.siren.replace(" ","") 
                self.companies_sucess_logs["siren"] += 1
            except:
                self.companies_errors_logs["siren"] += 1

    def gouv_api(self, config_activate_api_gouv):
        if config_activate_api_gouv :
            reponse = []
            reponse = gouv_api(self.siren, self.ape_code, self.name, self.address, self.zipcode, self.city, self.department, self.geo_api_id, self.companies_sucess_logs, self.companies_errors_logs, self.places_sucess_logs, self.places_errors_logs,self.config_str_error, self.config_int_error)
            self.name = reponse[0]
            self.ape_code = reponse[1]
            self.address = reponse[2]
            self.zipcode = reponse[3]
            self.city = reponse[4]
            self.department = reponse[5]
            self.geo_api_id = reponse[6]

    def companie_get_name_xml_if_api_is_none(self, avis):
        if self.name == self.config_str_error:             
            try :  
                search_name = avis.find('.//personneMorale')
                self.name = search_name.find('denomination').text
                self.companies_sucess_logs["name"] += 1
                self.companies_errors_logs["name"] -= 1
            except :
                try:
                    search_name = avis.find('.//personneMorale')
                    self.name = search_name.find('nomCommercial').text
                    self.companies_sucess_logs["name"] += 1
                    self.companies_errors_logs["name"] -= 1
                except :
                    try :
                        search_name = avis.find('.//personnePhysique')
                        self.name = search_name.find('nomUsage').text
                        self.companies_sucess_logs["name"] += 1
                        self.companies_errors_logs["name"] -= 1
                    except :
                        try :
                            search_name = avis.find('.//personnePhysique')
                            nom = search_name.find('nom').text
                            prenom = search_name.find('prenom').text
                            self.name = (nom + ' ' + prenom)
                            self.companies_sucess_logs["name"] += 1
                            self.companies_errors_logs["name"] -= 1
                        except :
                            self.name = self.config_str_error
                            self.companies_errors_logs["name"] += 1

    def companie_get_name_seller_xml_if_api_is_none(self, avis):
        if self.name == self.config_str_error:             
            try :  
                search_name = avis.find('.//precedentProprietairePM')
                self.name = search_name.find('denomination').text
                self.companies_sucess_logs["name"] += 1
                self.companies_errors_logs["name"] -= 1
            except :
                try :
                    search_name = avis.find('.//precedentProprietairePP')
                    self.name = search_name.find('nomUsage').text
                    self.companies_sucess_logs["name"] += 1
                    self.companies_errors_logs["name"] -= 1
                except :
                    try :
                        search_name = avis.find('.//precedentProprietairePP')
                        nom = search_name.find('nom').text
                        prenom = search_name.find('prenom').text
                        self.name = (nom + ' ' + prenom)
                        self.companies_sucess_logs["name"] += 1
                        self.companies_errors_logs["name"] -= 1
                    except :
                        self.name = self.config_str_error
                        self.companies_errors_logs["name"] += 1

    def creation_get_date_start_activity_xml(self, avis):
        try :
            search_date_start_activity = avis.find('.//creation')
            self.date_start_activity = search_date_start_activity.find('dateCommencementActivite').text
            self.creations_sucess_logs["date_start_activity"] += 1
        except :
            self.date_start_activity = self.config_date_error
            self.creations_errors_logs["date_start_activity"] += 1

    def creation_get_activity(self, avis):
        try :
            search_activity = avis.find('.//etablissement')
            self.activity = search_activity.find('activite').text
            self.creations_sucess_logs["activity"] += 1
        except :
            self.activity = self.config_str_error
            self.creations_errors_logs['activity'] += 1

    def creation_get_capital_cents_xml(self,avis):
        try :
            search_capital_cents = avis.find('.//capital')
            self.capital_cents = search_capital_cents.find('montantCapital').text
            self.capital_cents = int(self.capital_cents)
            self.capital_cents *= 100
            self.creations_sucess_logs["capital_cents"] += 1
        except :
            self.capital_cents = self.config_int_error
            self.creations_errors_logs["capital_cents"] += 1

    def transaction_get_price_cents_xml(self,avis):
        try : 
            search_price_cents = avis.find('.//etablissement')
            self.price_cents = search_price_cents.find('origineFonds').text
            find_eur = self.price_cents.find('Euro')
            if find_eur == -1 :
                find_eur = self.price_cents.find('euro')
            if find_eur == -1 :
                find_eur = self.price_cents.find('EUR')
            if find_eur == -1 :
                find_eur = self.price_cents.find('EURO')
            if find_eur == -1 :
                find_eur = self.price_cents.find('€')
            if find_eur == -1 :
                find_eur = 16
            self.price_cents = self.price_cents[find_eur-15:find_eur]
            self.price_cents = re.sub('[)(azertyuiopmlkjhgfdsqwxcvbnAZERTYUIOPMLKJHGFDSQWXCVBNéàèê€]', '', self.price_cents) 
            self.price_cents = self.price_cents.replace(' ','') 
            self.price_cents = self.price_cents.replace('-','') 
            self.price_cents = self.price_cents.replace(':','') 
            if self.price_cents[-1:] == ".":     
                self.price_cents = self.price_cents[:-1]
            if self.price_cents[-3:-2] == "." or self.price_cents[-3:-2] == ",": 
                self.price_cents = re.sub('[,.]', '', self.price_cents)
                self.price_cents = int(self.price_cents)
                self.transactions_sucess_logs["price_cents"] += 1
            else:
                self.price_cents = int(self.price_cents)
                self.price_cents *=100
                self.transactions_sucess_logs["price_cents"] += 1
        except :
            self.price_cents = self.config_int_error
            self.transactions_errors_logs["price_cents"] += 1

    def creation_get_journal_id_xml(self, avis):
        try :
            self.journal_id = avis.find('nojo').text
            self.creations_sucess_logs["journal_id"] += 1
        except :
            self.journal_id = self.config_str_error
            self.creations_errors_logs["journal_id"] += 1

    def transaction_get_date_xml(self, avis):
        try :
            search_date = avis.find('.//vente')
            self.date = search_date.find('dateCommencementActivite').text
            self.transactions_sucess_logs["date"] += 1
        except :
            self.date = self.config_date_error
            self.transactions_errors_logs["date"] += 1

    def transaction_get_journal_id_xml(self, avis):
        try :
            self.journal_id = avis.find('nojo').text
            self.transactions_sucess_logs["journal_id"] += 1
        except :
            self.journal_id = self.config_str_error
            self.transactions_errors_logs["journal_id"] += 1

    def check_if_companie_is_in_db_and_get_id_if_exist(self):
        answer = database.check_if_companie_is_in_db(self.siren)
        self.companie_is_in_db = answer[0]
        self.id_compagnie_in_db = answer[1]

    def check_if_place_is_in_db_and_get_id_if_exist(self):
        answer = database.check_if_place_is_in_db(self.geo_api_id)
        self.place_is_in_db = answer[0]
        self.id_place_in_db = answer[1]

    def insert_or_update_companie_in_db(self):
        if self.companie_is_in_db is False :
            database.insert_companies(self.name, self.ape_code, self.siren, self.created_at, self.updated_at)
            print('\033[32m'+"insert companie",'\033[0m')
        elif self.companie_is_in_db:
            database.update_companies(self.id_compagnie_in_db, self.name, self.ape_code, self.siren, self.updated_at)
            print('\033[34m'+"update companie",'\033[0m') 

    def insert_or_update_place_in_db(self):
        if self.place_is_in_db is False:
            database.insert_places(self.address, self.zipcode, self.city, self.department, self.created_at, self.updated_at, self.geo_api_id)
            print('\033[32m'+"insert place",'\033[0m')                
        elif self.place_is_in_db:
            database.update_places(self.id_place_in_db, self.address, self.zipcode, self.city, self.department, self.updated_at)
            print('\033[34m'+"update place",'\033[0m')      

    def insert_creation_in_db(self):
        database.insert_creations(self.companie_id, self.place_id, self.date_start_activity, self.activity, self.capital_cents, self.created_at, self.updated_at, self.journal_id)

    def insert_transaction_in_db(self):
        database.insert_transactions(self.date, self.seller_id, self.buyer_id, self.place_buyer_id, self.created_at, self.updated_at, self.address, self.geo_api_id, self.price_cents, self.zipcode, self.city, self.journal_id)

    def get_seller_infos(self):
        if self.companie_is_in_db is False :
            self.seller_id = database.search_actual_id_compagnie()
        if self.place_is_in_db is False :
            self.id_place_in_db = database.search_actual_id_place()

    def get_seller_companie_id(self):
        if self.companie_is_in_db is False : 
            self.seller_id = database.search_actual_id_compagnie()
        else:
            self.seller_id = self.id_compagnie_in_db

    def get_seller_place_id(self):
        if self.place_is_in_db is False :
            self.place_seller_id = database.search_actual_id_place()
        else:
            self.place_seller_id = self.id_place_in_db

    def get_actual_companie_id(self):
        if self.companie_is_in_db is False : 
            self.companie_id = database.search_actual_id_compagnie()
        else:
            self.companie_id = self.id_compagnie_in_db

    def get_buyer_companie_id(self):
        if self.companie_is_in_db is False : 
            self.buyer_id = database.search_actual_id_compagnie()
        else:
            self.buyer_id = self.id_compagnie_in_db

    def get_actual_place_id(self):
        if self.place_is_in_db is False :
            self.place_id = database.search_actual_id_place()
            self.place_buyer_id = self.place_id
        else:
            self.place_id = self.id_place_in_db
            self.place_buyer_id = self.place_id

    def creations_finals_logs(self, nb_files):
        print("Comp. C  >",nb_files,"|",self.companie_id,"|",self.name,"|", self.ape_code,"|", self.siren,"|", self.created_at,"|", self.updated_at)
        print("Place C  >",nb_files,"|", self.place_id,"|",self.address,"|", self.zipcode,"|", self.city,"|",self.department,"|", self.created_at,"|", self.updated_at,"|",self.geo_api_id)  
        print("Creation >",nb_files,"|", self.companie_id,"|", self.place_id,"|",self.date_start_activity,"|", self.activity,"|", self.capital_cents,"|",self.created_at,"|", self.updated_at,"|", self.journal_id)  
        print("-"*120)
        
    def transactions_buyer_logs(self, nb_files):
        print("Comp. A  >",nb_files,"|",self.buyer_id,"|",self.name,"|", self.ape_code,"|", self.siren,"|", self.created_at,"|", self.updated_at)
        print("Place A  >",nb_files,"|", self.place_id,"|",self.address,"|", self.zipcode,"|", self.city,"|",self.department,"|", self.created_at,"|", self.updated_at,"|",self.geo_api_id)  

    def transaction_final_logs(self,nb_files):
        print("Comp. V  >",nb_files,"|",self.seller_id,"|",self.name,"|", self.ape_code,"|", self.siren,"|", self.created_at,"|", self.updated_at)
        print("Place V  >",nb_files,"|", self.place_seller_id,"|",self.address,"|", self.zipcode,"|", self.city,"|",self.department,"|", self.created_at,"|", self.updated_at,"|",self.geo_api_id)  
        print("Transact >",nb_files,"|",self.date,"|",self.seller_id,"|", self.buyer_id,"|", self.place_buyer_id,"|", self.created_at,"|", self.updated_at,"|", self.address,"|", self.geo_api_id,"|", self.price_cents,"|", self.zipcode,"|", self.city,"|",self.journal_id)  
        print("-"*120)

    def final_logs(self, nb_avis, nb_files, nb_years):
        try:
            sum_errors = sum(self.companies_errors_logs.values()) + sum(self.places_errors_logs.values()) + sum(self.transactions_errors_logs.values()) + sum(self.creations_errors_logs.values())
            sum_total = sum_errors + sum(self.companies_sucess_logs.values()) + sum(self.places_sucess_logs.values()) + sum(self.transactions_sucess_logs.values()) + sum(self.creations_sucess_logs.values())
            pourcent_errors = (sum_errors / sum_total) * 100
            pourcent_errors = round(pourcent_errors,2)
        except:
            pourcent_errors = 0
        print('\033[36m'+"Total years >",nb_years)
        print("Total files >", nb_files)
        print("Total avis >",nb_avis)
        print("Total companies >",self.id_compagnie)
        print("Total places >",self.id_place)
        print("Total transactions >",self.id_transaction)
        print("Total creations >",self.id_creation,'\033[0m')
        print('\033[33m'+"\nTOTAL POURCENT ERRORS >",pourcent_errors,'%','\033[0m')                
        print('\033[31m' + '\nCOMPAGNIES ERRORS >',self.companies_errors_logs,'\033[0m')
        print('\033[31m' + 'PLACES ERRORS >',self.places_errors_logs,'\033[0m')
        print('\033[31m' + 'TRANSACTIONS ERRORS >',self.transactions_errors_logs,'\033[0m')
        print('\033[31m' + 'CREATIONS ERRORS >',self.creations_errors_logs,'\033[0m')
        print('\033[32m' + '\nCOMPAGNIES SUCESS >',self.companies_sucess_logs,'\033[0m')
        print('\033[32m' + 'PLACES SUCESS >',self.places_sucess_logs,'\033[0m')
        print('\033[32m' + 'TRANSACTIONS SUCESS >',self.transactions_sucess_logs,'\033[0m')
        print('\033[32m' + 'CREATIONS SUCESS >',self.creations_sucess_logs,'\033[0m')
        sys.exit()

