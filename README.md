# Trivia Game

This is basically a http server that you can play a trivia game.

Run httpserver inside main.py by typing,
>python3 main.py

From another terminal,
To start a new game type,
>curl http://<span></span>localhost:8080/newGame?amount=10

10 is the default. You can change it.
You can also send difficulty and category parameters.
>curl http://<span></span>localhost:8080/newGame?amount=10\\&difficulty=easy\\&category=9

**Normally you don't need "\" before "&" but BaseHttpRequestHandler doesn't receive parameters after the first "&" if you don't put "\" before them.**

To get next question:
>curl http://<span></span>localhost:8080/next?id=585

To answer:
>curl -X POST http://<span></span>localhost:8080/answer?id=585\\&answer=YOURANSWER

Run triviaGame.py from another terminal tab if you don't want to mess with long curl commands.

Also there is another script that i wrote to make testing faster. You can also use it for quality of life.
>python3 triviaGame.py
