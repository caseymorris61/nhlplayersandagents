from flask import Flask, render_template, request, json, g
import sqlite3

#initializations
app = Flask(__name__)

# Path for Heroku
DATABASE='/app/app/static/agentdatabase'

# Path for local
# DATABASE='static/agentdatabase'

@app.route("/")
@app.route("/index")
def main():
    playersInfo = []
    playerquery = "select players.name, players.agentID, players.salary, certified_agents.name from players join certified_agents on players.agentID=certified_agents.agentID"
    c = get_db().cursor()
    c.execute(playerquery)
    players = c.fetchall()
    for row in players:
        name = row[0]
        agentID = row[1]
        agentName = row[3]
        try:
            salaryVal = int(row[2].strip('"').strip('$').replace(',',"").strip())
        except ValueError :
            salaryVal = 0

        salary = '${:,.2f}'.format(salaryVal)

        d = [name,agentID,salary,agentName,salaryVal]
        playersInfo.append(d)


    playersInfo.sort(key=lambda x: x[4],reverse=True)

    return render_template('index.html', players=playersInfo)

@app.route('/agents/<variable>', methods=['GET'])
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


    playersInfo = []
    playerquery = "select name, salary from players where agentID = ?"
    c = get_db().cursor()
    c.execute(playerquery, (str(variable),))
    players = c.fetchall()
    for row in players:
        playername = row[0]
        try:
            salaryVal = int(row[1].strip('"').strip('$').replace(',',"").strip())
        except ValueError :
            salaryVal = 0

        salary = '${:,.2f}'.format(salaryVal)

        d = [playername,salary,salaryVal]
        playersInfo.append(d)


    playersInfo.sort(key=lambda x: x[2],reverse=True)
    numPlayers = len(playersInfo)

    return render_template('agent.html', name=name,address=address,agency=agency,email=email,phone=phone,mobile=mobile,url_ext=url_ext,players=playersInfo,numPlayers=numPlayers)

@app.route("/agents")
def agents():
    agentsquery = "select agentID, name, email, phone, mobile from certified_agents"
    c = get_db().cursor()
    c.execute( agentsquery)
    agentsRes = c.fetchall()

    agents = []
    for row in agentsRes:
        aid = str(row[0])
        name = row[1]
        email = row[2]
        phone = row[3]
        mobile = row[4]

        a = [aid,name,email,phone,mobile]
        agents.append(a)

    return render_template('agents.html',agents=agents)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def getApp():
    return app

if __name__ == "__main__":
    app.run()