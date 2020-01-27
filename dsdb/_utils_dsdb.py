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
    usr = attr.ib(default=os.getenv("DSDB_USER"), init=False)
    pwd = attr.ib(default=os.getenv("DSDB_PASSWORD"), init=False, repr=False)
    db = attr.ib(default=os.getenv("DSDB_DB"), init=False)
    host = attr.ib(default=os.getenv("DSDB_HOST"), init=False)
    driver = attr.ib(default=os.getenv("DSDB_DRIVER"), init=False)

    def create_engine(self):
        self.engine = create_engine(
            '{}://{}:{}@{}/{}'.format(
                self.driver,
                self.usr,
                self.pwd,
                self.host,
                self.db,
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
