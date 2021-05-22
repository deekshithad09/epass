
from flask import Flask,render_template
from flask import request
from twilio.rest import Client
from flask_bootstrap import Bootstrap
import requests
import requests_cache
auth_sid='ACa50ebf420da3a7815d5788d8427b6dca'
auth_token='02fdd5414acea801829f391cb65b5fc4'
client=Client(auth_sid,auth_token)
app=Flask(__name__,static_url_path="/static")
Bootstrap(app)
@app.route('/')
def registration_form():
    return render_template('login.html')

@app.route('/login_page',methods=['POST','GET'])

def login_registration_dtls():
    first_name=request.form['fname']
    last_name=request.form['lname']
    email_id=request.form['eid']
    source_st=request.form['source_st']
    source_dt=request.form['source']
    destination_st=request.form['destination_st']
    destination_dt=request.form['destination']
    phone_number=request.form['phno']
    id_proof=request.form['idcard']
    date=request.form['trip']
    full_name=first_name+" "+last_name
    r=requests.get('https://api.covid19india.org/v4/data.json')
    json_data=r.json()
    cnt=json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop=json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass=(cnt/pop)*100
    if travel_pass<30 and request.method =='POST':
        status='CONFIRMED'
        client.messages.create(to="whatsapp:+919100213186", from_="whatsapp:+14155238886", body="Hello"+" "+full_name+" "+"Your travel from "+" "+source_dt+" "
                               +"to"+" "+destination_dt+" "+"has"+" "+status+" on"+" "+date)
        return render_template('user_registration.html',var=full_name,var1=email_id,var2=id_proof,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,
                               var7=phone_number,var8=date,var9=status)
    else:
        status='Not Confirmed'
        client.messages.create(to="whatsapp:+919100213186", from_="whatsapp:+14155238886",
                               body="Hello" + " " + full_name + " " + "Your travel from " + " " + source_dt + " "
                                    + "to" + " " + destination_dt + " " + "has" + " " + status + " on" + " " + date)
        return render_template('user_registration.html',var=full_name,var1=email_id,var2=id_proof,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,
                               var7=phone_number,var8=date,var9=status)

if __name__ == "__main__":
    app.run(port=9000,debug=True)

