#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import json ,random,time

class RequestHandler(BaseHTTPRequestHandler):

    global MAXSESSIONS , MAXQUESTIONS , sessions , sessionsData ,sessionsQuestionNumbers , sessionsTime ,sessionsScore,TIMEGIVEN
    MAXSESSIONS = 100
    MAXQUESTIONS = {}
    TIMEGIVEN = 20
    sessions=[]
    sessionsData = {}
    sessionsQuestionNumbers = {}
    sessionsTime = {}
    sessionsScore = {}


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
            myid = "".join(query["id"])
            if int(myid) not in sessions:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str.encode("Session "+str(myid)+" doesn't exist.\n"))
                return
        else:
            return self.send_response(400)

        #Check if there is a remaining question
        if sessionsQuestionNumbers[myid]+1 > MAXQUESTIONS[myid]:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str.encode("No questions left.\n"))
            return
        print("\n\nPATH: /next \n"
                "METHOD: GET\n" \
                "PARAMS:\n" \
                    "\tid : "+str(myid) +"\n"
                "SAMPLE: http://localhost:8080/next?myid="+str(myid)+"\n")
        
        data = sessionsData[myid]
        

        
        self.send_response(200)
        self.end_headers()

        answers = data[sessionsQuestionNumbers[myid]]["incorrect_answers"]
        answers.append(str(data[sessionsQuestionNumbers[myid]]["correct_answer"]))
        question = ("Question Number: "+str(sessionsQuestionNumbers[myid]+1) +"\nCategory: " + str(data[sessionsQuestionNumbers[myid]]["category"])+
        "\nQuestion: " + str(data[sessionsQuestionNumbers[myid]]["question"]).replace("&quot;","").replace("&#039;","'").replace("&Uuml;","Ü") +"\n\n"+
        "Answers: \n-"+ "\n-".join(answers) +"\n\n" +"You have {} seconds to answer.".format(TIMEGIVEN) +"\n"
        )
        

        sessionsTime[myid] = time.time()

        sessionsQuestionNumbers[myid] +=1
        self.wfile.write(str.encode(urllib.parse.unquote(question)))


    def start_new_game(self,query):
        reqUrl = "https://opentdb.com/api.php?amount="
        amount = 10
        log = "\n\nPATH: /newGame \n" \
        "METHOD: GET\n" \
        "PARAMS:\n" 
        if "amount" in query.keys():
            reqUrl += str("".join(query["amount"]))
            amount = "".join(query["amount"])
        else:
            reqUrl = "https://opentdb.com/api.php?amount=10"

        log += "\tamount: " + str(amount) +"\n"
        if "difficulty" in query.keys():
            reqUrl += "&difficulty=" + str("".join(query["difficulty"]))
            log += "\tdifficulty: " + str("".join(query["difficulty"])) + "\n"
        if "category" in query.keys():
            reqUrl += "&category=" + str("".join(query["category"]))
            log += "\tcategory: " + str("".join(query["category"])) + "\n"

        req = urllib.request.Request(reqUrl)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            js = json.loads(data)
        
        
            "\tamount: N (integer) default=10\n"
        sample = "SAMPLE: http://localhost:8080/newGame?amount=" + "=".join(reqUrl.split("=")[1:])
        
        log += sample
        print(log)

        newSession = random.randint(0,MAXSESSIONS*10)
        while(newSession in sessions):
            newSession = random.randint(0,MAXSESSIONS*10)
        sessions.append(newSession)
        sessionsData[str(newSession)] = js["results"]
        sessionsQuestionNumbers[str(newSession)] = 0 

        MAXQUESTIONS[str(newSession)] = int(amount)
        sessionsScore[str(newSession)] = 0
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
            myid = "".join(query["id"])
            currentTime = time.time()
            if int(myid) not in sessions:
                return self.bad_session()
            elif currentTime - sessionsTime[myid] > TIMEGIVEN:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str.encode("Time is up. Answered in {} seconds.".format(currentTime-sessionsTime[myid])))
                return
                
            else:
                inp ="".join(query["answer"])
                data = sessionsData[myid]
                if inp==data[sessionsQuestionNumbers[myid]-1]["correct_answer"]:
                    self.send_response(200)
                    self.end_headers()
                    sessionsScore[myid] +=1
                    output ="CORRECT ANSWER!! \n {} correct of {} questions \n There are  {} more questions".format(sessionsScore[myid],
                        sessionsQuestionNumbers[myid],
                        MAXQUESTIONS[myid]-sessionsQuestionNumbers[myid])
                    self.wfile.write(str.encode(output))
                else:

                    self.send_response(200)
                    self.end_headers()
                    output ="WRONG ANSWER!! \n Correct answer was: {} \n {} correct of {} questions \n There are  {} more questions".format(data[sessionsQuestionNumbers[myid]-1]["correct_answer"],
                        sessionsScore[myid],
                        sessionsQuestionNumbers[myid],
                        MAXQUESTIONS[myid]-sessionsQuestionNumbers[myid])
                    self.wfile.write(str.encode(output))

                
        else:
            return self.bad_session()


    def do_POST(self):
        url = urlparse(self.path)
        if url.path == "/answer":    
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
        elif url.path =="/newGame":
            if len(sessions) < MAXSESSIONS:
                return self.start_new_game(parse_qs(url.query))
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
