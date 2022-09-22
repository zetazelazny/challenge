import pandas as pd
from datetime import date
from functions import download_file, create_path, get_data_frame, get_engine_from_settings, get_session, insert_dataframe_to_db, add_load_date
from constants import PATH_MUSEOS, PATH_CINES, PATH_BIBLIOTECAS, FILE_PREFIX_BIBLIOTECAS, FILE_PREFIX_CINES, FILE_PREFIX_MUSEOS, URL_BIBLIOTECAS, URL_CINES, URL_MUSEOS, EXTENSION

pd.set_option('chained_assignment', None)

path_date = date.today().strftime("%Y-%B")

path_museos = PATH_MUSEOS + path_date
path_cines = PATH_CINES + path_date
path_bibliotecas = PATH_BIBLIOTECAS + path_date

create_path(path_museos)
create_path(path_cines)
create_path(path_bibliotecas)

current_date = date.today().strftime("%d-%m-%Y")

file_name_museos = FILE_PREFIX_MUSEOS + current_date + EXTENSION
file_name_cines = FILE_PREFIX_CINES + current_date + EXTENSION
file_name_bibliotecas = FILE_PREFIX_BIBLIOTECAS + current_date + EXTENSION

download_file(URL_MUSEOS, path_museos + "\\" + file_name_museos)    
download_file(URL_CINES, path_cines + "\\" + file_name_cines) 
download_file(URL_BIBLIOTECAS, path_bibliotecas + "\\" + file_name_bibliotecas) 

df_bibliotecas = get_data_frame(path_bibliotecas, file_name_bibliotecas)
df_bibliotecas.rename(columns = {'IdProvincia':'Id_Provincia', 'IdDepartamento':'Id_Departamento', 'Categoría':'categoria', 'Observacion':'Observaciones', 'Cod_tel':'Cod_Area', 'Teléfono':'Telefono', 'Información adicional':'Info_adicional', 'TipoLatitudLongitud':'Tipo_Latitud_Longitud', 'año_inicio':'año_inauguracion'}, inplace = True)
df_bibliotecas.columns = df_bibliotecas.columns.str.upper()

df_museos = get_data_frame(path_museos, file_name_museos)
df_museos.rename(columns = {'IdProvincia':'Id_Provincia', 'IdDepartamento':'Id_Departamento', 'direccion':'Domicilio', 'cod_area':'Cod_Area', 'TipoLatitudLongitud':'Tipo_Latitud_Longitud', 'actualizacion':'año_actualizacion'}, inplace = True)
df_museos.columns = df_museos.columns.str.upper()

df_cines = get_data_frame(path_cines, file_name_cines)
df_cines.rename(columns = {'IdProvincia':'Id_Provincia', 'IdDepartamento':'Id_Departamento', 'Dirección':'Domicilio', 'Categoría':'categoria', 'Teléfono':'telefono', 'Información adicional':'Info_adicional', 'TipoLatitudLongitud':'Tipo_Latitud_Longitud'}, inplace = True)
df_cines.columns = df_cines.columns.str.upper()
df_cines['ESPACIO_INCAA'] = df_cines['ESPACIO_INCAA'].str.upper()
df_cines['ESPACIO_INCAA'] = df_cines['ESPACIO_INCAA'].str.replace('SI', '1')
df_cines['ESPACIO_INCAA'] = df_cines['ESPACIO_INCAA'].fillna(0)
df_cines['ESPACIO_INCAA'] = df_cines['ESPACIO_INCAA'].astype(str).astype(int)

conc_df = pd.concat([df_bibliotecas, df_cines, df_museos])
df_cols = conc_df[['COD_LOC', 'ID_PROVINCIA', 'ID_DEPARTAMENTO', 'CATEGORIA', 'PROVINCIA', 'LOCALIDAD', 'NOMBRE', 'DOMICILIO', 'CP', 'TELEFONO', 'MAIL', 'WEB']]
df_cols['CP'] = df_cols['CP'].str.extract('(\d+)')

engine = get_engine_from_settings()
session = get_session()

df_by_cat = conc_df.groupby(['CATEGORIA']).size().groupby(level=0).max().reset_index(name='CANTIDAD_REGISTROS')
df_by_fuente = conc_df.groupby(['FUENTE']).size().groupby(level=0).max().reset_index(name='CANTIDAD_REGISTROS')
df_by_prov_cat = conc_df.groupby(['PROVINCIA', 'CATEGORIA']).size().groupby(level=0).max().reset_index(name='CANTIDAD_REGISTROS')

df_pantallas_cines = df_cines.groupby(['PROVINCIA'])['PANTALLAS'].sum().reset_index(name='CANTIDAD_PANTALLAS')
df_butacas_cines = df_cines.groupby(['PROVINCIA'])['BUTACAS'].sum().reset_index(name='CANTIDAD_BUTACAS')
df_espacios_cines = df_cines.groupby(['PROVINCIA'])['ESPACIO_INCAA'].sum().reset_index(name='CANTIDAD_ESPACIOS_INCAA')

df_tabla_cines = pd.merge(df_pantallas_cines, df_butacas_cines, on='PROVINCIA')
df_tabla_cines = pd.merge(df_tabla_cines, df_espacios_cines, on='PROVINCIA')

df_cols = add_load_date(df_cols)
df_by_cat = add_load_date(df_by_cat)
df_by_fuente = add_load_date(df_by_fuente)
df_by_prov_cat = add_load_date(df_by_prov_cat)
df_tabla_cines = add_load_date(df_tabla_cines)

insert_dataframe_to_db(df_cols, 'datos_argentina', engine, 'replace')
insert_dataframe_to_db(df_by_cat, 'registros_x_categoria', engine, 'replace')
insert_dataframe_to_db(df_by_fuente, 'registros_x_fuente', engine, 'replace')
insert_dataframe_to_db(df_by_prov_cat, 'registros_x_prov_cat', engine, 'replace')
insert_dataframe_to_db(df_tabla_cines, 'info_cines', engine, 'replace')