from flask import Flask, request

app = Flask.init(__name__)

@app.route("/whats")
def whats_test():
    return "Hello Whatsauto"



if __name__ == "__main__":
    app.run(port=5000)


