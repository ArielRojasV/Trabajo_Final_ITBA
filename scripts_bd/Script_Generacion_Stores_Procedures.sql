
--Creo Store Procedure para carga de cotizaciones de monedas en produccion

CREATE OR REPLACE PROCEDURE "2024_ariel_rojas_schema".sp_lk_cotizacion_monedas_add()
	LANGUAGE plpgsql
AS $$
	
BEGIN

insert into "2024_ariel_rojas_schema".lk_cotizacion_monedas
(id_moneda , id_tcl_dia, i_tipocambio, i_fec_modificacion) 
  
select 
lkm.id_moneda , 
dia.id_tcl_dia,   
mon.tipocotizacion,
CAST(GETDATE() AS DATE) as "fechamodificacion"
from "2024_ariel_rojas_schema".stg_cotizaciones_monedas mon
inner join "2024_ariel_rojas_schema".lk_tcl_dia dia 
on mon.fecha = dia.desc_tcl_dia
inner join  "2024_ariel_rojas_schema".lk_moneda lkm
on mon.codigomoneda = lkm.desc_abrmoneda
left join "2024_ariel_rojas_schema".lk_cotizacion_monedas lkc
on lkm.id_moneda = lkc.id_moneda
and dia.id_tcl_dia = lkc.id_tcl_dia
where lkc.id_moneda is null

;

END;

$$
;



--Creo Store Procedure para carga de tabla final de cotizaciones en produccion

CREATE OR REPLACE PROCEDURE "2024_ariel_rojas_schema".sp_ft_cotizaciones_add()
	LANGUAGE plpgsql
AS $$
	
BEGIN

insert into "2024_ariel_rojas_schema".ft_cotizaciones
(id_tcl_dia , id_accion, i_apertura, i_maximo, i_minimo, i_cierre, i_apertura_usd, i_maximo_usd, i_minimo_usd , i_cierre_usd  ) 
  
select
tbc.id_tcl_dia, 
tbc.id_accion,
tbc.apertura,
tbc.maximo,
tbc.minimo, 
tbc.cierre,
tbc.apertura_usd, 
tbc.maximo_usd, 
tbc.minimo_usd,  
tbc.cierre_usd  
from 
(	 
	select
	dia.id_tcl_dia, 
	acc.apertura, 
	acc.maximo, 
	acc.minimo, 
	acc.cierre,
	round((acc.apertura / mnd.tipocotizacion ),2) as apertura_usd, 
	round((acc.maximo / mnd.tipocotizacion ),2) as maximo_usd, 
	round((acc.minimo / mnd.tipocotizacion ),2) as minimo_usd,  
	round((acc.cierre / mnd.tipocotizacion ),2) as cierre_usd  ,
	lka.id_accion

	from "2024_ariel_rojas_schema".stg_cotizaciones_acciones  as acc
	inner join  "2024_ariel_rojas_schema".lk_tcl_dia as dia
	on acc.fechacotizacion  = dia.desc_tcl_dia 
	inner join "2024_ariel_rojas_schema".stg_cotizaciones_monedas as mnd
	on acc.fechacotizacion  = mnd.fecha
	inner join "2024_ariel_rojas_schema".lk_accion lka
	on acc.accion = lka.desc_sigla
)
as tbc
left join "2024_ariel_rojas_schema".ft_cotizaciones as ftc
on tbc.id_tcl_dia  = ftc.id_tcl_dia 
and tbc.id_accion = ftc.id_accion 
where ftc.id_accion is NULL;

END;

$$
;


--Creo Store Procedure para carga de cotizaciones de acciones en staging

CREATE OR REPLACE PROCEDURE "2024_ariel_rojas_schema".sp_stg_cotizaciones_acciones_add()
	LANGUAGE plpgsql
AS $$

BEGIN

insert into "2024_ariel_rojas_schema".stg_cotizaciones_acciones
(fechacotizacion , apertura, maximo, minimo, cierre, accion, fechamodificacion ) 
  
select 
lnd.fechacotizacion, 
lnd.apertura, 
lnd.maximo, 
lnd.minimo, 
lnd.cierre, 
lnd.accion,
CAST(GETDATE() AS DATE) as "fechamodificacion"
from "2024_ariel_rojas_schema".lnd_cotizaciones_acciones  lnd
left join "2024_ariel_rojas_schema".stg_cotizaciones_acciones stg
on lnd.fechacotizacion = stg.fechacotizacion
and lnd.accion = stg.accion
where stg.apertura is null;

END;

$$
;



--Creo Store Procedure para carga de cotizaciones de monedas en staging

CREATE OR REPLACE PROCEDURE "2024_ariel_rojas_schema".sp_stg_cotizaciones_monedas_add()
	LANGUAGE plpgsql
AS $$
	

BEGIN

insert into "2024_ariel_rojas_schema".stg_cotizaciones_monedas
(codigomoneda , tipocotizacion, fecha, fechamodificacion) 
  
select 
lnd.codigomoneda, 
lnd.tipocotizacion, 
lnd.fecha,
CAST(GETDATE() AS DATE) as "fechamodificacion"
from  "2024_ariel_rojas_schema".lnd_cotizaciones_monedas lnd
left join "2024_ariel_rojas_schema".stg_cotizaciones_monedas stg
on lnd.codigomoneda = stg.codigomoneda
and lnd.fecha = stg.fecha
where stg.tipocotizacion is null;

END;


$$
 