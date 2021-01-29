from dataclasses import dataclass, asdict
from enum import Enum
from socket import socket, AF_INET, SOCK_STREAM
import json
from typing import Final

BUF_SIZE: Final = 1024


class Action(Enum):
	READ = '1'
	WRITE = '2'
	DELETE = '3'


class State(Enum):
	SUCCESS = 'success'
	FAILED = 'failed'
	IDLE = 'idle'


@dataclass
class Message:
	content: str = None


@dataclass
class Response:
	state: str = State.IDLE.value
	message: Message = None


@dataclass
class Body:
	message: Message = None


class Server:
	sock = None
	sock_c = None

	def __init__(self, address: tuple):
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.bind(address)
		self.sock.listen()

	def __del__(self):
		self.sock.close()

	def accept(self):
		self.sock_c, _ = self.sock.accept()

	def recv(self) -> str:
		response = self.sock_c.recv(BUF_SIZE)
		return response.decode('UTF-8')

	def send(self, data: str):
		self.sock_c.sendall(data.encode('UTF-8'))

	def c_close(self):
		self.sock_c.close()

	def recv_body(self) -> Body:
		data = self.recv()
		data = json.loads(data)
		if data['message']:
			data['message'] = Message(**data['message'])
		return Body(**data)

	def send_response(self, response: Response):
		data = asdict(response)
		data = json.dumps(data)
		self.send(data)

	def send_body(self, body: Body) -> None:
		data = asdict(body)
		data = json.dumps(data)
		self.send(data)


class Client:
	sock = None

	def __init__(self, address: tuple):
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.connect(address)

	def __del__(self):
		self.sock.close()

	def recv(self) -> str:
		response = self.sock.recv(BUF_SIZE)
		return response.decode('UTF-8')

	def send(self, data: str) -> None:
		self.sock.sendall(data.encode('UTF-8'))

	def recv_response(self) -> Response:
		response = self.recv()
		data = json.loads(response)
		if data['message']:
			data['message'] = [Message(**message) for message in data['message']]
		return Response(**data)

	def recv_body(self) -> Body:
		data = self.recv()
		data = json.loads(data)
		if data['message']:
			data['message'] = Message(**data['message'])
		return Body(**data)

	def send_body(self, body: Body) -> None:
		data = asdict(body)
		data = json.dumps(data)
		self.send(data)
