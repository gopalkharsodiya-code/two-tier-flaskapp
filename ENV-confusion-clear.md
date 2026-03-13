# MySQL + Flask (Docker) Environment Variables Explained

------

~~~md
This document explains **why environment variables differ between the MySQL container and the Flask backend container**, how they interact, and how to access the database.

---

## Overview

This project uses a **two-container architecture**:

- **MySQL container** → Responsible for **database initialization**
- **Flask container** → Responsible for **connecting to the database**

Both containers communicate over a shared Docker network.

---

## Docker Commands Used

### MySQL Container

```bash
docker run -d \
  --name mysql \
  --network=twotier \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_DATABASE=mydb \
  -e MYSQL_ROOT_PASSWORD=admin \
  -p 3306:3306 \
  mysql:5.7
~~~

### Flask Backend Container

```bash
docker run -d \
  --name flaskapp \
  --network=twotier \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=admin \
  -e MYSQL_DB=mydb \
  -p 5000:5000 \
  flaskapp:latest
```

------

## Why Environment Variables Are Different

Even though the variable names look similar, they serve **different purposes**.

### Key Rule

> **MySQL container variables initialize the database**
> **Backend container variables connect to the database**

------

## MySQL Container Environment Variables

These variables are **only used once**, when the container starts for the first time.

| Variable              | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| `MYSQL_ROOT_PASSWORD` | Sets the password for the existing `root` MySQL user |
| `MYSQL_DATABASE`      | Creates a database with this name                    |

### Important Notes

- The `root` user already exists in MySQL
- `MYSQL_ROOT_PASSWORD` does **not create** the root user — it only sets its password
- These variables are ignored on subsequent runs if a volume already exists

------

## Flask Backend Environment Variables

These variables are used by the **application code**, not by MySQL.

| Variable         | Purpose                           |
| ---------------- | --------------------------------- |
| `MYSQL_HOST`     | Address of the MySQL server       |
| `MYSQL_USER`     | MySQL username to authenticate as |
| `MYSQL_PASSWORD` | Password for that user            |
| `MYSQL_DB`       | Database name to connect to       |

### Why `MYSQL_HOST=mysql` Works

- Both containers are attached to the same Docker network
- Docker provides internal DNS
- The container name (`mysql`) resolves automatically to the MySQL container

> `localhost` must NOT be used between containers

------

## Why `MYSQL_DATABASE` vs `MYSQL_DB`?

These names are **not standardized**.

### `MYSQL_DATABASE` (MySQL container)

- Required by the **official MySQL Docker image**
- Used only to **create a database**

### `MYSQL_DB` (Flask container)

- Arbitrary variable name
- Used only by the backend application code
- Could be renamed as long as the code matches

They represent the **same database**, but are used at **different stages**.

------

## Conceptual Mapping

| Concept                 | Variable         |
| ----------------------- | ---------------- |
| Database server address | `MYSQL_HOST`     |
| Login username          | `MYSQL_USER`     |
| Login password          | `MYSQL_PASSWORD` |
| Database created        | `MYSQL_DATABASE` |
| Database connected to   | `MYSQL_DB`       |

------

## How to Access the MySQL Database

### From the MySQL Container

```bash
docker exec -it mysql mysql -u root -p
```

Password:

```text
admin
```

Useful commands:

```sql
SHOW DATABASES;
USE mydb;
SHOW TABLES;
```

------

### From the Host Machine

Because port `3306` is exposed:

```bash
mysql -h 127.0.0.1 -P 3306 -u root -p
```

------

## Docker Volume Behavior (Important)

```bash
-v mysql-data:/var/lib/mysql
```

Once the volume exists:

- MySQL will NOT re-run initialization
- Env vars like `MYSQL_DATABASE` are ignored

To reset everything:

```bash
docker rm -f mysql
docker volume rm mysql-data
```

------

## Best Practice (Recommended)

Avoid using the `root` user in applications.

### MySQL Container

```bash
-e MYSQL_DATABASE=mydb
-e MYSQL_USER=appuser
-e MYSQL_PASSWORD=apppass
-e MYSQL_ROOT_PASSWORD=admin
```

### Flask Container

```bash
-e MYSQL_HOST=mysql
-e MYSQL_USER=appuser
-e MYSQL_PASSWORD=apppass
-e MYSQL_DB=mydb
```

------

## Summary

- `MYSQL_HOST` is the **database server**, not a user
- `MYSQL_ROOT_PASSWORD` sets the root password
- Backend env vars do **not configure MySQL**
- Similar names ≠ shared meaning
- Initialization and connection are separate concerns

------

## One-Line Rule to Remember

> **Database container sets up MySQL**
> **Backend container connects to MySQL**


## Mentions

This is repo is clone of this https://github.com/LondheShubham153/two-tier-flask-app
I have created this seperate for my pesonal understanding, while removing thing which are not relevant for me now
