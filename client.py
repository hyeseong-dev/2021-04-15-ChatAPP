import socket
import select
import sys

name = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',8000))

while True: # 서버로부터 메시지를 기다림
    read, write, fail = select.select((s, sys.stdin), (), ()) # socket에서 메시지를 읽을수 있을 때까지 대기
                                                              # sys.stdin은 사용자가 키보드 엔터를 입력 할 때까지 기다림      
    for desc in read:# 메시지가 도착하면 
        if desc == s: # 만약 서버에서 온 메시지라면 출력
            data = s.recv(4096) # 4096바이트를 읽음.
            print(data.decode('utf-8')) # byte -> string 출력

            if name is None:        # 처음 접속시 부여 받은 이름을 저장!
                name = data.decode()  #
                s.send(f'{name} is connected!'.encode('utf-8'))     # 다른 사람에게 접속 사실을 알리게 됩니다.
        else: # 만약 사용자가 입력한 메시지라면
            msg = desc.readline() # 사용자의 입력 문자열을 읽어 서버에 전송함
            msg = msg.replace('\n','') # 사용자의 입력 문자열을 읽어 서버에 전송함
            s.send(f'{name}: {msg}'.encode())
