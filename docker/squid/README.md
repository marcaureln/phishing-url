# Squid Proxy

## Securing Squid

To make your Squid proxy more secure, you can add basic authentication. To do so, you need to install `apache2-utils`:

```bash
sudo apt-get update
sudo apt-get install apache2-utils
```

After installing `apache2-utils`, you can create a password file:

```bash
htpasswd -c /path/to/squid/passwords your_username
```

Add the following lines to your Squid configuration file:

```conf
# squid.conf
auth_param basic program /usr/lib/squid3/basic_ncsa_auth /etc/squid/passwords
auth_param basic realm proxy
acl authenticated proxy_auth REQUIRED

http_access allow authenticated
```

Make sure to mount the `passwords` file to the container:

```yaml
# compose.yml
services:
  proxy:
    volumes:
      - ./squid/passwords:/etc/squid/passwords:ro
```
