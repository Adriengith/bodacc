import tarfile
import os


                #NAME
                # try :
                #     search_name = avis.find('.//personneMorale')
                #     name = search_name.find('denomination').text
                #     #name = "name.denomination"
                #     companies_sucess_logs["name"] += 1
                # except :
                #     try :
                #         search_name = avis.find('.//personnePhysique')
                #         name = search_name.find('nomCommercial').text
                #         #name = "name.nomCommercial"
                #         companies_sucess_logs["name"] += 1
                #     except :
                #         try:
                #             search_name = avis.find('.//etablissement')
                #             name = search_name.find('enseigne').text
                #             #name = "name.enseigne"
                #             companies_sucess_logs["name"] += 1
                #         except:
                #             try:
                #                 search_name = avis.find('.//personnePhysique')
                #                 name = search_name.find('nom').text
                #                 #name = "name.enseigne"
                #                 companies_sucess_logs["name"] += 1
                #             except:
                #                 name = "ERROR"
                #                 companies_errors_logs["name"] += 1




                #name
                # try :  
                #     search_name = avis.find('.//precedentProprietairePM')
                #     name = search_name.find('denomination').text
                #     companies_sucess_logs["name"] += 1
                # except :
                #     try :
                #         search_name = avis.find('.//precedentProprietairePP')
                #         name = search_name.find('nomUsage').text
                #         companies_sucess_logs["name"] += 1
                #     except :
                #         try :
                #             search_name = avis.find('.//precedentProprietairePP')
                #             name = search_name.find('nom').text
                #             companies_sucess_logs["name"] += 1
                #         except :
                #             name = "ERROR_5432873"
                #             companies_errors_logs["name"] += 1




                    # #address place si pas trouvé dans api
                    # if len(address) == 31:
                    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    #     try :  
                    #         search_adr = avis.find('.//personne')
                    #         search_adresse = search_adr.find('adresse')
                    #         search_numeroImmatriculation = search_adresse.find('france')
                    #         ###############

                    #         try:  #bon
                    #             voie_number = search_voie_number.find('numeroVoie').text
                    #         except:
                    #             voie_number = ""

                    #         try : #bon
                    #             type_rue = search_type_rue.find('typeVoie').text

                    #         except:
                    #             type_rue = ""

                    #         try: #bon
                    #             name_voie = search_name_voie.find('nomVoie').text
                    #         except:
                    #             name_voie = ""


                    #         try: # bon
                    #             compl_geo = search_name_voie.find('complGeografhique').text
                    #         except:
                    #             compl_geo = ""

                    #         try: #bon
                    #             bp = search_name_voie.find('BP').text
                    #         except:
                    #             bp = ""

                    #         try: #
                    #             localite = search_name_voie.find('localite').text
                    #         except:
                    #             localite = ""


                    #         try: #bon
                    #             zipcode = search_zipcode.find('codePostal').text

                    #             try: #bon
                    #                 department = zipcode[0:2]
                    #             except:
                    #                 department = ""
                    #         except:
                    #             zipcode = ""


                    #         try: #bon
                    #             city = search_city.find('ville').text
                    #         except:
                    #             city = ""

                    #         address = voie_number + type_rue + name_voie + compl_geo + bp + localite + zipcode + ' ' + city

                    #         #companies_sucess_logs["siren"] += 1
                    #     except :
                    #         try:
                    #             search_siren = avis.find('.//personne')
                    #             search_numeroImma = search_siren.find('adresse')
                    #             search_numeroImmatriculation = search_siren.find('etranger')


                    #             #companies_sucess_logs["siren"] += 1
                    #         except:
                    #             #companies_errors_logs["siren"] += 1
                    #             pass




def unzip_BODACC_2016_tar() :
    nbtar = 0
    nbtaz = 0
    folder_BODACC_2016 = 'BODACC_xml/BODACC_2016'
    fname = 'BODACC_tar/BODACC_2016.tar'



    #1  ON DEZIPE LE FICHIER PRINCIPAL
    
    print("unzip >", fname,"...")

    if fname.endswith("tar"):
        tar = tarfile.open(fname, "r:tar")
        tar.extractall(folder_BODACC_2016)
        tar.close()
        print(">>>",fname,">",folder_BODACC_2016," DONE !\n-----------------------------------------")

    elif fname.endswith("taz"):
        tar = tarfile.open(fname, "r")
        tar.extractall(folder_BODACC_2016)
        tar.close()
        print(">>>",fname,">",folder_BODACC_2016," DONE !\n-----------------------------------------")



    #2  ON DEZIPE TOUT LES FICHIERS ZIPPE QUI VIENNENT DU FICHIER PRINCIPAL

    list_unzip = os.listdir(folder_BODACC_2016)
    print("unzip >",len(list_unzip),"files in :",folder_BODACC_2016,"...")


    for onefile in list_unzip :
        onefile = folder_BODACC_2016 + '/' + onefile

        if onefile.endswith("tar"):
            try :
                tar = tarfile.open(onefile, "r:tar")
                tar.extractall(folder_BODACC_2016)
                tar.close()
                os.remove(onefile)
                nbtar += 1
            except :
                pass
        elif onefile.endswith("taz"):
            try :
                tar = tarfile.open(onefile, "r")
                tar.extractall(folder_BODACC_2016)
                tar.close()
                os.remove(onefile)
                nbtaz += 1
            except :
                pass
    print(">>> Tar files unzipped >",nbtar,"|| Taz files unzipped >",nbtaz," !")



def bug_pour_jo() :
    
    onefile = 'RCS-B_BXB20160256.taz'
    onefile = 'PCL_BXA20160074.taz'

    if onefile.endswith("tar"):
        try :
            tar = tarfile.open(onefile, "r:tar")
            tar.extractall()
            tar.close()
            print("GOOD1")
        except :
            pass
    elif onefile.endswith("taz"):
        try :
            tar = tarfile.open(onefile, "r")
            tar.extractall()
            tar.close()
            print("GOOD2")
        except :
            pass




def salut():
    print("Salut")






#unzip_BODACC_2016_tar()
#bug_pour_jo()