from math import pi, sin, cos, atan2, radians, sqrt
from os.path import isfile
from socket import gethostname
from sqlite3 import connect
from flask import Flask, request, g, url_for
from contextlib import closing

app = Flask(__name__)
app.config['DATABASE'] = '/tmp/vpns'

def connect_db():
    return connect(app.config['DATABASE'])

def init_db(schema):
    with closing(connect_db()) as db:
        with app.open_resource(schema, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def isnumber(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

@app.before_request
def before_request():
    """
    Opens db connection before request is processed
    """
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """
    Closes db connection after request is complete
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def listvpns():
    """
    Lists VPNs by distance from given coordinates
    """
    error = None
    if 'lng' not in request.args or not isnumber(request.args['lng']):
        error = 'Invalid longitude. '
    elif 'lat' not in request.args or not isnumber(request.args['lat']):
        error = 'Invalid latitude. '
    
    if error:
        return error+'Desired url format: '+gethostname()+':5000/?lng=&ltlng&gt&lat=&ltlat&gt'

    else:
        cur = g.db.execute('SELECT * FROM vpns')
        vpns =  [[str(row[0]),row[1],row[2]] for row in cur.fetchall()]
        
        # Calculate the distance to each vpn
        for vpn in vpns:
            vpnlng = vpn[1]
            vpnlat = vpn[2]
            phi1 = radians(float(request.args['lat']))
            phi2 = radians(vpnlat)
            deltaphi = radians(vpnlat-float(request.args['lat']))
            deltalambda = radians(vpnlng-float(request.args['lng']))

            R = 3959 # radius of the earth
            a = pow(sin(deltaphi/2),2) + cos(phi1) * cos(phi2) * pow(sin(deltalambda/2),2)
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R*c
            
            vpn.append(distance)

        vpn_output = ''
        for vpn in sorted(vpns, key=lambda vpn: vpn[3]):
            vpn_output += vpn[0]+'<br>'

        return vpn_output
        
@app.route('/addvpn')
def addvpn():
    """
    Adds a VPN to the database
    """
    error = None
    if 'name' not in request.args:
        error = 'Name of VPN not found in query. '
    elif 'lng' not in request.args or not isnumber(request.args['lng']):
        error = 'Invalid longitude. '
    elif 'lat' not in request.args or not isnumber(request.args['lat']):
        error = 'Invalid latitude. '
    
    if error:
        return error+'Desired url format: '+gethostname()+':5000/addvpn?name=&ltname&gt&lng=&ltlng&gt&lat=&ltlat&gt'
    else:
        g.db.execute("INSERT OR REPLACE INTO vpns ('name','lng','lat') VALUES (?,?,?)",
                     [request.args['name'], request.args['lng'], request.args['lat']])
        g.db.commit()
        return "Added vpn: "+','.join([request.args['name'],request.args['lng'],request.args['lat']])

@app.route('/delvpn')
def delvpn():
    """
    Deletes a VPN from the database
    """
    error = None
    if 'name' not in request.args:
        return 'Name of VPN not found in query. Desired url format: '+gethostname()+':5000/delvpn?name=&ltname&gt'
        
    else:
        cur = g.db.execute('SELECT name FROM vpns WHERE name == ?', [request.args['name']])
        if len(cur.fetchall()) == 0:
            return 'No such vpn: '+request.args['name']
            
        g.db.execute('DELETE FROM vpns WHERE name == ?', [request.args['name']])
        g.db.commit()
        return 'Deleted vpn: '+request.args['name']
                           

    
if __name__ == '__main__':
    if not isfile(app.config['DATABASE']):
        init_db('schema.sql')
    
    app.run(host='0.0.0.0')
