from flask import Flask, request

app = Flask(__name__)

@app.route("/whats", methods=['GET','POST'])
def whats_test():   
    #This code, somehow, populate the message. Dont know why it works that way, but it does
    print(request.get_data().decode('utf-8'))
    #The message comes in this format:
    #app=WhatsAuto&sender=WhatsAuto+app&message=Mensagem+de+teste&
    
    #And this one gets an ImmutableDict and prints the message from it
    print(request.form['message'])
    
    #Flask convert dicts automaticaly as Json objects when returning
    awnser = {'reply': 'Hello Whatsauto'}
    return awnser


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)


