import pandas as pd
import requests as req
from typing import Union, Dict, List
import json  

#################Variables##########################
##EndPoints a Consultar
endp_divisas = "Maestros/Divisas"
endp_cotiz = "Cotizaciones/"
#Lista de Acciones
acciones_list = ["YPF", "ALUAR", "MACRO", "GALICIA", "EDENOR"]
#################Variables##########################

 
def obtener_url(endpoint):  
    ##Defino Variable de URL
    base_url = "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/"
    match endpoint:
        case "divisas": 
            return base_url + "Maestros/Divisas"
        case "cotizaciones":
            return base_url + "Cotizaciones/"  


def obtener_url_moneda_fechas(endpoint, moneda, fechadesde , fechahasta ): 
    return obtener_url(endpoint) + moneda + "?fechadesde=" + fechadesde + "&fechahasta=" + fechahasta
 

def obtener_datos(endpoint_url):     
    print(endpoint_url)
    try:              
        response = req.get(endpoint_url, verify=False) ##Las APIS no requieren Tokens         
        response.raise_for_status()  # Excepción si hay error en la respuesta
 
        # Verificar si los datos están en formato JSON.
        try:
            json_data = response.json()['results']                      
        except:
            print("Formato no reconocido")
            return None
        return json_data

    except req.exceptions.RequestException as e:
        # Capturar error de solicitud
        print(f"La petición ha fallado. Error : {e}")
        return None
 
 
def obtener_url_IOL(accion):
    basic_url = "https://iol.invertironline.com/Titulo/DatosHistoricos?simbolo="
    fin_url = "&mercado=BCBA" 
    match accion:
        case "YPF": 
            return basic_url + "YPFD" + fin_url   
        case "ALUAR":
            return basic_url + "ALUA" + fin_url
        case "MACRO":
            return basic_url + "BMA" + fin_url
        case "GALICIA":
            return basic_url + "GGAL" + fin_url
        case "EDENOR":
            return basic_url + "EDN" + fin_url


################################################

##Traigo info del maestro de divisas del BCRA

maestro_divisas = obtener_datos(obtener_url("divisas"))

if maestro_divisas:
    df_maestro_divisas = pd.DataFrame(maestro_divisas)  
    print(df_maestro_divisas)


##Traigo info de las cotizaciones del dolar del BCRA

cotizaciones_divisa = obtener_datos( obtener_url_moneda_fechas("cotizaciones" , "USD" ,  "2024-01-01" ,  "2024-09-11" ))

if cotizaciones_divisa:
    df_cotizaciones_divisa = pd.json_normalize(cotizaciones_divisa,  "detalle" , ["fecha"] )
    print(df_cotizaciones_divisa)


##Traigo info de cotizacion de Acciones de IOL

df_ext_final = pd.DataFrame()

for x in range(len(acciones_list)):
    url = obtener_url_IOL(acciones_list[x])
   
    df_ext = pd.read_html(url)
    df_ext_tab = df_ext[1] 
    df_ext_tab['Accion'] = acciones_list[x]

    df_ext_final = pd.concat([df_ext_final , df_ext_tab])


#Imprimo datos
print(df_ext_final)
print(df_ext_final.count())





    
 