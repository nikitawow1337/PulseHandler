#!/usr/bin/env python

import os
import asyncore
import socket
import logging


class Server(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.logger = logging.getLogger('Server')
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(address)
        self.address = self.socket.getsockname()
        self.logger.debug('binding to %s', self.address)
        self.listen(5)

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        if client_info is not None:
            self.logger.debug('handle_accept() -> %s', client_info[1])
            ClientHandler(client_info[0], client_info[1])


class ClientHandler(asyncore.dispatcher):
    def __init__(self, sock, address):
        asyncore.dispatcher.__init__(self, sock)
        self.logger = logging.getLogger('Client ' + str(address))
        self.data_to_write = []

    def writable(self):
        return bool(self.data_to_write)

    def handle_write(self):
        data = self.data_to_write.pop()
        sent = self.send(data[:1024])
        if sent < len(data):
            remaining = data[sent:]
            self.data.to_write.append(remaining)
        self.logger.debug('handle_write() -> (%d) "%s"', sent, data[:sent].rstrip())
        self.logger.findCaller()

    def handle_read(self):
        data = self.recv(1024)
        self.logger.debug('handle_read() -> (%d) "%s"', len(data), data.rstrip())
        # !!!!! EAXAMPLE - ECHO
        self.data_to_write.insert(0, data)
        self.logger.warning("message!!")
        filepath = os.path.dirname(os.path.abspath(__file__)) + "\\recievedData.txt"
        decoded = str(data.decode('UTF-8'))
        if decoded:
            # filepath.replace("\\\\", "\\")  # Replace \\ -> \. Comment/Uncomment this if getting error
            # print("Filepath: ", filepath)
            # strinfo = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'
            # f = open(file=filepath + "\\.txt", mode="a+", encoding="UTF-8")
            # f.write(strinfo)
            f = open(file=filepath, mode="w+", encoding="UTF-8")
            f.write(decoded)
            f.close()


def handle_close(self):
    self.logger.debug('handle_close()')
    self.close()


def main():
    # filepath = os.path.dirname(os.path.abspath(__file__)) + "/recievedData.txt"
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')
    # fh = logging.FileHandler(filename=filepath, mode="w+")
    host = '192.168.0.61'
    port = 8888

    s = Server((host, port))
    asyncore.loop()


if __name__ == '__main__':
    main()
