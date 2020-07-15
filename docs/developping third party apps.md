# Developping third party apps

## Authentication

Third party apps should authenticate using the OAuth2 server embeded in Udata.
The server supports the following grants:

- Authorization Code Grant
- PKCE Grant
- Password Grant
- Client Credentials Grant
- Refresh token Grant

The Implicit Grant in not supported as it is considered deprecated and insecure.

Udata uses [Authlib][] to implemented the OAuth2 server.

The prefered way to authenticate is using PKCE grant.

### Creating an OAuth client

In order to use the OAuth server, an OAuth client must be created, per app.
The client needs the email of a user to be its owner.

```shell
$ udata api create-oauth-client -u john@doe.com.
```

A client name can optionaly be passed to the command.
```shell
$ udata api create-oauth-client -u john@doe.com -n client-01
```

Redirect URIs can be specified, using once or several times the `--uri` argument.
If none is specified, the default `http://localhost:8080/login` will be used.
```shell
$ udata api create-oauth-client -u john@doe.com --uri 'http://localhost:8080/login' --uri 'http://localhost:8181/auth'
```

The command returns the client's information needed by the app.
```shell
New OAuth client: client-01
Client's ID 5f0c5af8cd5e5189d4dc6888
Client's secret rm0Ow8NI751UBzFYCff5YZcVTCEZoU4ALCwuv0BDTH2UD442eC
Client's URI ['http://localhost:8080/login', 'http://localhost:8181/auth']
```

[Authlib]: https://docs.authlib.org/en/latest/index.html
