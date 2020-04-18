from flask import Flask, render_template, request, json, g
import sqlite3

#initializations
app = Flask(__name__)

DATABASE='/app/app/static/agentdatabase'

@app.route("/")
@app.route("/index")
def main():
    playersInfo = []
    playerquery = "select name, agentID, salary from players"
    c = get_db().cursor()
    c.execute(playerquery)
    players = c.fetchall()
    for row in players:
        name = row[0]
        agentID = row[1]
        try:
            salaryVal = int(row[2].strip('"').strip('$').replace(',',"").strip())
        except ValueError :
            salaryVal = 0

        salary = '${:,.2f}'.format(salaryVal)

        d = [name,agentID,salary,salaryVal]
        playersInfo.append(d)


    playersInfo.sort(key=lambda x: x[3],reverse=True)

    return render_template('index.html', players=playersInfo)

@app.route('/agent/<variable>', methods=['GET'])
def get_agent(variable):

    agentquery = "select name, address, agency, email, phone, mobile, url_ext from certified_agents where agentID = ?"
    c = get_db().cursor()
    c.execute( agentquery, (str(variable),) )
    agent = c.fetchone()

    name = agent[0]
    address = agent[1]
    agency = agent[2]
    email = agent[3]
    phone = agent[4]
    mobile = agent[5]
    url_ext = agent[6]
    return render_template('agent.html', name=name,address=address,agency=agency,email=email,phone=phone,mobile=mobile,url_ext=url_ext)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def getApp():
    return app

if __name__ == "__main__":
    app.run()