from flask import Flask, request
import messageProcessor as processor
from datetime import datetime

app = Flask(__name__)

log_file_name = "log.txt"

@app.route("/whats", methods=['GET','POST'])
def whats_test():
    if request.method == 'POST': 
        #This code, somehow, populate the message. Its a thing with flask
        request.get_data().decode('utf-8')
        #The message comes in this format:
        #app=WhatsAuto&sender=WhatsAuto+app&message=Mensagem+de+teste&
        
        #And this one gets an ImmutableDict and prints the message from it
        awnser_text = processor.process_message(request.form['message'])
        
        #Generate logs of users and their comands
        with open(log_file_name, "a+") as log_file:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            sender = request.form.get('sender')
            phone = request.form.get('phone')
            message = request.form.get('message')
            
            log = f"\n[{dt_string}] {sender},de número {phone}, enviou o comando '{message}'" 
            log_file.write(log)
        
        #Flask convert dicts automaticaly as Json objects when returning
        awnser = {'reply': awnser_text}
        return awnser
    
    elif request.method == 'GET':
        #just a response to check the server via browser
        return "Servidor de Whatsauto da Aliança\nGerente: Portho"

#This one is to see the logs via webrowser
@app.route("/log", methods=['GET'])
def log_web():
    to_fill = ""
    with open(log_file_name, "r") as log_file:
        for line in log_file.readlines()[1:11]:
            to_fill += line.replace('\n','<br>')
    template = f"""
<html>
<head>
<title>Aliança Bot Logs</title>
</head>
<body>
{ to_fill }
</body>
</html>
"""
    return template


if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0",port=5000)

