import socket
import string
import threading

TEXT_FORMAT = "ascii"
BUF_SIZE = 1024

# !add thread stop √
# !add all chat √
# client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect
client.connect((socket.gethostname(), 9999))


def start():
    # username check
    while True:
        user = input("Username: ")
        if user in string.whitespace or user in string.punctuation:
            print("Username must has at least a character!")
        else:
            break

    # send username
    client.send(user.encode(TEXT_FORMAT))
    print("type !help for more infomation.")
    # chat()
    back_thread()
    send_text()


"""
sent to server list:
    -!user
    -!quit
    -!all
    -text
"""


def back_thread():
    thread = threading.Thread(target=get_text)
    thread.start()


def get_text():
    try:
        while True:
            recv = client.recv(BUF_SIZE).decode(TEXT_FORMAT)
            if recv == "!quit":
                break
            print(recv)
    except:
        print("Server Error!")
        print('Type "quit" to exit the program.')
        client.close()


def send_text():
    try:
        while True:
            inp1 = input()
            # check
            if inp1 not in string.whitespace:
                if inp1[0] == "!":
                    text = inp1[1:].lower()
                    if text == "help":
                        help_()
                    elif text == "user":
                        client.send("!user".encode(TEXT_FORMAT))

                    elif text.split()[0] == "all" and len(text.split()) > 1:
                        client.send(str(inp1).encode(TEXT_FORMAT))

                    else:
                        print("type !help for more infomation.")

                elif inp1.lower() == "quit":
                    client.send("!quit".encode(TEXT_FORMAT))
                    print("Program is ending...")
                    break

                elif len(inp1.split()) >= 2:
                    client.send(str(inp1).encode(TEXT_FORMAT))
                    # print(client.recv(BUF_SIZE).decode(TEXT_FORMAT))
                else:
                    print("Need 2 Arguments: <Username> <Text>.")
            else:
                print("Need 2 Arguments: <Username> <Text>.")
        client.close()
    except:
        client.close()


def help_():
    print(
        """--------------------------------------------------
To send the message: <Username> <Msg>,
To want to know the online user now: !user,
To send the message to all user: !all <Msg>,
To end the program: quit
--------------------------------------------------"""
    )


start()
