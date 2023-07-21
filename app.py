from boggle import Boggle
from flask import Flask, render_template, redirect, flash, session, request, jsonify

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenz"

@app.route("/")
def start():
    """render landing page"""
    #initialize board as a session variable
    del session["board"]
    if(session.get("board", None) == None):
        session["guess_list"] = []
        session["board"] = boggle_game.make_board()
    #session["board"][0][0] = session.get("guess","not yet set in javascript")
    return render_template("start.html",
        header = "Game Start",
        title = "Boggle",
        board = session["board"])
        
@app.route("/submit", methods = ['POST'])
def sub_question():
    """accept guess and use the boggle game to send the guess verification results to Javascript"""
    guess = request.get_json().get("guess", "ERR: No Guess")
    result = boggle_game.check_valid_word(session["board"],guess)
    
    if(session.get("guess_list", None) == None): session["guess_list"] = [guess]
    elif(guess in session["guess_list"]): result = "already-guessed"
    else : session["guess_list"] += [guess]
    
    data = {"result": result}
    return jsonify(data)

@app.route("/scores", methods = ['POST', 'GET'])
def scores():
    data = {"result": "result"}
    if(request.method == 'POST'):
        score = request.get_json().get("score",0)
        if(int(session.get("highscore",-1)) < int(score)): 
            session["highscore"] = score
        #return jsonify(data)
        if(session.get("games_played") == None): 
            session["games_played"] = 1
        else: 
            session["games_played"] += 1
        return jsonify({"result": "result"})
    elif(request.method =='GET'):
        return jsonify({"highscore":session.get("highscore", "none yet"), "gamesPlayed":session.get("games_played", "none yet")})
    else:
        return jsonify({"success":"true"})