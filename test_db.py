import pytest
from pytest_lazyfixture import lazy_fixture
import sqlalchemy

from db2 import Db2Container
from testcontainers.mssql import SqlServerContainer


@pytest.fixture(scope="module")
def db2_engine():
    # platform="linux/amd64"
    with Db2Container("ibmcom/db2:11.5.7.0", privileged=True) as db2:
        engine = sqlalchemy.create_engine(db2.get_connection_url())
        yield engine
        engine.dispose()


@pytest.fixture(scope="module")
def mssql_engine():
    # platform="linux/amd64"
    with SqlServerContainer("mcr.microsoft.com/mssql/server:2017-latest") as mssql:
        engine = sqlalchemy.create_engine(mssql.get_connection_url())
        yield engine
        engine.dispose()


engine_fixtures = [lazy_fixture("db2_engine")]


# @pytest.mark.parametrize("engine", engine_fixtures)
# def test_db2(engine):
#     with engine.connect() as conn:
#         query = sqlalchemy.text("SELECT SERVICE_LEVEL FROM SYSIBMADM.ENV_INST_INFO")
#         result = conn.execute(query)
#         version = result.scalar()
#     assert version == "DB2 v11.5.7.0"


@pytest.mark.parametrize("engine", [lazy_fixture("mssql_engine")])
def test_mssql(engine):
    with engine.connect() as conn:
        pass
