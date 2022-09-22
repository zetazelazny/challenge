CREATE TABLE IF NOT EXISTS public.datos_argentina
(
    index bigint,
    "COD_LOC" bigint,
    "ID_PROVINCIA" bigint,
    "ID_DEPARTAMENTO" bigint,
    "CATEGORIA" text COLLATE pg_catalog."default",
    "PROVINCIA" text COLLATE pg_catalog."default",
    "LOCALIDAD" text COLLATE pg_catalog."default",
    "NOMBRE" text COLLATE pg_catalog."default",
    "DOMICILIO" text COLLATE pg_catalog."default",
    "CP" text COLLATE pg_catalog."default",
    "TELEFONO" text COLLATE pg_catalog."default",
    "MAIL" text COLLATE pg_catalog."default",
    "WEB" text COLLATE pg_catalog."default",
    "FECHA_CARGA" text COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.info_cines
(
    index bigint,
    "PROVINCIA" text COLLATE pg_catalog."default",
    "CANTIDAD_PANTALLAS" bigint,
    "CANTIDAD_BUTACAS" bigint,
    "CANTIDAD_ESPACIOS_INCAA" integer,
    "FECHA_CARGA" text COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.registros_x_categoria
(
    index bigint,
    "CATEGORIA" text COLLATE pg_catalog."default",
    "CANTIDAD_REGISTROS" bigint,
    "FECHA_CARGA" text COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.registros_x_fuente
(
    index bigint,
    "FUENTE" text COLLATE pg_catalog."default",
    "CANTIDAD_REGISTROS" bigint,
    "FECHA_CARGA" text COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.registros_x_prov_cat
(
    index bigint,
    "PROVINCIA" text COLLATE pg_catalog."default",
    "CANTIDAD_REGISTROS" bigint,
    "FECHA_CARGA" text COLLATE pg_catalog."default"
);
