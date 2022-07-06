import json
import cx_Oracle
from wattpad.logger.baselogger import BaseLogger

class DBConfig:
    def __init__(self) -> None:
        self.file_prefix="wattpad.utils.db"
        self.logger= BaseLogger().loggger_init()

    def load_db_config(self):
        try:
            self.logger.info("%s.load_db_config method invoked", self.file_prefix)

            with open("dbconfig.json") as f:
                db=json.load(f)

            connection_string=f"{db['Username']}/{db['Password']}@{db['DSN']}"

            return connection_string
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.load_db_config method", self.file_prefix, exc_info=1)
            raise e
                

    def load_client_path(self):
        try:
            self.logger.info("%s. method invoked")

            with open("dbconfig.json") as f:
                db=json.load(f)

            client_path=f"{db['ClientPath']}"

            return client_path
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s. method",exc_info=1)
            raise e


    def initialize_oracle_client_path(self):
        try:
            self.logger.info("%s.initialize_oracle_client_path method invoked", self.file_prefix)

            path=self.load_client_path()
            cx_Oracle.init_oracle_client(lib_dir=path)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.initialize_oracle_client_path method", self.file_prefix ,exc_info=1)
            raise e
        


    