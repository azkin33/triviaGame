import os ,subprocess

x = input('''Hi, type "/new [questionCount]" to start a new game where questionCount is a whole number. (Default questionCount is 10)
\n/next to get next question \n /answer your_answer to answer. \n.
You can change session by typing /id your_id. \nType /exit to exit\n\n\n''')

myId=0

while(x != "/exit"):
    if x.split(" ")[0] == "/new":
        #os.system("curl http://localhost:8080/newGame?amount=10")
        reqUrl = "curl http://localhost:8080/newGame?amount=" 
        if len(x.split(" "))==2:
            reqUrl += str(x.split(" ")[1])
        else:
            reqUrl += str(10)
        p = subprocess.Popen(reqUrl, stdout=subprocess.PIPE, shell=True)
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
    elif x.split(" ")[0] == "/id":
        myId = x.split(" ")[1]
    x=input()
