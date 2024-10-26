
--Crear Esquema BD
CREATE SCHEMA "2024_ariel_rojas_schema";

--Tabla de Landing para las cotizaciones de acciones
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".lnd_cotizaciones_acciones
(
	fechacotizacion DATE NOT NULL  ENCODE az64
	,apertura DOUBLE PRECISION   ENCODE RAW
	,maximo DOUBLE PRECISION   ENCODE RAW
	,minimo DOUBLE PRECISION   ENCODE RAW
	,cierre DOUBLE PRECISION   ENCODE RAW
	,cierreajustado DOUBLE PRECISION   ENCODE RAW
	,volumenmonto DOUBLE PRECISION   ENCODE RAW
	,volumennominal DOUBLE PRECISION   ENCODE RAW
	,accion CHAR(256) NOT NULL  ENCODE lzo
	,PRIMARY KEY (fechacotizacion, accion)
)
DISTSTYLE AUTO
;
ALTER TABLE "2024_ariel_rojas_schema".lnd_cotizaciones_acciones owner to "2024_ariel_rojas";


--Tabla de Landing para las cotizaciones de monedas
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".lnd_cotizaciones_monedas
(
	codigomoneda CHAR(5) NOT NULL  ENCODE lzo
	,descripcion CHAR(35) NOT NULL  ENCODE lzo
	,tipopase DOUBLE PRECISION   ENCODE RAW
	,tipocotizacion DOUBLE PRECISION   ENCODE RAW
	,fecha DATE NOT NULL  ENCODE az64
	,PRIMARY KEY (codigomoneda, fecha)
)
DISTSTYLE AUTO
;
ALTER TABLE "2024_ariel_rojas_schema".lnd_cotizaciones_monedas owner to "2024_ariel_rojas";


--Tabla de Landing para guardar maestro de monedas
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".lnd_moneda
(
	codigo CHAR(5) NOT NULL  ENCODE lzo
	,denominacion CHAR(35) NOT NULL  ENCODE lzo
	,PRIMARY KEY (codigo)
)
DISTSTYLE AUTO
;
ALTER TABLE "2024_ariel_rojas_schema".lnd_moneda owner to "2024_ariel_rojas";



--Tabla de Staging para las cotizaciones de acciones
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".stg_cotizaciones_acciones
(
	fechacotizacion DATE NOT NULL  ENCODE az64
	,apertura DOUBLE PRECISION   ENCODE RAW
	,maximo DOUBLE PRECISION   ENCODE RAW
	,minimo DOUBLE PRECISION   ENCODE RAW
	,cierre DOUBLE PRECISION   ENCODE RAW
	,accion CHAR(256) NOT NULL  ENCODE lzo
	,fechamodificacion DATE NOT NULL  ENCODE az64
	,PRIMARY KEY (fechacotizacion, accion)
)
DISTSTYLE AUTO
 DISTKEY (accion)
 SORTKEY (
	fechacotizacion
	)
;
ALTER TABLE "2024_ariel_rojas_schema".stg_cotizaciones_acciones owner to "2024_ariel_rojas";


--Tabla de Staging para las cotizaciones de monedas
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".stg_cotizaciones_monedas
(
	codigomoneda CHAR(5) NOT NULL  ENCODE lzo
	,tipocotizacion DOUBLE PRECISION   ENCODE RAW
	,fecha DATE NOT NULL  ENCODE az64
	,fechamodificacion DATE NOT NULL  ENCODE az64
	,PRIMARY KEY (codigomoneda, fecha)
)
DISTSTYLE AUTO
 DISTKEY (codigomoneda)
 SORTKEY (
	codigomoneda
	)
;
ALTER TABLE "2024_ariel_rojas_schema".stg_cotizaciones_monedas owner to "2024_ariel_rojas";


--Tabla de Produccion que guarda un calendario , no se carga por ETL
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".lk_tcl_dia
(
	id_tcl_dia INTEGER NOT NULL  ENCODE az64
	,desc_tcl_dia DATE NOT NULL  ENCODE az64
	,desc_tcl_diasemana CHAR(15) NOT NULL  ENCODE lzo
	,desc_tcl_mesanio INTEGER   ENCODE az64
	,PRIMARY KEY (id_tcl_dia)
)
DISTSTYLE AUTO
;
ALTER TABLE "2024_ariel_rojas_schema".lk_tcl_dia owner to "2024_ariel_rojas";


--Tabla de Produccion que guarda maestro de monedas
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".lk_moneda
(
	id_moneda INTEGER NOT NULL DEFAULT "identity"(200826, 0, '0,1'::text) ENCODE az64
	,desc_abrmoneda CHAR(12) NOT NULL  ENCODE lzo
	,desc_moneda CHAR(55) NOT NULL  ENCODE lzo
	,PRIMARY KEY (id_moneda)
)
DISTSTYLE AUTO
 DISTKEY (id_moneda)
 SORTKEY (
	id_moneda
	)
;
ALTER TABLE "2024_ariel_rojas_schema".lk_moneda owner to "2024_ariel_rojas";


--Tabla de Produccion que guarda cotizacion de monedas
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".lk_cotizacion_monedas
(
	id_moneda INTEGER NOT NULL  ENCODE az64
	,id_tcl_dia INTEGER NOT NULL  ENCODE az64
	,i_tipocambio DOUBLE PRECISION   ENCODE RAW
	,i_fec_modificacion DATE   ENCODE az64
	,PRIMARY KEY (id_moneda, id_tcl_dia)
)
DISTSTYLE AUTO
 DISTKEY (id_moneda)
 SORTKEY (
	id_moneda
	)
;
ALTER TABLE "2024_ariel_rojas_schema".lk_cotizacion_monedas owner to "2024_ariel_rojas";


--Tabla de Produccion que guarda maestro de acciones
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".lk_accion
(
	id_accion INTEGER NOT NULL  ENCODE az64
	,desc_accion CHAR(15) NOT NULL  ENCODE lzo
	,id_flg_activo CHAR(1)   ENCODE lzo
	,desc_sigla CHAR(7)   ENCODE lzo
	,PRIMARY KEY (id_accion)
)
DISTSTYLE AUTO
;
ALTER TABLE "2024_ariel_rojas_schema".lk_accion owner to "2024_ariel_rojas";


--Tabla de Produccion que guarda cotizaciones en pesos y dolares
CREATE TABLE IF NOT EXISTS "2024_ariel_rojas_schema".ft_cotizaciones
(
	id_tcl_dia INTEGER NOT NULL  ENCODE az64
	,id_accion INTEGER NOT NULL  ENCODE az64
	,i_apertura DOUBLE PRECISION   ENCODE RAW
	,i_maximo DOUBLE PRECISION   ENCODE RAW
	,i_minimo DOUBLE PRECISION   ENCODE RAW
	,i_cierre DOUBLE PRECISION   ENCODE RAW
	,i_apertura_usd DOUBLE PRECISION   ENCODE RAW
	,i_maximo_usd DOUBLE PRECISION   ENCODE RAW
	,i_minimo_usd DOUBLE PRECISION   ENCODE RAW
	,i_cierre_usd DOUBLE PRECISION   ENCODE RAW
	,PRIMARY KEY (id_tcl_dia, id_accion)
)
DISTSTYLE AUTO
 DISTKEY (id_tcl_dia)
 SORTKEY (
	id_tcl_dia
	)
;
ALTER TABLE "2024_ariel_rojas_schema".ft_cotizaciones owner to "2024_ariel_rojas";



