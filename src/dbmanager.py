import pandas as pd
import psycopg2
import json
import datetime
import yfinance as yf
import os



class DbManager:
    
    def __init__(self, scheme = None, database = None):
        config = self._load_config()
        
        if scheme:
            config["scheme"] = scheme
        if database:
            config["database"] = database
        
        self.user = config["user"]
        self.password = config["password"]
        self.host = config["host"]
        self.port = config["port"]
        self.scheme = config["scheme"]
        # self.database = database or config["database"]
        self.dbname = config["database"]
        self.connection = None
        self.connection = self._connect()
        
        for key, value in config.items():
            print(f'{key}: {value}')

    def _load_config(self):
        config_path = os.path.expanduser('~/.creds/config_postgres.json')
        with open(config_path) as f:
            config = json.load(f)
        return config['postgres']

    def _connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Successful connection to PostgreSQL database")
            return True
        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL database:", error)
            assert error
            

    def add_df_to_postgresql(self, df, company: str = None):
        
        result = []
        
        self._connect()
        for index, df in df.iterrows():        
            """
                cada linea del df tendrá que lanzar la query de añadir dato
            """
            try:
                if isinstance(df["Date"], pd.Timestamp):
                    # df["Date"] = df["Date"].strftime("%Y-%m-%d")  # Convertir Timestamp a cadena
                    df["Date"] = df["Date"].to_pydatetime()
                    #print(df)
                    date = df["Date"]
                    #print(type(date))
                    # date = df["Date"].date()
                else:
                    date = datetime.datetime.strptime(df["Date"], "%Y-%m-%d")
                #print(date)
                if company == None:
                    company_str = df["company_code"]
                else:
                    company_str = company
                    
                values = [company_str, date, float(df["Open"]), float(df["High"]), float(df["Low"]), float(df["Close"]), float(df["Adj Close"]), int(df["Volume"])]
                
                self.add_individual_share(nombre_tabla="stock_data", valores=values)
                print('Data added correctly.')
                result.append(values)
                
            except Exception as e:
                print("Error ocurred: " + str(e))
                
        self._close_conexion()
        return result





    def add_individual_share(self, nombre_tabla: str = "stock_data", valores: list = []):
        """_summary_

        Args:
            nombre_tabla (_type_): 
                Nombre de la tabla:
                    - company, shares...
            valores (list): 
                Lista de valores a añadir:
                    - company_code: string
                    - date: datetime
                    - open: float
                    - High: float
                    - Low: flaot
                    - close: float
                    - Adj Close: float
                    - volume: integer
        """   
        
        try:
            valores, flag = self._check_data(valores)
            if flag:
                cursor = self.connection.cursor()
                
                valores = ', '.join([f"'{val}'" for val in valores])
                print(valores)
                consulta = f"INSERT INTO {self.scheme}.{nombre_tabla} VALUES ({valores});"
                cursor.execute(consulta)
                
                #self.connection.autocommit(True)
                self.connection.commit()
                print(f"Valores agregados a la tabla '{self.scheme}.{nombre_tabla}' exitosamente.")
                cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("Error al agregar valores:", error)
            self.connection.rollback() # Revert transaction in case of error


    def get_all_tickers(self):
        """_summary_
            get a list with all the tickers 
        Args:
            No Args
        """
        
        self._connect()
        cursor = self.connection.cursor()
        
        # consulta = f"SELECT COLUMN_NAME
        #             FROM INFORMATION_SCHEMA.COLUMNS
        #             WHERE TABLE_SCHEMA = '{self.esquema}'
        #             AND TABLE_NAME = '{table_name}';"
        
        consulta = f"""
            SELECT company_code
            FROM {self.scheme}.company
            """

        cursor.execute(consulta)
        
        columns = cursor.fetchall() #result será una lista con los datos de la query
        
        # Rearrenge format
        columns = [column[0] for column in columns]
        
        self.connection.commit()

        self._close_conexion()

        return columns 



    def _check_data(self, valores, table="stock_data"):
        if table == "stock_data":
            # Verificar que la lista de valores tenga el formato correcto
            if len(valores) != 8:
                print("Error: La lista 'valores' debe contener exactamente 7 elementos.")
                """
                Lista de valores a añadir:        
                    - company_code: string
                    - date: datetime
                    - open: float
                    - High: float
                    - Low: flaot
                    - close: float
                    - Adj Close: float
                    - volume: integer
                """
                return valores, False

            # Desempaquetar los valores de la lista
            company_code, date, open_val, high_val, low_val, close_val, adj_close, volume = valores

            # Verificar que los valores estén en el formato correcto
            if not isinstance(company_code, str):
                print("Error: 'company_code' debe ser una cadena de caracteres.")
                return valores, False
            
            if not isinstance(date, datetime.date):
                print("Error: 'date' debe ser un objeto de fecha.")
                if isinstance(date, datetime.datetime.timestamp):
                    date_str = valores["Date"].strftime("%Y-%m-%d")  # Convertir Timestamp a cadena
                    return date_str, True
                return valores, False
            
                
            if open_val is not None and not isinstance(open_val, (int, float)):
                print("Error: 'open_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if high_val is not None and not isinstance(high_val, (int, float)):
                print("Error: 'high_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if low_val is not None and not isinstance(low_val, (int, float)):
                print("Error: 'low_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if close_val is not None and not isinstance(close_val, (int, float)):
                print("Error: 'close_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if adj_close is not None and not isinstance(adj_close, (int, float)):
                print("Error: 'adj_close' debe ser un número entero o de punto flotante.")
                return valores, False
            if volume is not None and not isinstance(volume, int):
                print("Error: 'volume' debe ser un número entero.")
                return valores, False
            else:
                print("data in correct format")
                return valores, True
            
            
        elif table == "company":
            # Desempaquetar los valores de la lista
            company_code, company_name, market = valores

            # Verificar que los valores estén en el formato correcto
            if not isinstance(company_code, str):
                print("Error: 'company_code' debe ser una cadena de caracteres.")
                return valores, False
            if not isinstance(company_name, str):
                print("Error: 'company_name' debe ser una cadena de caracteres.")
                return valores, False
            if not isinstance(market, str):
                print("Error: 'market' debe ser una cadena de caracteres.")
                return valores, False
            else:
                print("data in correct format")
                return valores, True

    def _close_conexion(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada correctamente.")
