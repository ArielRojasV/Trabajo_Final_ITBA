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


##Traigo info de las cotizaciones del dolar del BCRA

cotizaciones_divisa = confext.obtener_datos_BCRA( confext.obtener_url_moneda_fechas("cotizaciones" , "USD" ,  "2024-01-01" ,  datetime.today().strftime('%Y-%m-%d') ))

if cotizaciones_divisa:
    df_cotizaciones_divisa = pd.json_normalize(cotizaciones_divisa,  "detalle" , ["fecha"] )
    print(df_cotizaciones_divisa)


##Traigo info de variables economicas del BCRA

var_economicas_bcra = confext.obtener_datos_BCRA( confext.obtener_url_var_econ_bcra_fechas(  "2024-09-01" ,  "2024-09-11" ))

if var_economicas_bcra:
    df_var_economicas = pd.json_normalize(var_economicas_bcra  )
    print(df_var_economicas)





##Traigo info de cotizacion de Acciones de IOL

df_ext_final = pd.DataFrame()

for x in range(len(confext.acciones_list)):
    url = confext.obtener_url_IOL(confext.acciones_list[x])
   
    df_ext = pd.read_html(url)
    df_ext_tab = df_ext[1] 
    df_ext_tab['Accion'] = confext.acciones_list[x]

    df_ext_final = pd.concat([df_ext_final , df_ext_tab])


#Imprimo datos

df_ext_final = df_ext_final.rename(columns={'Fecha Cotización': 'FechaCotizacion', 'Máximo': 'Maximo', 'Mínimo': 'Minimo', 
                                            'Cierre ajustado': 'CierreAjustado' , 'Volumen Monto' :  'VolumenMonto',
                                            'Volumen Nominal':'VolumenNominal'})


print(df_ext_final)
print(df_ext_final.count())



##Inserto en Base de Datos

carga_bd.carga_dtf_to_bd(df_maestro_divisas, "lnd_moneda")
carga_bd.carga_dtf_to_bd(df_cotizaciones_divisa, "lnd_cotizaciones_monedas")
carga_bd.carga_dtf_to_bd(df_ext_final, "lnd_cotizaciones_acciones")



## Actualizo tabla cotizaciones final

carga_bd.actualizar_ft_cotizaciones_bd()
    
 