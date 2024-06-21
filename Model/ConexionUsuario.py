import mariadb as sql

class ConexionUsuario():
    """
    Representa una conexión a una base de datos utilizando MariaDB.

    Attributes:
        __host (str): Dirección del servidor de base de datos.
        __user (str): Nombre de usuario para acceder a la base de datos.
        __password (str): Contraseña del usuario para acceder a la base de datos.
        __database (str): Nombre de la base de datos a la que se conecta.
        __port (int): Puerto de conexión a la base de datos.
        __conexion: Objeto de conexión a la base de datos.

    """
    
    def __init__(self):
        """
        Constructor de la clase ConexionUsuario. Inicializa los parámetros de conexión con valores predeterminados.
        """
        self.__host = "localhost"
        self.__user = "root"
        self.__password = ""
        self.__database = "juego"
        self.__port = 3306
        self.__conexion = None

    def crearConexion(self):
        """
        Crea una conexión a la base de datos utilizando los atributos de conexión establecidos (host, usuario, contraseña, base de datos y puerto).
        """
        self.__conexion = sql.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__database,
            port=self.__port)

    def cerrarConexion(self):
        """
        Cierra la conexión actual a la base de datos.
        """
        if self.__conexion:
            self.__conexion.close()

    def getHost(self):
        """
        Retorna la dirección del servidor de base de datos.

        Returns:
            str: Dirección del servidor de base de datos.
        """
        return self.__host

    def getUser(self):
        """
        Retorna el nombre de usuario para acceder a la base de datos.

        Returns:
            str: Nombre de usuario para acceder a la base de datos.
        """
        return self.__user

    def getPassword(self):
        """
        Retorna la contraseña del usuario para acceder a la base de datos.

        Returns:
            str: Contraseña del usuario para acceder a la base de datos.
        """
        return self.__password

    def getDatabase(self):
        """
        Retorna el nombre de la base de datos a la que se conecta.

        Returns:
            str: Nombre de la base de datos a la que se conecta.
        """
        return self.__database

    def getPort(self):
        """
        Retorna el puerto de conexión a la base de datos.

        Returns:
            int: Puerto de conexión a la base de datos.
        """
        return self.__port

    def getConexion(self):
        """
        Retorna el objeto de conexión a la base de datos.

        Returns:
            mariadb.connection: Objeto de conexión a la base de datos.
        """
        return self.__conexion

    def setHost(self, host):
        """
        Establece la dirección del servidor de base de datos.

        Args:
            host (str): Dirección del servidor de base de datos.
        """
        self.__host = host

    def setUser(self, user):
        """
        Establece el nombre de usuario para acceder a la base de datos.

        Args:
            user (str): Nombre de usuario para acceder a la base de datos.
        """
        self.__user = user

    def setPassword(self, password):
        """
        Establece la contraseña del usuario para acceder a la base de datos.

        Args:
            password (str): Contraseña del usuario para acceder a la base de datos.
        """
        self.__password = password

    def setDatabase(self, database):
        """
        Establece el nombre de la base de datos a la que se conectará.

        Args:
            database (str): Nombre de la base de datos a la que se conectará.
        """
        self.__database = database

    def setPort(self, port):
        """
        Establece el puerto de conexión a la base de datos.

        Args:
            port (int): Puerto de conexión a la base de datos.
        """
        self.__port = port

    def setConexion(self, conexion):
        """
        Establece el objeto de conexión a la base de datos.

        Args:
            conexion (mariadb.connection): Objeto de conexión a la base de datos.
        """
        self.__conexion = conexion
