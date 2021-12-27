from flask import Flask, request

app = Flask(__name__)

@app.route("/whats", methods=['POST'])
def whats_test():
    request_data = request.get_json()
    
    message = request_data['message']
    print(message)
    return "Hello Whatsauto"



if __name__ == "__main__":
    app.run(port=5000)


