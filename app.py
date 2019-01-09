import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "not a secret")
app.config.from_object(__name__)

def quiz_answers():
    """ Create an array of the quiz answers """
    answers = []
    with open("data/answers.txt", "r") as file:
        lines = file.read().splitlines()
    for line in lines:
        answers.append(line)
    return answers


def clear_answers():
    """ Clear the guesses.txt file"""
    with open("data/guesses.txt", "w"):
         return

def write_to_file(filename, data):
        """ Handle the process of writing data to a file """
        with open(filename, "a") as file:
             file.writelines(data)
 
        
def get_all_attempts():
    """Get all of the messages and seperate them by a `br` """
    attempts = []
    with open("data/guesses.txt", "r") as incorrect_attempts:
        attempts = incorrect_attempts.readlines()
    return attempts
  
    
def num_of_attempts():
    """ The number of attempts made by the user on the current quiz """
    attempts = get_all_attempts()
    return len(attempts);
 
    
def attempts_rem():
    """ Return the number of attempts remaining """
    rem_attempts = 5 - num_of_attempts()
    return rem_attempts;


def add_to_score():
    """ Add the score award during the round depeneding on how many turns it took to answer correctly """
    round_score = 6 - num_of_attempts()
    return round_score;
  
    
def final_score(username, score):
    """ If both username and score has text, submit to txt file, otherwise return """
    if username != "" and score != "":
        with open("data/scores.txt", "a") as file:
            """ If a single digit score, format it so it will be sorted as an int (09 rather than 9) """
            if int(score) > 0 and int(score) < 10:
                score = "0" + str(score)
            file.writelines(str(score) + "\n")
            file.writelines(str(username) + "\n")
    else:
        return
  
        
def get_scores():
    usernames = []
    scores = []
    
    """ Open the scores.txt file and split each line"""
    with open("data/scores.txt", "r") as file:
        lines = file.read().splitlines()
    
    """ Add the scores (on each even number line) to the empty score list"""
    """ Add the usernames (on each odd number line) to the empty username list """
    for i, text in enumerate(lines):
        if i%2 ==0:
            scores.append(text)
        else:
            usernames.append(text)
    
    """ Zip the two lists, sort them by scores in reverse """
    usernames_and_scores = sorted(zip(usernames, scores), key=lambda x: x[1], reverse=True)
    return usernames_and_scores


@app.route('/', methods=["GET", "POST"])
def index():
    """ Clear the answers.txt file so attempts_remaining and score is correct """
    clear_answers()
    score = 0
    """Handle POST request"""
    if request.method == "POST":
        username = request.form["username"]
        """ To make sure that a username has been entered """
        if username == "":
            """ If empty, render the index template again """
            return render_template("index.html")
        else:
            """ Grab the username from the form and score to pass through the redirect """
            return redirect(url_for('user', username=username, score=score))
    return render_template("index.html")


@app.route('/<username>/quiz1/<int:score>', methods=["GET", "POST"])
def user(username, score):
    """ User starts with 5 attempts per riddle """
    rem_attempts = 5
    if request.method == "POST":
        """ Add response to the guesses.txt file """
        guess = request.form["answer"]
        write_to_file("data/guesses.txt", guess + "\n")
        """ Grab the quiz answers from the answers.txt file """
        answers = quiz_answers()
        """ If the guess matches the answer, calculate the score for the round """
        if answers[0] == guess:
            score = score + add_to_score()
            """ Clear the guesses.txt file for the next riddle """
            clear_answers()
            """ Take the user to the next question, pass on the username and their score with them """
            return redirect(url_for('quiz2', username=username, score=score))
        else:
            """ If answer is incorrect and the number of attempts they've had is over 5, take them to the next quiz"""
            if num_of_attempts() > 4:
                """ Clear the guesses.txt file for the next riddle """
                clear_answers()
                return redirect(url_for('quiz2', username=username, score=score))
            else:
                """ If answer is incorrect but they've not had more than 5 attempts, reload the current quiz """
                return render_template("quiz1.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz1.html", username=username, rem_attempts=rem_attempts, score=score)


