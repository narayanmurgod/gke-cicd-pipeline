from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route('/about')
def about():
    return "This is the About Page."

@app.route('/services')
def services():
    return "Here are our Services."

@app.route('/contact')
def contact():
    return "Contact us at contact@example.com."

if __name__ == '__main__':
    app.run(debug=True)
