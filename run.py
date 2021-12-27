from flask import Flask, request

app = Flask(__name__)

@app.route("/whats", methods=['GET','POST'])
def whats_test():
    #request_data = request.get_json()
    #request.data.decode('utf-8')
    
    print(request.get_data().decode('utf-8'))
    print(request.data.decode('utf-8'))
    
    #message = request_data['message']
    #print(message)
    return "Hello Whatsauto"



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)


