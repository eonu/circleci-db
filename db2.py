#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os
import subprocess
from typing import Optional

from testcontainers.core.generic import DbContainer
from testcontainers.core.waiting_utils import wait_for_logs


class Db2Container(DbContainer):
    TIMEOUT = 1_000

    def __init__(
        self,
        image: str = "ibmcom/db2:latest",
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        port: int = 50_000,
        **kwargs,
    ) -> None:
        super(Db2Container, self).__init__(image=image, **kwargs)
        self.username = username or os.environ.get("DB2_USER", "test")
        self.password = password or os.environ.get("DB2_PASSWORD", "test")
        self.database = database or os.environ.get("DB2_DATABASE", "test")
        self.port_to_expose = port
        self.with_exposed_ports(self.port_to_expose)

    def _configure(self) -> None:
        self.with_env("DB2INSTANCE", self.username)
        self.with_env("DB2INST1_PASSWORD", self.password)
        self.with_env("DBNAME", self.database)
        self.with_env("LICENSE", "accept")
        self.with_env("PERSISTENT_HOME", "false")
        self.with_env("ARCHIVE_LOGS", "false")  # reduces start-up time
        self.with_env("AUTOCONFIG", "false")  # reduces start-up time

    def get_connection_url(self, host=None) -> str:
        url = super()._create_connection_url(
            dialect="db2",
            username=self.username,
            password=self.password,
            db_name=self.database,
            host=host,
            port=self.port_to_expose,
        )
        print(f"URL: \033[31m{url}\033[0m")
        print(f"self.get_container_host_ip(): {self.get_container_host_ip()}")
        print(f"self.get_docker_client().host(): {self.get_docker_client().host()}")
        print(
            f"self.get_docker_client().gateway_ip(self._container.id): {self.get_docker_client().gateway_ip(self._container.id)}"
        )
        print(
            f"self.get_docker_client().bridge_ip(self._container.id): {self.get_docker_client().bridge_ip(self._container.id)}"
        )
        return url

    def _connect(self) -> None:
        wait_for_logs(self, "Setup has completed", self.TIMEOUT)
        super()._connect()


if __name__ == "__main__":
    import sqlalchemy

    with Db2Container(privileged=True, platform="linux/amd64") as db2:
        engine = sqlalchemy.create_engine(db2.get_connection_url())
        breakpoint()
        with engine.connect() as conn:
            query = sqlalchemy.text("SELECT SERVICE_LEVEL FROM SYSIBMADM.ENV_INST_INFO")
            breakpoint()
            result = conn.execute(query)
            version = result.scalar()
            breakpoint()
            pass
