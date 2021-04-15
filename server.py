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
