import os ,subprocess

x = input('''Hi, type /new to start a new game \n/next to get next question \n /answer your_answer to answer \n. Y
ou can change session by typing /id your_id. \n Type /exit to exit\n\n\n''')

myId=0

while(x != "/exit"):
    if x == "/new":
        #os.system("curl http://localhost:8080/newGame?amount=10")
        p = subprocess.Popen("curl http://localhost:8080/newGame?amount=10", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.status = p.wait()
        myId = output.split()[-1].decode()
        print("\n\nYour id is: " + str(myId)+"\n\n")
    elif x == "/next":
        print("\n\n")
        os.system("curl http://localhost:8080/next?id="+str(myId))

        print("\n\n")
    elif x.split(" ")[0] == "/answer":
        print("\n\n")
        print("+".join(x.split(" ")[1:]))
        os.system("curl -X POST http://localhost:8080/answer?id="+str(myId)+"\&answer="+"+".join(x.split(" ")[1:]))
        print("\n\n")
    x=input()
