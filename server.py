"""Basic webserver"""
import socket
import multiprocessing
import os

def decode(connection):
    """Decoding incoming data"""
    content = ''
    while True:
        data = connection.recv(1)
        if data:
            content += data.decode()
        else:
            break

        if content[-4:] == '\r\n\r\n':
            break
    return content

def handle(connection, client_address):
    """Handle incoming connections"""
    while True:
        print('servicing', client_address)

        content = decode(connection)
        path_line = content.split('\n')[0]
        path = path_line.split(' ')[1]
        filename = path.split('/')[-1]
        mime = 'text/html'
        body = ''

        # handle html
        if path.endswith('.html'):
            with open(filename) as file:
                body = file.read()
        # handle jpg
        elif path.endswith('.jpg'):
            mime = 'image/jpeg'
            with open(filename, 'rb') as file:
                body = file.read()
        #handle css
        elif path.endswith('.css'):
            mime = 'text/css'
            with open(filename) as file:
                body = file.read()
        # handle python
        elif path.endswith('.py'):
            body = os.popen('python3 %s' % filename).read()
        else:
            if filename != '':
                with open(filename) as file:
                    body = '<link rel="stylesheet" href="dark_theme.css">' + file.read()


        if body == '':
            body = '<link rel="stylesheet" href="dark_theme.css"><h1>404: File not found.</h2>'

        try:
            body = body.encode()
        except: #pylint: disable=W0702
            pass

        connection.send(b'HTTP/1.1 200 OK\r\n')
        connection.send('Content-Type: {0}\r\n'.format(mime).encode())
        connection.send('Content-Length: {0}\r\n'.format(len(body)).encode())
        connection.send(b'\r\n')
        connection.send(body)
        connection.send(b'\r\n\r\n')

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 8080))
    sock.listen(1)

    while True:
        conn, client_addr = sock.accept()
        print('accepted new connection')

        process = multiprocessing.Process(target=handle, args=(conn, client_addr))
        process.start()
