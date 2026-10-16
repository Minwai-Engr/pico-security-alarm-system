import network
import socket
import time


ssid = 'RPI_PICO_AP'
password = 'open_sesame'

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
    pass
print('Connection is successful')
print(ap.ifconfig())

#Create a socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5) # maximum bumber of requests that can be queued


#Create a home page
def index_page():
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Home</h1>
        <p>Welcome.</p>
        <a href="/">Home</a><br>
        <a href="/about">About</a><br>
        <a href="/security">Security</a>
    </body>
    </html>
    """
#Create an about us page
def about_page():
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>About</h1>
        <p>This is the about page.</p>
        <a href="/">Home</a>
    </body>
    </html>
    """

#Create a security page
def security_page():
    return """\
    <!DOCTYPE html>
    <h1>Security</h1>
    <p>Sensor Page</p>
    <a href="/">Home</a>
    """


# Response when connection received 
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request_str = request.decode()
    path = request_str.split(" ")[1]

    if path == "/":
        response = index_page()
    elif path == "/about":
        response = about_page()
    elif path == "/security":
        response = security_page()
    else:
        response = index_page()

        
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()

roomA = Room("336B", "ELW", 7, 19, "lab")

bob = Uid(334, "bob", "bobby", "student")
jeremy = Uid(335, "jeremy", "jeremy", "student")
roomA.add_open_uids(bob.uid)
roomA.add_open_uids(jeremy.uid)

roomA.add_open_uids([13, 17])
roomA.add_closed_uids([15, 16, 17])
roomA.add_closed_uids(17)

#roomA.add_open_uids(bob._registry)

roomA.print_room()



