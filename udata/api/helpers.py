from flask import request as flask_req
from flask import Response, json
from authlib.common.encoding import to_unicode

### source : https://ns1.ibsinternet.com/powerdns-admin/flask/lib/python3.4/site-packages/authlib/flask/oauth2/authorization_server.py

def create_oauth_request(request, request_cls):
    print(f'\n>>> create_oauth_request > request : {request}')
    print(f'>>> create_oauth_request > request_cls : {request_cls}')
    print(f'>>> create_oauth_request > request A : \n{request.__dict__}')

    if isinstance(request, request_cls):
        print(f'>>> create_oauth_request > isinstance == true ')
        return request

    if not request:
        request = flask_req

    print(f'>>> create_oauth_request > request B : \n{request.__dict__}')
    if request.method == 'POST':
        if request.form:
            body = request.form.to_dict(flat=True)
        else:
            body = request.get_json()
    else:
        body = None

    # query string in werkzeug Request.url is very weird
    # scope=profile%20email will be scope=profile email
    url = request.base_url
    if request.query_string:
        url = url + '?' + to_unicode(request.query_string)
    requestOauth = request_cls(request.method, url, body, request.headers)
    print(f'>>> create_oauth_request > requestOauth : \n{requestOauth.__dict__}')

    return requestOauth


def handle_response(status_code, payload, headers):
    if isinstance(payload, dict):
        payload = json.dumps(payload)
    return Response(payload, status=status_code, headers=headers)
