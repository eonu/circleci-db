import sqlalchemy
from testcontainers.mssql import SqlServerContainer

if __name__ == "__main__":
    with SqlServerContainer("mcr.microsoft.com/mssql/server:2017-latest") as container:
        engine = sqlalchemy.create_engine(container.get_connection_url())
        with engine.connect() as conn:
            breakpoint()
            pass
