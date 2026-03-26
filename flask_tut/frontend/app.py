from flask import Flask, render_template, request
from datetime import datetime
import requests
import os 
#BACKEND_URL = "http://127.0.0.1:9000"
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:9000")

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')

    return render_template(
        'index.html',
        day_of_week=day_of_week,
        current_time=current_time,
        success=None,
        error=None
    )

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)

    try:
        response = requests.post(f"{BACKEND_URL}/submit", json=form_data)
        result = response.json()

        if result["status"] == "success":
            return render_template(
                'index.html',
                success="Data submitted successfully",
                error=None,
                day_of_week=datetime.today().strftime('%A'),
                current_time=datetime.now().strftime('%H:%M:%S')
            )
        else:
            return render_template(
                'index.html',
                error=result["message"],
                success=None,
                day_of_week=datetime.today().strftime('%A'),
                current_time=datetime.now().strftime('%H:%M:%S')
            )

    except Exception as e:
        return render_template(
            'index.html',
            error=str(e),
            success=None,
            day_of_week=datetime.today().strftime('%A'),
            current_time=datetime.now().strftime('%H:%M:%S')
        )

@app.route('/get_data')
def get_data():
    response = requests.get(f"{BACKEND_URL}/view")
    data = response.json()
    return data

@app.route('/todo')
def todo():
    return render_template('todo.html')



@app.route('/submit_todo', methods=['POST'])
def submit_todo():
    form_data = dict(request.form)

    response = requests.post(f"{BACKEND_URL}/submittodoitem", json=form_data)

    return "To-Do Item Submitted"


if __name__ == '__main__':
    app.run(debug=True)