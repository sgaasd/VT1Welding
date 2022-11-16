    
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 50000))
s.listen(1)
conn, addr = s.accept()

print(conn)
print(addr)

data = conn.recv(8)
print(data)
acc = 0.1
speed = 0.2
time_m = 0
blend = 0


    
#conn.send((bytes('(9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999)', 'ascii')))
while True:
    conn.send((bytes('(1)', 'ascii')))
    data = conn.recv(16)
    
    print(data)

#conn.close()
