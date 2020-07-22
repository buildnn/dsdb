# Copyright (c) 2018-2020 Giacomo Barone, Buildnn Team. All Rights Reserved.
# MIT License

import os
import contextlib
import attr
import logging
from datetime import datetime
import warnings


logger = logging.getLogger("dsdb")


try:
    from sqlalchemy import create_engine
    from sqlalchemy.engine.url import URL
except ModuleNotFoundError:
    logger.debug("`sqlalchemy` not found. Skipping ")

try:
    import boto3
except ModuleNotFoundError:
    logger.debug("`boto3` not found. Skipping ")

try:
    from pymongo import MongoClient
except ModuleNotFoundError:
    logger.debug("`pymongo` not found. Skipping ")

try:
    from redis import Redis
except ModuleNotFoundError:
    logger.debug("`redis` not found. Skipping ")


def return_pwd(*args):
    return "pwd is hidden"


@attr.s
class DsDb(object):
    db = attr.ib(default=None)
    db_type = attr.ib(default=None)
    driver = attr.ib(default=None)
    endpoint = attr.ib(default=None)
    hide_parameters = attr.ib(default=True)
    host = attr.ib(default=None)
    port = attr.ib(default=None)
    pwd = attr.ib(default=None, repr=False)
    region = attr.ib(default=None)
    usr = attr.ib(default=None)
    query = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.db = self.db if self.db else os.getenv("DSDB_DB")
        self.db_type = self.db_type if self.db_type else os.getenv("DSDB_TYPE")
        self.driver = self.driver if self.driver else os.getenv("DSDB_DRIVER")
        self.endpoint = self.endpoint if self.endpoint else os.getenv("DSDB_ENDPOINT")
        self.host = self.host if self.host else os.getenv("DSDB_HOST")
        self.port = self.port if self.port else os.getenv("DSDB_PORT")
        self.region = self.region if self.region else os.getenv("DSDB_REGION")
        self.usr = self.usr if self.usr else os.getenv("DSDB_USER")
        self.query = self.query if self.query else os.getenv("DSDB_QUERY")

    def create_engine(self, pwd):

        if not self.port:
            if ":" in self.host:
                warnings.warn(
                    "the embedding of port in `DSDB_HOST` (eg. 'localhost:4532') will be "
                    "removed from 0.3 on. Use the `DSDB_PORT` parameter instead.",
                    DeprecationWarning,
                )
                host, port = self.host.split(":")
            else:
                host = self.host
                port = None
        else:
            host = self.host
            port = self.port

        self.engine = create_engine(
            URL(
                drivername=self.driver,
                username=self.usr,
                password=pwd,
                host=host,
                port=port,
                database=self.db,
                query=self.query,
            ),
            echo=False,
            hide_parameters=self.hide_parameters,
        )
        return self.engine

    def connect(self):

        pwd = self.pwd if self.pwd else os.getenv("DSDB_PASSWORD")

        if self.db_type == "dynamodb":
            self.client = boto3.resource(
                self.db_type, region_name=self.region, endpoint_url=self.endpoint
            )
            return self.client

        elif self.db_type == "mongodb":
            self.client = MongoClient(
                self.host, username=self.usr, password=pwd, authSource=self.db
            )
            return self.client

        elif self.db_type == "redis":
            self.client = Redis(
                host=self.host,
                port=int(self.port),
                username=self.usr,
                password=pwd,
                db=self.db,
            )
            return self.client

        else:
            engine = getattr(self, "engine", None)
            if not engine:
                self.create_engine(pwd)
            self.con = self.engine.connect()
            return self.con

    def close(self):
        if not self.db_type == "dynamodb":
            if hasattr(self, "con"):
                self.con.close()
            if hasattr(self, "client"):
                self.client.close()
        return self


@contextlib.contextmanager
def DsDbConnect(db=None, buf="print", hide_parameters=True):
    buf = print if buf == "print" else buf

    if not db:
        db = DsDb(hide_parameters=hide_parameters)

    if buf:
        buf("connecting to DSDB...")
    t0 = datetime.now()

    yield db.connect()
    db.close()

    if buf:
        buf(f"executed in {datetime.now() - t0}")
