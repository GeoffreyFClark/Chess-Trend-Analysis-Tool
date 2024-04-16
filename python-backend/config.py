import os
import oracledb

class OracleConfig:
    def __init__(self):
        self.username = os.environ.get("DB_USERNAME")
        self.password = os.environ.get("DB_PASSWORD")
        self.hostname = os.environ.get("DB_HOSTNAME")
        self.port = os.environ.get("DB_PORT")
        self.sid = os.environ.get("DB_SID")
        self.oracle_home = os.environ.get("ORACLE_HOME")

        oracledb.init_oracle_client(lib_dir=self.oracle_home)
        self.dsn = oracledb.makedsn(self.hostname, self.port, sid=self.sid)
        
    @property
    def connection_string(self):
        return self.dsn
            
