import os
from twilio.rest import Client
from flask import Flask,request 

account_sid = 'AC079c58693b2f2b23330d76a774f40000'
auth_token = '89be68f1d9bde7427e8750919bc27bdd'
    
app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def home():
    if request.method == "POST":
        cont_no = request.form.get("number")
        print(cont_no)
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body="This is a test for SEND.",
                            from_='+18183505192',
                            to='+91310-804-3279'

                        )
        return message.status
        
        # return cont_no
    return """
    <form action="" method="POST">
  <div class="form-group">
    <label for="exampleInputEmail1">Email address</label>
    <input type="text" class="form-control" name="number">
    <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>

  </div>
  <button type="submit">Send</button>

  </form>
    """

if __name__ == '__main__':
    app.run()




