import os
import random
import threading

from requests import *
from colorama import *

class checker:
    available = 0
    taken     = 0
    def __init__(self) -> None:
        self.session = Session()

    def csrf(self) -> str:
        with self.session as session:
            response = session.post('https://auth.roblox.com/')
            if 'X-CSRF-TOKEN' in response.headers:
                session.headers['X-CSRF-TOKEN'] = response.headers['X-CSRF-TOKEN']
                xcsrf = session.headers['X-CSRF-TOKEN']
                return xcsrf
            else:
                raise 'Unable to fetch CSRF token'

    def sendRequest(self) -> None:
        with self.session as session:
            headers = {
                'authority'         : 'auth.roblox.com',
                'accept'            : 'application/json, text/plain, */*',
                'accept-language'   : 'en-GB,en;q=0.9',
                'content-type'      : 'application/json;charset=UTF-8',
                'origin'            : 'https://www.roblox.com',
                'referer'           : 'https://www.roblox.com',
                'sec-ch-ua'         : '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                'sec-ch-ua-mobile'  : '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest'    : 'empty',
                'sec-fetch-mode'    : 'cors',
                'sec-fetch-site'    : 'same-site',
                'user-agent'        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'x-csrf-token'      : self.csrf(),
            }
            username = ''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxz', k=4))
            payload = {
                'username': username,
                'context' : 'Signup',
                'birthday': '2000-02-13T00:00:00.000Z',
                }
            try:
                response = session.post('https://auth.roblox.com/v1/usernames/validate', json=payload, headers=headers).json()
                if response['code'] == 0:
                    checker.available += 1
                    print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} Username available {username} ({checker.available})")
                    open('available.txt', 'a').write(f'{username}\n')
                else:
                    checker.taken += 1
                    print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Username Taken ({checker.taken})")
            except:
                print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Unknown Error")

os.system('cls')
threads = int(input(f"{Fore.BLUE}[ {Fore.YELLOW}> {Fore.BLUE}]{Fore.RESET} Threads > "))
for i in range(threads):
    threading.Thread(target=checker().sendRequest).start()