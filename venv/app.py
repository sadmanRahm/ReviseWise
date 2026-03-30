
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Your flask app is running successfully"

if __name__ == "__main__":
    app.run(debug=True)