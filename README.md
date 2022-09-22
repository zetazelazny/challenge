# Descarga de proyecto

Clonar desde GitHub a un directorio local mediante el comando
	
	git clone https://github.com/zetazelazny/challenge


# Instalación y activación del entorno virtual

Ejecutar desde el directorio donde se descargo el repositorio el comando 
	
	pip install virtualenv

Una vez instalado, ejecutar el comando
	
	virtualenv [nombre]

Cuando termine de crear el entorno virtual, se debe ejecutar
	
	env/Scripts/activate

# Instalacion de librerias necesarias

Una vez inicializado el entorno virtual, ejecutar los siguientes comandos:
- pip install pandas
- pip install psycopg2
- pip install python-decouple
- pip install python-dotenv 
- pip install requests
- pip install SQLAlchemy
- pip install SQLAlchemy-Utils

# Configuración de conexión a la base de datos

Para configurar la información necesaria para lograr la conexión, se deben modificar las variables en el archivo .env

# Ejecucion del programa

Desde linea de comandos se deberá ejecutar primero el archivo tables.py ingresando
	
	Python tables.py

De esta forma nos aseguramos la existencia de las tablas previamente

Una vez ejecutado tables.py, podemos ingresar el comando
	
	Python main.py

Para ejecutar el programa principal
