from typing import Union, Dict, List
from datetime import datetime
import pandas as pd
import json  
import config_extraccion as confext
import carga_bd  



################################################

##Traigo info del maestro de divisas del BCRA

maestro_divisas = confext.obtener_datos_BCRA(confext.obtener_url_divisas_bcra("divisas"))

if maestro_divisas:
    df_maestro_divisas = pd.DataFrame(maestro_divisas)  
    print(df_maestro_divisas)
    
    ##Inserto en Base de Datos
    carga_bd.carga_dtf_to_bd(df_maestro_divisas, "lnd_moneda")




##Traigo info de las cotizaciones del dolar del BCRA

cotizaciones_divisa = confext.obtener_datos_BCRA( confext.obtener_url_moneda_fechas("cotizaciones" , "USD" ,  "2023-01-01" ,  datetime.today().strftime('%Y-%m-%d') ))

if cotizaciones_divisa:
    df_cotizaciones_divisa = pd.json_normalize(cotizaciones_divisa,  "detalle" , ["fecha"] )
    print(df_cotizaciones_divisa)

    ##Inserto en Base de Datos
    carga_bd.carga_dtf_to_bd(df_cotizaciones_divisa, "lnd_cotizaciones_monedas")


##Traigo info de variables economicas del BCRA
""""
var_economicas_bcra = confext.obtener_datos_BCRA( confext.obtener_url_var_econ_bcra_fechas(  "2024-09-01" ,  "2024-09-11" ))

if var_economicas_bcra:
    df_var_economicas = pd.json_normalize(var_economicas_bcra  )
    print(df_var_economicas)
"""


##Traigo info de cotizacion de Acciones de IOL

for x in range(len(confext.acciones_list)):
    url = confext.obtener_url_IOL(confext.acciones_list[x])
    df_ext_final = pd.DataFrame()

    df_ext = pd.read_html(url)
    df_ext_tab = df_ext[1] 
    df_ext_tab['Accion'] = confext.acciones_list[x]

    #df_ext_final = pd.concat([df_ext_final , df_ext_tab])

    df_ext_final = df_ext_tab.rename(columns={'Fecha Cotización': 'FechaCotizacion', 'Máximo': 'Maximo', 'Mínimo': 'Minimo', 
                                            'Cierre ajustado': 'CierreAjustado' , 'Volumen Monto' :  'VolumenMonto',
                                            'Volumen Nominal':'VolumenNominal'})     
 

    df_ext_final['FechaCotizacion'] = pd.to_datetime(df_ext_final['FechaCotizacion'] )
    print(df_ext_final)  

    df_ext_final = df_ext_final.loc[(df_ext_final['FechaCotizacion'] >= '2024-09-01')]

    #print(df_ext_final)
    print(df_ext_final.count())

    carga_bd.carga_dtf_to_bd(df_ext_final, "lnd_cotizaciones_acciones")





            
## Actualizo tabla de base de datos
carga_bd.actualizar_lk_cotizacion_monedas_bd()
carga_bd.actualizar_stg_cotizaciones_monedas_bd()
carga_bd.actualizar_stg_cotizaciones_acciones_bd()
carga_bd.actualizar_ft_cotizaciones_bd() 
 