@app.route('/<username>/quiz2/<int:score>', methods=["GET", "POST"])
def quiz2(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[1] == guess:
            score = score + add_to_score()
            clear_answers()
            return redirect(url_for('quiz3', username=username, score=score))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                return redirect(url_for('quiz3', username=username, score=score))
            else:
                return render_template("quiz2.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz2.html", username=username, rem_attempts=rem_attempts, score=score)


@app.route('/<username>/quiz3/<int:score>', methods=["GET", "POST"])
def quiz3(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[2] == guess:
            score = score + add_to_score()
            clear_answers()
            return redirect(url_for('quiz4', username=username, score=score))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                return redirect(url_for('quiz4', username=username, score=score))
            else:
                return render_template("quiz3.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz3.html", username=username, rem_attempts=rem_attempts, score=score)


@app.route('/<username>/quiz4/<int:score>', methods=["GET", "POST"])
def quiz4(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[3] == guess:
            score = score + add_to_score()
            clear_answers()
            return redirect(url_for('quiz5', username=username, score=score))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                return redirect(url_for('quiz5', username=username, score=score))
            else:
                return render_template("quiz4.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz4.html", username=username, rem_attempts=rem_attempts, score=score)
    
@app.route('/<username>/quiz5/<int:score>', methods=["GET", "POST"])
def quiz5(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[4] == guess:
            score = score + add_to_score()
            clear_answers()
            return redirect(url_for('quiz6', username=username, score=score))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                return redirect(url_for('quiz6', username=username, score=score))
            else:
                return render_template("quiz5.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz5.html", username=username, rem_attempts=rem_attempts, score=score)
    
@app.route('/<username>/quiz6/<int:score>', methods=["GET", "POST"])
def quiz6(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[5] == guess:
            score = score + add_to_score()
            clear_answers()
            return redirect(url_for('quiz7', username=username, score=score))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                return redirect(url_for('quiz7', username=username, score=score))
            else:
                return render_template("quiz6.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz6.html", username=username, rem_attempts=rem_attempts, score=score)    
    
@app.route('/<username>/quiz7/<int:score>', methods=["GET", "POST"])
def quiz7(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[6] == guess:
            score = score + add_to_score()
            clear_answers()
            return redirect(url_for('quiz8', username=username, score=score))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                return redirect(url_for('quiz8', username=username, score=score))
            else:
                return render_template("quiz7.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz7.html", username=username, rem_attempts=rem_attempts, score=score) 
   
@app.route('/<username>/quiz8/<int:score>', methods=["GET", "POST"])
def quiz8(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[7] == guess:
            score = score + add_to_score()
            clear_answers()
            return redirect(url_for('quiz9', username=username, score=score))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                return redirect(url_for('quiz9', username=username, score=score))
            else:
                return render_template("quiz8.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz8.html", username=username, rem_attempts=rem_attempts, score=score)
    
@app.route('/<username>/quiz9/<int:score>', methods=["GET", "POST"])
def quiz9(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[8] == guess:
            score = score + add_to_score()
            clear_answers()
            return redirect(url_for('quiz10', username=username, score=score))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                return redirect(url_for('quiz10', username=username, score=score))
            else:
                return render_template("quiz9.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz9.html", username=username, rem_attempts=rem_attempts, score=score)    
    
    
@app.route('/<username>/quiz10/<int:score>', methods=["GET", "POST"])
def quiz10(username, score):
    rem_attempts = 5
    if request.method == "POST":
        write_to_file("data/guesses.txt", request.form["answer"] + "\n")
        guess = request.form["answer"]
        answers = quiz_answers()
        if answers[9] == guess:
            score = score + add_to_score()
            clear_answers()
            final_score(username, score)
            return redirect(url_for('scoreboard'))
        else:
            if num_of_attempts() > 4:
                clear_answers()
                final_score(username, score)
                return redirect(url_for('scoreboard'))
            else:
                return render_template("quiz10.html", username=username, attempts=get_all_attempts(), rem_attempts=attempts_rem(), score=score)
    return render_template("quiz10.html", username=username, rem_attempts=rem_attempts, score=score)
    
    
@app.route('/scoreboard')
def scoreboard():
    usernames_and_scores = get_scores()
    print(usernames_and_scores)
    return render_template("scoreboard.html", usernames_and_scores=usernames_and_scores)


if __name__ == "__main__":
    app.run(os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")),
            debug=True)