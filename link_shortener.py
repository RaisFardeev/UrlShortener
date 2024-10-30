import hashlib
import random
import string
from urllib.parse import quote


storage = {}


def generate_short_id(url):
    base_hash = hashlib.sha256(url.encode()).hexdigest()[:5]
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    return base_hash + random_part


def parse_multipart(data, boundary):
    parts = data.split(boundary.encode())
    parsed_data = {}
    for part in parts:
        if not part.strip() or part == b"--":
            continue
        try:
            headers, content = part.split(b"\r\n\r\n", 1)
            content = content.strip(b'\r\n--')

            if b'Content-Disposition' in headers:
                name = headers.split(b'name="')[1].split(b'"')[0].decode()
                parsed_data[name] = content.decode("utf-8").strip()
        except ValueError:
            continue
    return parsed_data


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    path = scope['path']
    method = scope['method']

    if method == 'POST' and path == '/shorten':
        headers = dict(scope['headers'])
        content_type = headers.get(b'content-type', b'').decode()

        if "multipart/form-data" in content_type:
            boundary = content_type.split("boundary=")[-1]
            body = await receive()
            body_data = body.get("body", b"")

            form_data = parse_multipart(body_data, boundary)
            url = form_data.get("url")

            if url:
                short_id = generate_short_id(url)
                storage[short_id] = url

                response = f"Shortened URL: http://localhost:8000/{short_id}"
                await send({
                    'type': 'http.response.start',
                    'status': 200,
                    'headers': [(b'content-type', b'text/plain')]
                })
                await send({
                    'type': 'http.response.body',
                    'body': response.encode('utf-8')
                })
            else:
                await send({
                    'type': 'http.response.start',
                    'status': 400,
                    'headers': [(b'content-type', b'text/plain')]
                })
                await send({
                    'type': 'http.response.body',
                    'body': b"URL parameter missing"
                })
        else:
            await send({
                'type': 'http.response.start',
                'status': 415,
                'headers': [(b'content-type', b'text/plain')]
            })
            await send({
                'type': 'http.response.body',
                'body': b"Unsupported Media Type"
            })

    elif method == 'GET' and path.startswith("/"):
        short_id = path.lstrip('/')

        if short_id in storage:
            original_url = storage[short_id].strip()
            encoded_url = quote(original_url, safe=':/')
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'location', encoded_url.encode('utf-8'))]
            })
            await send({
                'type': 'http.response.body',
                'body': b''
            })
        else:
            await send({
                'type': 'http.response.start',
                'status': 404,
                'headers': [(b'content-type', b'text/plain')]
            })
            await send({
                'type': 'http.response.body',
                'body': b"URL not found"
            })
    else:
        await send({
            'type': 'http.response.start',
            'status': 405,
            'headers': [(b'content-type', b'text/plain')]
        })
        await send({
            'type': 'http.response.body',
            'body': b"Method not allowed"
        })