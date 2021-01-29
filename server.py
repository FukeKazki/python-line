from util import Server, Message, Body
from multiprocessing import Process


def write(sock: Server):
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


def read(sock: Server):
	while True:
		body = sock.recv_body()
		print(f"{body.message.content.rjust(80)} < Partner")

		if body.message.content == 'bye':
			print("byeされました。通信を終了します")
			break


def main():
	sock = Server(("", 50000))
	sock.accept()

	p_read = Process(target=read, args=(sock,))
	p_read.daemon = True

	p_read.start()
	write(sock)
	print("通信を終了しました")


if __name__ == '__main__':
	main()
