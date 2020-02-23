# Copyright (c) 2018-2020 Giacomo Barone, Buildnn Team. All Rights Reserved.
# MIT License

import os
import contextlib
from datetime import datetime
import attr
from sqlalchemy import create_engine

def return_pwd(*args):
    return "pwd is hidden"

@attr.s
class DsDb(object):
    usr = attr.ib(default=None)
    db = attr.ib(default=None)
    host = attr.ib(default=None)
    driver = attr.ib(default=None)
    pwd = attr.ib(default=None, repr=False)

    def create_engine(self):

        usr = self.usr if self.usr else os.getenv("DSDB_USER")
        db = self.db if self.db else os.getenv("DSDB_DB")
        host = self.host if self.host else os.getenv("DSDB_HOST")
        driver = self.driver if self.driver else os.getenv("DSDB_DRIVER")
        pwd = self.pwd if self.pwd else os.getenv("DSDB_PASSWORD")

        self.engine = create_engine(
            '{}://{}:{}@{}/{}'.format(
                driver,
                usr,
                pwd,
                host,
                db,
            ), echo=False)
        return self.engine

    def connect(self):
        engine = getattr(self, "engine", None)
        if not engine:
            self.create_engine()
        self.con = self.engine.connect()
        return self.con

    def close(self):
        self.con.close()
        return self

@contextlib.contextmanager
def DsDbConnect(db=DsDb(), buf=print):
    buf("connecting to DSDB...")
    t0 = datetime.now()
    yield db.connect()
    db.close()
    buf(f"executed in {datetime.now()-t0}")
