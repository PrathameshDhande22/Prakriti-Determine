from flask import Flask, url_for,redirect,render_template, request, jsonify
from get_intent import get_response, get_intent

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer":response}
    return jsonify(message)



if __name__ == "__main__":
    app.run(debug=True)