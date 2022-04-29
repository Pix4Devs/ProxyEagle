from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import Future
import socket
from sys import exit,argv
import os.path

# Author: Z3NTL3
# Studios: Pix4Devs
# Contact: www.pix4.dev

def Usage():
    print(f"""
[Usage]
> python3 {__file__} timeout file.txt protocol

[Example]
> python3 {__file__} 20 proxies.txt http
> python3 {__file__} 20 proxies.txt https
""")

def Logo():
    print("""
\033[38;5;206m╔═╗╦═╗╔═╗═╗ ╦╦ ╦  ╔═╗╔═╗╔═╗╦  ╔═╗
\033[38;5;207m╠═╝╠╦╝║ ║╔╩╦╝╚╦╝  ║╣ ╠═╣║ ╦║  ║╣ 
\033[38;5;206m╩  ╩╚═╚═╝╩ ╚═ ╩   ╚═╝╩ ╩╚═╝╩═╝╚═╝
 \033[38;5;206mMade by Pix4Devs - Pix4.dev
 \033[38;5;207mby Z3NTL3\033[0m
""")

try:
    int(argv[1])
    str(argv[2])

    if "http" or "https" in argv[3]:
        pass
    else:
        raise RuntimeError()
except:
    Usage()
    exit(-1)

def FileRead(file = argv[2]):
    if os.path.exists(argv[2]):
        with open(f"{argv[2]}","r")as file:
            content = file.read().strip(" ").split("\n")
            return content
    else:
        return False

def ProxyConnector(**info):
    try:
        header = f"""GET / HTTP/1.1
Host: www.pix4.dev:{info['protocol']}
Connection: keep-alive
User-Agent: Mozilla/5.0 (compatible; Discordbot/1.0; +https://discordapp.com)"""
        port = int(info['port'])
        sockInit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockInit.settimeout(int(argv[1]))
        sockInit.connect((f"{info['proxy']}",port))
        sockInit.send(header.encode("utf-8"))
        rep = sockInit.recv(1024)
        with open("goods.txt","a+")as f:
            f.write(f"{info['proxy']}:{info['port']}\n")
        return f"\033[32mGood proxy: \033[33m{info['proxy']}:{info['port']}\033[0m"
    except:
        return f"\033[31mBad proxy: \033[33m{info['proxy']}:{info['port']}\033[0m"
    finally:
        sockInit.close()

def Main():
    Logo()
    ct = FileRead()

    if type(ct) is list:
        pass
    elif type(ct) is bool:
        print(f"\033[31mFile: \033[33m\'{argv[2]}\'\033[0m does not exist in the current directory\033[0m")
        exit(-1)
    
    pool = ThreadPoolExecutor(max_workers=61)
    hosts = []
    ports = []

    for proxy in ct:
        h,p = proxy.split(":")
        hosts.append(h)
        ports.append(p)

    ftrs = [pool.submit(ProxyConnector,proxy=Worker[0],port=Worker[1],protocol=argv[3]) for Worker in zip(hosts,ports)]
    for f in as_completed(ftrs):
        print(f.result())
    pool.shutdown()
if __name__ == "__main__":
    Main()