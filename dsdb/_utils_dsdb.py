# Copyright (c) 2018-2020 Giacomo Barone, Buildnn Team. All Rights Reserved.
# MIT License

import os
import contextlib
from datetime import datetime
import attr
from sqlalchemy import create_engine
import logging
logger = logging.getLogger("dsdb")
try:
    import boto3
except ModuleNotFoundError:
    logger.debug("`boto3` not found. Skipping ")
try:
    from pymongo import MongoClient
except ModuleNotFoundError:
    logger.debug("`pymongo` not found. Skipping ")


def return_pwd(*args):
    return "pwd is hidden"


@attr.s
class DsDb(object):
    usr = attr.ib(default=None)
    db = attr.ib(default=None)
    host = attr.ib(default=None)
    driver = attr.ib(default=None)
    hide_parameters = attr.ib(default=True)
    pwd = attr.ib(default=None, repr=False)
    endpoint = attr.ib(default=None)
    region = attr.ib(default=None)
    db_type = attr.ib(default=None)

    def create_engine(self):

        usr = self.usr if self.usr else os.getenv("DSDB_USER")
        db = self.db if self.db else os.getenv("DSDB_DB")
        host = self.host if self.host else os.getenv("DSDB_HOST")
        driver = self.driver if self.driver else os.getenv("DSDB_DRIVER")
        pwd = self.pwd if self.pwd else os.getenv("DSDB_PASSWORD")

        self.engine = create_engine(
            "{}://{}:{}@{}/{}".format(driver, usr, pwd, host, db,),
            echo=False,
            hide_parameters=self.hide_parameters,
        )
        return self.engine

    def connect(self):
        endpoint = self.endpoint if self.endpoint else os.getenv("DSDB_ENDPOINT")
        region = self.region if self.region else os.getenv("DSDB_REGION")
        db_type = self.db_type if self.db_type else os.getenv("DSDB_TYPE")
        host = self.host if self.host else os.getenv("DSDB_HOST")

        if type == "dynamodb":
            self.client = boto3.resource(
                db_type, region_name=region, endpoint_url=endpoint
            )
            return self.client
        elif type == "mongodb":
            self.client = MongoClient(host)
            return self.client
        else:
            engine = getattr(self, "engine", None)
            if not engine:
                self.create_engine()
            self.con = self.engine.connect()
            return self.con

    def close(self):
        if not type == "dynamodb":
            if hasattr(self, "con"):
                self.con.close()
            if hasattr(self, "client"):
                self.client.close()
        return self


@contextlib.contextmanager
def DsDbConnect(db=DsDb(), buf=print, hide_parameters=True):
    if not db:
        db = DsDb(hide_parameters=hide_parameters)
    buf("connecting to DSDB...")
    t0 = datetime.now()
    yield db.connect()
    db.close()
    buf(f"executed in {datetime.now() - t0}")
