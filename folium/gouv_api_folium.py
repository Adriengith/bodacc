import urllib.request, json

def gouv_api(siren, config_int_error, boycott):
    try :
        with urllib.request.urlopen(f"https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/{siren}") as url:
            data = json.loads(url.read().decode())
            
            latitude = data['unite_legale']['etablissement_siege']['latitude']
            longitude = data['unite_legale']['etablissement_siege']['longitude']


            if type(latitude) != str and type(longitude) != str:
                latitude = config_int_error
                longitude = config_int_error
                boycott = True
            elif type(latitude) == str and type(longitude) == str:
                latitude = float(latitude)
                longitude = float(longitude)
        return latitude, longitude, boycott
    except:
        latitude = config_int_error
        longitude = config_int_error
        boycott = True
        return latitude, longitude, boycott
