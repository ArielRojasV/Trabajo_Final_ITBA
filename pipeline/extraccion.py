import pandas as pd
import requests as req
from typing import Union, Dict, List
from sqlalchemy import create_engine
import json  


#################Variables##########################
##EndPoints a Consultar
endp_divisas = "Maestros/Divisas"
endp_cotiz = "Cotizaciones/"
#Lista de Acciones
acciones_list = ["YPF", "ALUAR", "MACRO", "GALICIA", "EDENOR"]
#################Variables##########################


#################Variables de Conexion##########################
redshift_user = "2024_ariel_rojas"
redshift_pass = "F9!L2^&6$xQ"
redshift_endpoint = "redshift-pda-cluster.cnuimntownzt.us-east-2.redshift.amazonaws.com"
port = 5439  
database = "pda"
#################Variables##########################
 



def carga_dtf_to_bd(df, table): 

    connection_string = f"postgresql://{redshift_user}:{redshift_pass}@{redshift_endpoint}:{port}/{database}"
    engine = create_engine(connection_string)
    
    try:
        with engine.connect() as connection:
            print("Conexion Exitosa")
            
            df.to_sql(name= table, con=engine, schema='2024_ariel_rojas_schema', if_exists='append', index=False)

    except Exception as e:
        print(f"Error connecting to Redshift: {e}")


def obtener_url_divisas_bcra(endpoint):  
    ##Defino Variable de URL
    base_url = "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/"
    match endpoint:
        case "divisas": 
            return base_url + "Maestros/Divisas"
        case "cotizaciones":
            return base_url + "Cotizaciones/"  

def obtener_url_moneda_fechas(endpoint, moneda, fechadesde , fechahasta ): 
    return obtener_url_divisas_bcra(endpoint) + moneda + "?fechadesde=" + fechadesde + "&fechahasta=" + fechahasta


def obtener_url_var_econ_bcra_fechas(fechadesde , fechahasta):  
    ##Defino Variable de URL
    base_url = "https://api.bcra.gob.ar/estadisticas/v2.0/datosvariable/1/"
    return base_url + fechadesde + "/" + fechahasta

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

maestro_divisas = obtener_datos(obtener_url_divisas_bcra("divisas"))

if maestro_divisas:
    df_maestro_divisas = pd.DataFrame(maestro_divisas)  
    print(df_maestro_divisas)


##Traigo info de las cotizaciones del dolar del BCRA

cotizaciones_divisa = obtener_datos( obtener_url_moneda_fechas("cotizaciones" , "USD" ,  "2024-01-01" ,  "2024-09-11" ))

if cotizaciones_divisa:
    df_cotizaciones_divisa = pd.json_normalize(cotizaciones_divisa,  "detalle" , ["fecha"] )
    print(df_cotizaciones_divisa)


##Traigo info de variables economicas del BCRA

var_economicas_bcra = obtener_datos( obtener_url_var_econ_bcra_fechas(  "2024-09-01" ,  "2024-09-11" ))

if var_economicas_bcra:
    df_var_economicas = pd.json_normalize(var_economicas_bcra  )
    print(df_var_economicas)



##Traigo info de cotizacion de Acciones de IOL

""""
df_ext_final = pd.DataFrame()

for x in range(len(acciones_list)):
    url = obtener_url_IOL(acciones_list[x])
   
    df_ext = pd.read_html(url)
    df_ext_tab = df_ext[1] 
    df_ext_tab['Accion'] = acciones_list[x]

    df_ext_final = pd.concat([df_ext_final , df_ext_tab])


#Imprimo datos

df_ext_final = df_ext_final.rename(columns={'Fecha Cotización': 'FechaCotizacion', 'Máximo': 'Maximo', 'Mínimo': 'Minimo', 
                                            'Cierre ajustado': 'CierreAjustado' , 'Volumen Monto' :  'VolumenMonto',
                                            'Volumen Nominal':'VolumenNominal'})


print(df_ext_final)
print(df_ext_final.count())
"""



##Inserto en Base de Datos
##carga_dtf_to_bd(df_maestro_divisas, "lnd_moneda")
##carga_dtf_to_bd(df_cotizaciones_divisa, "lnd_cotizaciones_monedas")
##carga_dtf_to_bd(df_ext_final, "lnd_cotizaciones_acciones")




    
 