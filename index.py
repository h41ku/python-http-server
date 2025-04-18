import asyncio, re, ssl, binascii, hashlib

html = """<!doctype html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>Python HTTP Server</title>
</head>
<body>
    <h1>%s</h1>
</body>
</html>
"""

listen_host = '127.0.0.1'
listen_port = 3080
charset = 'utf-8'
ssl_certificate = None # 'server.crt.pem'
ssl_key = None # 'server.key.pem'
ssl_password = None
ssl_ca_certificate = None

ascii = 'ascii'
request_pattern = re.compile('^([A-Z]+)\s+(\S+)\s+HTTP/1.1\r?\n$', re.IGNORECASE)
header_pattern = re.compile('^([A-Z0-9\-]+)\s*:\s*([^\r\n]+)\r?\n$', re.IGNORECASE)
path_pattern = re.compile('^([^?]+)(?:\?([^#]*))?(?:#(.*))?$')

async def close_writer(writer, drain = True):
    if drain:
        print("Draining...")
        await writer.drain()
    print("Closing...")
    writer.close()
    print("Waiting while closing...")
    await writer.wait_closed()
    print("Done")

async def http_error(writer, status, status_text):
    print("Responding with error:", status)
    writer.write(b'HTTP/1.0 %d %s\r\n' % (status, bytes(status_text, ascii)))
    writer.write(b'\r\n')
    await close_writer(writer)

async def serve_client(reader, writer):
    request_line = await reader.readline()
    print("Request:", request_line)
    if request_line == b'':
        return await close_writer(writer, False)
    match = request_pattern.match(str(request_line, ascii))
    if not match:
        print("Request is not match with pattern!")
        return await http_error(writer, 405, 'Bad Request')
    method = match.group(1).lower()
    originalUrl = match.group(2)
    print("method:", method)
    print("originalUrl:", originalUrl)
    match = path_pattern.match(originalUrl)
    if match:
        url = match.group(1)
        query = match.group(2)
        print("url:", url)
        print("query:", query)
    if url != '/':
        return await http_error(writer, 404, 'Not Found')
    headers = {}
    while reader.feed_eof() or not reader.at_eof():
        header_line = await reader.readline()
        print("Header:", header_line)
        if header_line == b'':
            print("Oops!")
            return await close_writer(writer, False)
        if header_line in (b'\n', b'\r\n'):
            print('End of header')
            break
        match = header_pattern.match(str(header_line, ascii))
        #if not match:
        #    return await http_error(writer, 405, 'Bad Request')
        if match:
            key = match.group(1).lower()
            value = match.group(2)
            #print("Key:", key)
            #print("Value:", value)
            if key in headers:
                previous = headers[key]
                if not type(previous) is list:
                    headers[key] = [ previous ]
                headers[key].append(value)
            else:
                headers[key] = value
        pass
    print(headers)
    message = 'Привет, Py!'
    response = bytes(html % (message), charset)
    print("Length:", len(response))
    print("Response:", response)
    writer.write(b'HTTP/1.0 200 OK\r\n')
    writer.write(b'Content-Type: text/html; charset="%s"\r\n' % (bytes(charset, ascii)))
    writer.write(b'Content-Length: %d\r\n' % (len(response)))
    writer.write(b'Connection: close\r\n')
    writer.write(b'ETag: "%s"\r\n' % (binascii.hexlify(hashlib.sha256(response).digest())))
    writer.write(b'\r\n')
    writer.write(response)
    await close_writer(writer)

async def main():
    if ssl_certificate and ssl_key:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(ssl_certificate, ssl_key, ssl_password)
        if ssl_ca_certificate:
            ssl_context.load_verify_locations(ssl_ca_certificate)
    else:
        ssl_context = None
    asyncio.create_task( \
        asyncio.start_server( \
            serve_client, \
            listen_host, \
            listen_port, \
            ssl = ssl_context, \
            reuse_address = True, \
            reuse_port = True \
        ) \
    )
    print('Listen: %s://%s%s/' % ( \
        'https' if ssl_context else 'http', \
        listen_host, \
        '' if listen_port in (80, 443) else ':%d' % (listen_port) \
    ))
    while True:
        #print('Waiting for connections...')
        await asyncio.sleep(3.0)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
