## chatApp
![](https://images.velog.io/images/hyeseong-dev/post/8bec5bac-e910-44c7-a07b-52baaeceb3af/image.png)

## Directory Structure

- server.py
- client.py
(poetry.lock, pyproject.toml 파일은 poetry를 이용하여 가상환경을 구성하여 나온 파일들입니다. 다른 가상환경을 사용해도 무방해요.)
![](https://images.velog.io/images/hyeseong-dev/post/9a9a7ccf-9ac1-43bf-b576-da8bb6919036/image.png)


### 라이브러리, 패키지
- twisted
- names

## server.py

```python
import names
from twisted.internet import protocol, reactor # 네트워크 통신을 쉽게 구현 하도록 도와주는 패키지

COLORS = [ # 사용자마다 출력 글자 색깔 지정
    '\033[31m', # RED
    '\033[32m', # GREEN
    '\033[33m', # YELLOW
    '\033[34m', # BLUE
    '\033[35m', # MAGENTA
    '\033[36m', # CYAN
    '\033[37m', # WHITE
    '\033[4m',  # UNDERLINE
]


transports = set()
users = set() # 유저의 이름을 저장 할 변수

class Chat(protocol.Protocol):
    """
    채팅 서버의 로직 정의 
    """
    def connectionMade(self):
        ''' 사용자가 서버에 접속하면 'connected' 메시지 출력'''
        name = names.get_first_name()
        color = COLORS[len(users)%len(COLORS)]
        users.add(name)
        transports.add(self.transport) # 사용자가 접속하면 transport(클라이언트)추가
        self.transport.write(f'{color}{name}\
        \033[0m'.encode('utf-8')) # client 연결시, 접속된듯?메시지를 클라이언테에게 전송(문자열 -> 바이트)
                                            # name은 사용자가 접속하면 임의의 이름을 부여함.
                                            # \033[0m은 컬러를 리셋하는 코드, 이름에만 색을 칠하고 메시지에는 칠하지 않음
    def dataReceived(self, data):
        '''사용자가 서버에 메시지를 보내면 실행 사용자 메시지(data) 출력'''
        for t in transports: # 모든 클라이언트를 하나씩 돌면서 만약 내가 보낸 메시지가 아니면 메시지를 전달함
            if self.transport is not t:
                t.write(data)

class ChatFactory(protocol.Factory):
    '''통신 프로토콜 정의'''
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory()) # TCP 8000번 포트 리쓴~
reactor.run()


```

## client.py

```python
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


```


