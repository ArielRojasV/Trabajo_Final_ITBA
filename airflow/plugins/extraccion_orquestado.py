from typing import Union, Dict, List
import pandas as pd
import json  
import carga_bd_orquestado as  carga_bd
import config_extraccion_orquestado as confext


## Traigo info de las cotizaciones del dolar del BCRA    
def extraer_datos_BCRA():
    fecha_ultcarga_cotizaciones = carga_bd.get_fechaultima_entidad_bd("moneda")
    fecha_desde_cotizaciones = pd.to_datetime(fecha_ultcarga_cotizaciones) +  pd.DateOffset(days=1) 
    fecha_desde_cotizaciones = fecha_desde_cotizaciones.strftime('%Y-%m-%d')

    fecha_hasta_cotizaciones = pd.Timestamp("today").strftime('%Y-%m-%d')

    cotizaciones_divisa = confext.obtener_datos_BCRA( confext.obtener_url_moneda_fechas("cotizaciones" , "USD" ,  fecha_desde_cotizaciones , fecha_hasta_cotizaciones  ))

    if cotizaciones_divisa:
        df_cotizaciones_divisa = pd.json_normalize(cotizaciones_divisa,  "detalle" , ["fecha"] )
        ##print(df_cotizaciones_divisa)
        ##Inserto en Base de Datos
        carga_bd.carga_dtf_to_bd(df_cotizaciones_divisa, "lnd_cotizaciones_monedas")


 ## Extraigo info de la web de IOL
def extraer_datos_IOL():   
    fecha_ultcarga_acciones = carga_bd.get_fechaultima_entidad_bd("accion")
    acciones = carga_bd.get_codigo_acciones() 

    for accion in acciones:
        df_ext_final = pd.DataFrame()
        url = confext.obtener_url_IOL(str(accion))    

        df_ext = pd.read_html(url)
        df_ext_tab = df_ext[1] 
        df_ext_tab['Accion'] = accion

        df_ext_final = df_ext_tab.rename(columns={'Fecha Cotización': 'FechaCotizacion', 'Máximo': 'Maximo', 'Mínimo': 'Minimo', 
                                            'Cierre ajustado': 'CierreAjustado' , 'Volumen Monto' :  'VolumenMonto',
                                            'Volumen Nominal':'VolumenNominal'})      

        df_ext_final['FechaCotizacion'] = pd.to_datetime(df_ext_final['FechaCotizacion'] )

        df_ext_final = df_ext_final.loc[ ( df_ext_final['FechaCotizacion'] > fecha_ultcarga_acciones ) ]
     
        carga_bd.carga_dtf_to_bd(df_ext_final, "lnd_cotizaciones_acciones")
    

## Actualizo staging de tablas de monedas y tabla final
def carga_staging():        
    carga_bd.ejecutar_sp_staging_bd("sp_stg_cotizaciones_monedas_add()")
    carga_bd.ejecutar_sp_staging_bd("sp_stg_cotizaciones_acciones_add()")


## Actualizo staging de tablas de cotizaciones de acciones y tabla final
def carga_produccion():    
    carga_bd.ejecutar_sp_produccion_bd("sp_lk_cotizacion_monedas_add()")
    carga_bd.ejecutar_sp_produccion_bd("sp_ft_cotizaciones_add()") 




"""
##Traigo info del maestro de divisas del BCRA

maestro_divisas = confext.obtener_datos_BCRA(confext.obtener_url_divisas_bcra("divisas"))

if maestro_divisas:
    df_maestro_divisas = pd.DataFrame(maestro_divisas)  
    print(df_maestro_divisas)
    
    ##Inserto en Base de Datos
    carga_bd.carga_dtf_to_bd(df_maestro_divisas, "lnd_moneda")


##Traigo info de variables economicas del BCRA

var_economicas_bcra = confext.obtener_datos_BCRA( confext.obtener_url_var_econ_bcra_fechas(  "2024-09-01" ,  "2024-09-11" ))

if var_economicas_bcra:
    df_var_economicas = pd.json_normalize(var_economicas_bcra  )
    print(df_var_economicas)
"""
 
