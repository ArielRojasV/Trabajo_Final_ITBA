import pandas as pd

#URL de acciones de YPF
url = "https://iol.invertironline.com/Titulo/DatosHistoricos?simbolo=YPFD&mercado=BCBA" 
df_ypf_ext = pd.read_html(url)

df_ypl = df_ypf_ext[1]

#Imprimo datos
print(df_ypl)
