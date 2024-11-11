from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

questions = [
    {"id": 1, "title": "How to learn Flask?", "content": "What are the best resources?", "answers": []},
    {"id": 2, "title": "How to use Jinja?", "content": "How can I display data dynamically?", "answers": []}
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        question_id = int(request.form['question_id'])
        answer_content = request.form['content']
        
        # Find the question and add the answer
        question = next((q for q in questions if q["id"] == question_id), None)
        if question:
            question["answers"].append(answer_content)
        return redirect(url_for('home'))
    
    return render_template("home.html", questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
