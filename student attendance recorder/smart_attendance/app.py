from flask import Flask, render_template, request

app = Flask(__name__)

# List of students
students = ["Gurleen Kaur",
    "Priti Thakur",
    "Bhumi Wadkute",
    "Rishi Purohit",
    "Ishwar Dawalbaje",
    "Nikhi Hatagale ",
    "Girish Lolewar",
    "Aayush Harne",
    "Aavishkar",
    "Gayatri Sangle"]

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/submit', methods=['POST'])
def submit():
    present = []
    absent = []

    for student in students:
        status = request.form.get(student)
        if status == "P":
            present.append(student)
        else:
            absent.append(student)

    return render_template('result.html', present=present, absent=absent)

if __name__ == '__main__':
    app.run(debug=True)
