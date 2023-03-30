import os
import pytest
from pytest_lazyfixture import lazy_fixture
import sqlalchemy

from db2 import Db2Container
from testcontainers.mssql import SqlServerContainer


@pytest.fixture(scope="module")
def db2_engine():
    container = Db2Container(
        "ibmcom/db2:latest",
        platform="linux/amd64",
        privileged=True,
    ).with_volume_mapping(
        os.environ["DOCKER_HOST"], os.environ["DOCKER_HOST"], mode="rw"
    )
    with container as db2:
        engine = sqlalchemy.create_engine(db2.get_connection_url())
        yield engine
        engine.dispose()


@pytest.fixture(scope="module")
def mssql_engine():
    container = SqlServerContainer(
        "mcr.microsoft.com/mssql/server:2017-latest",
        platform="linux/amd64",
    ).with_volume_mapping(
        os.environ["DOCKER_HOST"], os.environ["DOCKER_HOST"], mode="rw"
    )
    with container as mssql:
        engine = sqlalchemy.create_engine(mssql.get_connection_url())
        yield engine
        engine.dispose()


@pytest.mark.parametrize("engine", [lazy_fixture("db2_engine")])
def test_db2(engine):
    with engine.connect() as conn:
        query = sqlalchemy.text("SELECT SERVICE_LEVEL FROM SYSIBMADM.ENV_INST_INFO")
        result = conn.execute(query)
        version = result.scalar()
    assert version == "DB2 v11.5.8.0"


# @pytest.mark.parametrize("engine", [lazy_fixture("mssql_engine")])
# def test_mssql(engine):
#     with engine.connect() as conn:
#         pass
