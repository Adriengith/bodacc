import urllib.request, json

def gouv_api(siren, ape_code, name, address, zipcode, city, department, geo_api_id,companies_sucess_logs, companies_errors_logs,places_sucess_logs, places_errors_logs, config_str_error, config_int_error):
    try :
        with urllib.request.urlopen(f"https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/{siren}") as url:
            data = json.loads(url.read().decode())
            
            ape_code = api_get_ape_code(data, companies_errors_logs, companies_sucess_logs, config_str_error)
            name = api_get_name(data, companies_errors_logs, companies_sucess_logs, config_str_error)
            geo_api_id = api_get_geo_api_id(data, places_errors_logs, places_sucess_logs, config_str_error)
            department = api_get_department(data, places_errors_logs, places_sucess_logs, config_int_error)
            city = api_get_city(data, places_errors_logs, places_sucess_logs, config_str_error)
            zipcode = api_get_zipcode(data, places_errors_logs, places_sucess_logs, config_int_error)
            address = api_get_address(data, places_errors_logs, places_sucess_logs, config_str_error)
            return name, ape_code, address, zipcode, city, department, geo_api_id
    except:
        companies_errors_logs["ape_code"] += 1
        companies_errors_logs["name"] += 1
        places_errors_logs["address"]+= 1
        places_errors_logs["zipcode"]+= 1
        places_errors_logs["city"]+= 1
        places_errors_logs['department'] += 1
        places_errors_logs["geo_api_id"] += 1
        return name, ape_code, address, zipcode, city, department, geo_api_id


def api_get_ape_code(data, companies_errors_logs, companies_sucess_logs, config_str_error):
    ape_code = data['unite_legale']['activite_principale']
    ape_code = ape_code.replace(".","")
    # logs
    if type(ape_code) != str:
        companies_errors_logs["ape_code"] += 1
        ape_code = config_str_error
    elif type(ape_code) == str:
        companies_sucess_logs["ape_code"] += 1
    return ape_code

def api_get_name(data, companies_errors_logs, companies_sucess_logs, config_str_error):
    name = data['unite_legale']['denomination']
    if type(name) != str:
        name = data['unite_legale']['etablissement_siege']['denomination_usuelle']
        if type(name) != str:
            first_name = data['unite_legale']['prenom_usuel']
            last_name = data['unite_legale']['nom']
            name = (first_name +' '+ last_name)
    # logs
    if type(name) != str:
        companies_errors_logs["name"] += 1
        name = config_str_error
    elif type(name) == str:
        companies_sucess_logs["name"] += 1
    return name

def api_get_address(data, places_errors_logs, places_sucess_logs, config_str_error):
    address = data['unite_legale']['etablissement_siege']['geo_adresse']
    # logs
    if type(address) != str:
        places_errors_logs["address"] += 1
        address = config_str_error
    elif type(address) == str:
        places_sucess_logs['address'] += 1
    return address

def api_get_zipcode(data, places_errors_logs, places_sucess_logs, config_int_error):
    zipcode = data['unite_legale']['etablissement_siege']['code_postal']
    # logs 
    if type(zipcode) != str:
        places_errors_logs["zipcode"] += 1
        zipcode = config_int_error
    elif type(zipcode) == str:
        places_sucess_logs['zipcode'] += 1
    return zipcode

def api_get_city(data, places_errors_logs, places_sucess_logs, config_str_error):
    city = data['unite_legale']['etablissement_siege']['libelle_commune']
    # logs
    if type(city) != str:
        places_errors_logs["city"] += 1
        city = config_str_error
    elif type(city) == str:
        places_sucess_logs['city'] += 1
    return city

def api_get_department(data, places_errors_logs, places_sucess_logs, config_int_error):
    department = data['unite_legale']['etablissement_siege']['code_postal']
    try:
        department = department[0:2]
    except:
        department = config_int_error
    # logs
    if type(department) != str:
        places_errors_logs["department"] += 1
        department = config_int_error
    elif type(department) == str:
        places_sucess_logs['department'] += 1
    return department

def api_get_geo_api_id(data, places_errors_logs, places_sucess_logs, config_str_error):
    geo_api_id = data["unite_legale"]['etablissement_siege']['geo_id']
    # logs
    if type(geo_api_id) != str:
        places_errors_logs["geo_api_id"] += 1
        geo_api_id = config_str_error
    elif type(geo_api_id) == str:
        places_sucess_logs['geo_api_id'] += 1
    return geo_api_id
