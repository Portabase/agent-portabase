<br />
<div align="center">
  <a href="https://portabase.io">
    <img src="https://portabase.io/static/logo/logo.svg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Portabase Agent</h3>
  <p>
    Free, open-source, and self-hosted solution for automated backup and restoration of your database instances.
  </p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/solucetechnologies/agent-portabase?color=brightgreen)](https://hub.docker.com/r/solucetechnologies/agent-portabase)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)](https://github.com/Portabase/portabase)

[![PostgreSQL](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-003545?logo=mariadb&logoColor=white)](https://mariadb.org/)
[![Self Hosted](https://img.shields.io/badge/self--hosted-yes-brightgreen)](https://github.com/Portabase/portabase)
[![Open Source](https://img.shields.io/badge/open%20source-❤️-red)](https://github.com/Portabase/portabase)

  <p>
    <strong>
        <a href="https://portabase.io">Documentation</a> •
        <a href="https://www.youtube.com/watch?v=hvLbX5LN1UE">Demo</a> •
        <a href="#installation">Installation</a> •
        <a href="https://github.com/Portabase/agent-portabase/issues/new?labels=bug&template=bug-report---.md">Report Bug</a> •
        <a href="https://github.com/Portabase/agent-portabase/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
    </strong>
  </p>


</div>

---

## ✨ About The Project

Portabase Agent is the agent service use with Portabase Server. This service is for backup/restore db instances.
<a href="https://github.com/Portabase/portabase">Portabase Server</a>

### Built With

* [![Python][Python]][Python-url]
* [![Redis][Redis]][Redis-url]
* [![Celery][Celery]][Celery-url]
* [![Docker][Docker]][Docker-url]

---

## 🚀 Getting Started

### Installation

You have 3 ways to install **Portabase Agent**:

- Automated CLI (recommended) - [details](https://portabase.io/docs/cli)
- Docker Compose setup - [details](https://portabase.io/docs/agent/setup)
- Kubernetes with Helm (soon)

Ensure Docker is installed on your machine before getting started.

### Docker Compose Setup

Create a `docker-compose.yml` file with the following configuration:

```yaml
name: agent-portabase

services:
  app:
    container_name: agent-portabase
    restart: always
    image: solucetechnologies/agent-portabase:latest
    volumes:
      # Mount the DB config file
      - ./databases.json:/app/src/data/config/config.json
      # - ./databases.toml:/app/src/data/config/config.toml
    environment:
      TZ: "Europe/Paris"
      # DATABASES_CONFIG_FILE: "config.toml" if you use .toml config file. By default, it's "config.json"
      EDGE_KEY: "<Get your edge key from your dashboard>"
    networks:
      - portabase

  db:
    image: postgres:17-alpine
    networks:
      - portabase
      - default
    ports:
      - "5430:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=<your_database>
      - POSTGRES_USER=<database_user>
      - POSTGRES_PASSWORD=<database_password>

volumes:
  postgres-data:

networks:
  portabase:
    name: portabase_network
    external: true
```

Then run:

```bash
docker compose up -d
```

### Locally (Development)

1. Clone the repository
   ```sh
   git clone https://github.com/Portabase/agent-portabase
   ```
3. Start the project
   ```sh
   docker compose up 
   ```

---

## 🔑 Config File

You can configure your database connections by adding a **config file**. The software supports both **JSON** and **TOML
** formats, so you can choose the format that best fits your workflow.

Multiple databases can be connected through the same agent, which is useful for managing development, staging, and
production environments.

### JSON Example

Create a `database.json` file with your database information:

```json
{
  "databases": [
    {
      "name": "Test database 1",
      "database": "devdb",
      "type": "postgresql",
      "username": "devuser",
      "password": "changeme",
      "port": 5432,
      "host": "localhost",
      "generatedId": "16678159-ff7e-4c97-8c83-0adeff214681"
    },
    {
      "name": "Test database 2",
      "database": "mariadb",
      "type": "mysql",
      "username": "mariadb",
      "password": "changeme",
      "port": 3306,
      "host": "localhost",
      "generatedId": "16678124-ff7e-4c97-8c83-0adeff214681"
    }
  ]
}
```

### TOML Example

Create a `database.json` file with your database information:

```toml
[[databases]]
name = "Test database 1"
database = "devdb"
type = "postgresql"
username = "devuser"
password = "changeme"
port = 5432
host = "localhost"
generatedId = "16678159-ff7e-4c97-8c83-0adeff214681"

[[databases]]
name = "Test database 1"
database = "mariadb"
type = "mysql"
username = "mariadb"
password = "changeme"
port = 3306
host = "localhost"
generatedId = "16678124-ff7e-4c97-8c83-0adeff214681"
```

✅ Both JSON and TOML formats are fully supported.

For `generatedId`, you will need to generate it yourself using the [UUID V4 format](https://www.uuidgenerator.net/)

## 📦 Database Seed (development)

Using Docker

### For postgres

```bash
docker exec -i -e PGPASSWORD=<password> <container_name> psql -U <USER> -d <DATABASE> < ./scripts/seed.sql
```

### For mysql

Install the client cli before

```bash
mysql -h 127.0.0.1 -P <port> -u <username> -p<password> <database_name> < ./scripts/seed-mysql.sql
```

--- 

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how to get started:

1. Fork the repository
2. Create a new branch:
    ```bash
    git checkout -b features/your-feature
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add YourFeature"
    ```
4. Push to the branch:
    ```bash
    git push origin features/your-feature
    ```
5. Open a pull request

### Top contributors:

<a href="https://github.com/Portabase/agent-portabase/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Portabase/agent-portabase" alt="contrib.rocks image" />
</a>

## 📄 License

Distributed under the Apache License. See `LICENSE.txt` for more information.

---

## 🙏 Acknowledgments

Thanks to all contributors and the open-source community!

Give the project a ⭐ if you like it!


[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

[Docker]: https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge

[Celery]: https://img.shields.io/static/v1?style=for-the-badge&message=Celery&color=37814A&logo=Celery&logoColor=FFFFFF&label

[Redis]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white

[Python-url]: https://www.python.org/

[Redis-url]: https://redis.io/

[Docker-url]: https://www.docker.com/

[Celery-url]: https://docs.celeryq.dev/en/stable/