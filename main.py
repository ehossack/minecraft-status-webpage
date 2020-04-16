
from mcstatus import MinecraftServer
from os import getenv
from flask import Flask
from dotenv import load_dotenv

load_dotenv(verbose=True)
app = Flask(__name__)


@app.route('/')
def status():
    serverName = getenv("SERVER_NAME", "Minecraft Server")
    server = MinecraftServer(getOrError("SERVER"), int(getenv("PORT")) if getenv("PORT") else None)
    
    statusString = "<b style='color: red'>Server is down</b>"
    try:
        statusString = getStatusString(server)
    except Exception as e:
        print(e)
        pass

    try:
        statusString += getQueryString(server)
    except Exception as e:
        print(e)
        statusString += "<p>No further information</p>"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8"><style>body {{ font-family: monospace, monospace; }}</style>
        <title>{serverName} Status</title>
    </head>
    <body>
        <h3>{serverName} Status</h3>
        {statusString}
    </body>
    </html>"""

def getStatusString(server):
    status = server.status()

    return f"""
        <p>{status.players.online} players online</p>
        <p>{status.latency}ms latency</p>"""

# 'query' has to be enabled in a servers' server.properties file.
def getQueryString(server):
    query = server.query()
    return f"""
    <p>Online players:
        <ul>{"".join([f"<li>{n}</li>" for n in query.players.names])}</ul>
    </p>"""

def getOrError(variable):
    if not getenv(variable):
        raise Exception(f'Missing environment value for {variable}')
    return getenv(variable)

if __name__ == '__main__':
    app.run()