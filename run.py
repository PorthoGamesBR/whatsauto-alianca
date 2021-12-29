from flask import Flask, request
import messageProcessor as processor

app = Flask(__name__)

@app.route("/whats", methods=['GET','POST'])
def whats_test():   
    #This code, somehow, populate the message. Its a thing with flask
    print(request.get_data().decode('utf-8'))
    #The message comes in this format:
    #app=WhatsAuto&sender=WhatsAuto+app&message=Mensagem+de+teste&
    
    #And this one gets an ImmutableDict and prints the message from it
    awnser_text = processor.process_message(request.form['message'])
    
    #Flask convert dicts automaticaly as Json objects when returning
    awnser = {'reply': awnser_text}
    return awnser


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)


