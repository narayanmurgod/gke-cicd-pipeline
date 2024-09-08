from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
greetings = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        greetings.append((name, message))
        return redirect(url_for('greet'))
    return render_template('form.html', greetings=greetings)

@app.route('/greet')
def greet():
    return render_template('greet.html', greetings=greetings)

if __name__ == '__main__':
    app.run(debug=True)
