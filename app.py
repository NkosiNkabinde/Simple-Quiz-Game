from flask import Flask, render_template, request, session, redirect, url_for
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key in production

# Load questions once at startup
with open('questions.json', 'r') as f:
    all_questions = json.load(f)

@app.route('/')
def index():
    # Randomize questions order per session
    session['questions'] = random.sample(all_questions, len(all_questions))
    session['score'] = 0
    session['current'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    current = session.get('current', 0)
    questions = session.get('questions', [])

    if current >= len(questions):
        # All questions done, go to results
        return redirect(url_for('result'))

    if request.method == 'POST':
        selected = request.form.get('choice')
        if selected:
            # Check answer correctness
            if selected == questions[current]['answer']:
                session['score'] += 1
            session['current'] = current + 1
            # Redirect to GET to prevent form resubmission
            return redirect(url_for('quiz'))

    question = questions[current]
    return render_template('quiz.html',
                           question_num=current + 1,
                           total=len(questions),
                           question=question['question'],
                           choices=question['choices'])

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(session.get('questions', []))
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)
