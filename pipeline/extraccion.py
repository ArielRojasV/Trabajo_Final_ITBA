import pandas as pd

url = "https://iol.invertironline.com/Titulo/DatosHistoricos?simbolo=YPFD&mercado=BCBA" 
df_ypf_ext = pd.read_html(url)

df_ypl = df_ypf_ext[1]

print(df_ypl)
