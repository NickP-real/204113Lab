import socket
import threading
import time

# !add time, log,√
# server to all chat (admin)

TEXT_FORMAT = "ascii"
BUF_SIZE = 1024
user_list = dict()

# connect, bind
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 9999))


def server():
    server_socket.listen()
    back_thread()
    # server_terminal()
    # print("[SERVER] Program is ending...")
    # server_socket.close()


def server_time():
    localtime = time.asctime(time.localtime(time.time()))
    time_hour = localtime.split()[3]
    return [localtime, time_hour]


def back(client, time_hour):
    try:
        username = client.recv(BUF_SIZE).decode(TEXT_FORMAT)
        user_list[str(username)] = client
        client.send(("[SERVER] Welcome " + str(username) + "\r\n").encode(TEXT_FORMAT))
        client_name = list(user_list.keys())[list(user_list.values()).index(client)]
        user(client, time_hour)
        chat(client)
    except:
        print("[%s] %s has disconnected." % (str(time_hour), str(client_name)))
        if client_name in user_list:
            del user_list[client_name]


def back_thread():
    print("[SERVER] has started!")
    while True:
        client_socket, addr = server_socket.accept()
        print("[%s] Got connection from %s" % (str(server_time()[1]), str(addr)))
        thread = threading.Thread(target=back, args=(client_socket, server_time()[1]))
        thread.start()
        print("[SERVER] Active Connection:", threading.active_count() - 1)


def user(client, time_hour):
    user_text = "\n".join(list(user_list.keys()))

    client.send(
        (
            "[SERVER] User Online Count: "
            + str(threading.active_count() - 1)
            + " at %s" % str(time_hour)
            + "\n"
            + str(user_text)
        ).encode(TEXT_FORMAT)
    )


def chat(client):
    client_name = list(user_list.keys())[list(user_list.values()).index(client)]
    while True:
        recv_msg = client.recv(BUF_SIZE).decode(TEXT_FORMAT)
        time_hour = server_time()[1]
        # print(recv_msg)
        if recv_msg == "!quit":
            client.send("!quit".encode(TEXT_FORMAT))
            print(
                "[%s] User: " % str(time_hour) + str(client_name) + " has disconnected."
            )
            del user_list[client_name]
            break

        elif recv_msg == "!user":
            # send user list
            user(client, time_hour)
            print(
                "[%s] Sent user information to %s"
                % (
                    str(time_hour),
                    str(client_name),
                )
            )
        # send to all
        elif "!all" in recv_msg:
            for i in user_list:
                if i == client_name:
                    continue
                user_list[i].send(
                    str(
                        "[%s][ALL] " % str(time_hour)
                        + str(client_name)
                        + ": "
                        + " ".join(recv_msg.split()[1:])
                    ).encode(TEXT_FORMAT)
                )
            client.send("Message sent!".encode(TEXT_FORMAT))
            print(
                "[%s] User: %s, Sent to ALL, Message: %s"
                % (
                    str(time_hour),
                    str(client_name),
                    str(" ".join(recv_msg.split()[1:])),
                )
            )

        else:
            # check username, send text
            if recv_msg.split()[0] in user_list:
                # send to use
                user_list[recv_msg.split()[0]].send(
                    str(
                        "[%s][DIRECTED] " % str(time_hour)
                        + str(client_name)
                        + ": "
                        + " ".join(recv_msg.split()[1:])
                    ).encode(TEXT_FORMAT)
                )
                client.send("Message sent!".encode(TEXT_FORMAT))
                print(
                    "[%s] User: %s, Sent to User: %s, Message: %s"
                    % (
                        str(time_hour),
                        str(client_name),
                        str(recv_msg.split()[0]),
                        str(" ".join(recv_msg.split()[1:])),
                    )
                )
            else:
                # send wrong
                client.send("[SERVER] Unknown User".encode(TEXT_FORMAT))


def server_terminal():
    while True:
        command = input()

    pass


server()
