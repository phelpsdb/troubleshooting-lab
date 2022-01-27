import socket
import time

def connect_socket(reqid):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("", 8080))
    s.send(b"GET /hello_world.html HTTP/1.1\n")
    chunk = s.recv(16)
    print(f"(Load Tester) Reponse for {reqid}: {str(chunk, 'utf-8')}")


while True:
    time.sleep(0.03)
    try:
        connect_socket(time.time())
    except Exception as e:
        print(f"Error in load tester: {e}")
        time.sleep(1)
