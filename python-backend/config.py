import os
import oracledb

class OracleConfig:
    def __init__(self, username = "", password = ""):
        self.username = username
        self.password = password
        self.hostname = "oracle.cise.ufl.edu"
        self.port = 1521
        self.sid = "orcl"
        self.oracle_home = os.environ.get("ORACLE_HOME")
        self.config_dir = "."
        self.init_oracle_client()
        self.makedsn()

    def init_oracle_client(self):
        oracledb.init_oracle_client(lib_dir=self.oracle_home, config_dir=self.config_dir)

    def makedsn(self):
        return oracledb.makedsn(self.hostname, self.port, sid=self.sid)
