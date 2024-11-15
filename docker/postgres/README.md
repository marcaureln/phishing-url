# Postgres

## Install extensions

We used a custom Dockerfile to be able to install extensions. To see how to do it, check the following [link](https://datacraze.io/postgresql-docker-image-adding-extensions/).

## Access Postgres container

To access the database, you can use the following command:

```bash
docker exec -it phishing-url-db psql -U postgres
```

**Note:** `phishing-url-db` is the name of the running container.
