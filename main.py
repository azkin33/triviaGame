#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import json
import random
import time
class RequestHandler(BaseHTTPRequestHandler):

    global MAXSESSIONS , MAXQUESTIONS , sessions , sessionsData ,sessionsQuestionNumbers , sessionsTime
    MAXSESSIONS = 100
    MAXQUESTIONS = 10
    sessions=[]
    sessionsData = {}
    sessionsQuestionNumbers = {}
    sessionsTime = {}


    def say_hello(self, query):
        """
        Send Hello Message with optional query
        """
        mes = "Hello"
        if "name" in query:
            # query is params are given as array to us
            mes += " " + "".join(query["name"])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode(mes+"\n"))

    def randomize_answers(myList):
        pos = random.randint(0,len(myList)-1)
        right = myList[len(myList)]
        temp = myList[pos]
        myList[pos] = right
        myList[len(myList)-1] = temp
        return myList

    def get_next_question(self,query):
        if "id" in query:
            id = "".join(query["id"])
            if int(id) not in sessions:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str.encode("Session "+str(id)+" doesn't exist.\n"))
                return
        else:
            return self.send_response(400)

        #Check if there is a remaining question
        if sessionsQuestionNumbers[id]+1 > MAXQUESTIONS:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str.encode("No questions left.\n"))
            return
        print("\n\nPATH: /next \n"
                "METHOD: GET\n" \
                "PARAMS:\n" \
                    "\tid : "+str(id) +"\n"
                "SAMPLE: http://localhost:8080/next?id="+str(id)+"\n")
        
        data = sessionsData[id]
        print(sessionsData[id])

        
        self.send_response(200)
        self.end_headers()

        answers = data[sessionsQuestionNumbers[id]]["incorrect_answers"]
        answers.append(str(data[sessionsQuestionNumbers[id]]["correct_answer"]))
        question = ("Question Number: "+str(sessionsQuestionNumbers[id]+1) +"\nCategory: " + str(data[sessionsQuestionNumbers[id]]["category"])+
        "\nQuestion: " + str(data[sessionsQuestionNumbers[id]]["question"]).replace("&quot;","").replace("&#039;","") +"\n\n"+
        "Answers: \n-"+ "\n-".join(answers) +"\n\n" +"You have 15 seconds to answer." +"\n"
        )
        print(question)

        sessionsTime[id] = time.time()

        sessionsQuestionNumbers[id] +=1
        self.wfile.write(str.encode(urllib.parse.unquote(question)))


    def start_new_game(self):
        req = urllib.request.Request("https://opentdb.com/api.php?amount=10")
        with urllib.request.urlopen(req) as response:
            data = response.read()
            js = json.loads(data)
        
        
        print("\n\nPATH: /newGame \n"
        "METHOD: GET\n" \
        "PARAMS:\n" \
            "\tamount: N (integer) default=10\n"
        "SAMPLE: http://localhost:8080/newGame?amount=10\n")
        
        

        newSession = random.randint(0,MAXSESSIONS*10)
        while(newSession in sessions):
            newSession = random.randint(0,MAXSESSIONS*10)
        sessions.append(newSession)
        sessionsData[str(newSession)] = js["results"]
        sessionsQuestionNumbers[str(newSession)] = 0 
        print(sessionsData)
        #currentData = {str(newSession) : js["results"]}
        #sessionsData.append(currentData)
       # print(sessionsData)
        #print(sessions)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode("New Trivia Game Started \nSession ID = "+str(newSession)+"\n"))
    


    def bad_session(self):
        self.send_response(400)
        self.end_headers()
        self.wfile.write(str.encode("Invalid session id."))
    
    def answer_question(self,query):
        print(query)
        if "id" in query:
            id = "".join(query["id"])
            
            if int(id) not in sessions:
                return self.bad_session()
            else:
                inp ="".join(query["answer"])
                data = sessionsData[id]
                if inp==data[sessionsQuestionNumbers[id]-1]["correct_answer"]:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(str.encode("HARİKA"))
                else:

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(str.encode("NOOBSUN" + str(data[sessionsQuestionNumbers[id]-1]["correct_answer"])))

                
        else:
            return self.bad_session()


    def do_POST(self):
        # Doesn't do anything with posted data
        print(self.path)
        
        url = urlparse(self.path)
        if url.path == "/answer":
            print(url)
            
            return self.answer_question(parse_qs(url.query))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(str.encode("POST!"))
    
    def do_GET(self):
        # Parse incoming request url
        url = urlparse(self.path)
        if url.path == "/hello":
            return self.say_hello(parse_qs(url.query))
        elif url.path == "/newGame":
            if len(sessions) < MAXSESSIONS:
                return self.start_new_game()
        elif url.path == "/next":
            
            return self.get_next_question(parse_qs(url.query))
            
 
        # return 404 code if path not found
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Error!\n')
        

if __name__ == "__main__":
    port = 8080
    print(f'Listening on localhost:{port}')
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()
