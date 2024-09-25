import requests as req


#################Variables IOL##########################
##EndPoints a Consultar
endp_divisas = "Maestros/Divisas"
endp_cotiz = "Cotizaciones/"

#Lista de Acciones
acciones_list = ["YPF", "ALUAR", "MACRO", "GALICIA", "EDENOR"]
#################Variables IOL##########################




## Obtengo la URL para consultar en IOL
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


## Obtengo URL para consultar datos cambiarios al BCRA
def obtener_url_divisas_bcra(endpoint):  
    ##Defino Variable de URL
    base_url = "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/"
    match endpoint:
        case "divisas": 
            return base_url + "Maestros/Divisas"
        case "cotizaciones":
            return base_url + "Cotizaciones/"  


## Obtengo URL con filtro de fechas
def obtener_url_moneda_fechas(endpoint, moneda, fechadesde , fechahasta ): 
    return obtener_url_divisas_bcra(endpoint) + moneda + "?fechadesde=" + fechadesde + "&fechahasta=" + fechahasta


## Obtengo URL de estadisticas del BCRA
def obtener_url_var_econ_bcra_fechas(fechadesde , fechahasta):  
    ##Defino Variable de URL
    base_url = "https://api.bcra.gob.ar/estadisticas/v2.0/datosvariable/1/"
    return base_url + fechadesde + "/" + fechahasta


##Obtengo datos del BCRA
def obtener_datos_BCRA(endpoint_url):     
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
    




