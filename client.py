from util import Client, Message, Body
from multiprocessing import Process


def write(sock):
	while True:
		content = input()

		message = Message(
			content=content
		)

		body = Body(
			message=message
		)

		sock.send_body(body)

		if content == 'bye':
			break


def read(sock):
	while True:
		response = sock.recv_body()
		print(f"{response.message.content.rjust(80)} < Partner")

		if response.message.content == 'bye':
			print("byeされました。通信を終了します")
			break


def main():
	sock = Client(("localhost", 50000))

	p_read = Process(target=read, args=(sock,))

	p_read.daemon = True
	p_read.start()
	write(sock)
	print("通信を終了しました")


if __name__ == '__main__':
	main()
