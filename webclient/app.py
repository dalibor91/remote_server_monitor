#!/usr/bin/env python
import flask, sys, os, time, helpers, json


# set the project root directory as the static folder, you can set others.
app = flask.Flask(__name__, static_url_path='/static')

#check if servers file is present
SERVERS_FILE = "%s/servers.ini" % app.root_path

if not os.path.isfile(SERVERS_FILE):
    helpers.log("servers.ini not found", "error")
    sys.exit(1);


SERVERS = helpers.read_servers_file(SERVERS_FILE)

#home
@app.route('/')
def index():
    return flask.render_template('home.html', servers=SERVERS)

#dashboard where charts will be shown
@app.route('/dashboard/<server>')
def dashboard(server):
    if server not in SERVERS:
        return 'Not found'
    return flask.render_template('index.html', server=server, server_data=SERVERS[server])


#page for SSE connections
#where we can pool information
@app.route('/get-<server>/<service>/<pooltime>')
def service(server, service,pooltime):
    if server not in SERVERS:
        return 'Not found'

    srv = SERVERS[server]
    
    pooltime = int(pooltime) if int(pooltime) >= 1 else 1
    def _loop(s, sec, timeout, counter=1):
        s = helpers.SockConnect(srv)
        yield " "*1024
        while True:
            yield helpers.encodeSSE(service, s.pool(service))
            time.sleep(sec)
            counter += 1
            if counter >= timeout:
                break

    res = flask.Response(_loop(service, pooltime, 5), mimetype="text/event-stream")
    res.headers['Transfer-Encoding'] = 'chunked'
    res.headers['Content-Type'] = 'text/event-stream'
    return res

#page where we can ajax informations
@app.route('/once-<server>/<service>')
def once(server, service):
    res = flask.Response(json.dumps({ "error": "unable to fetch"}))
    if server not in SERVERS:
        res.headers['Content-Type'] = 'application/json';
        return res

    s = helpers.SockConnect(SERVERS[server])
    response = s.pool(service)
    s.close()
    res = flask.Response(response)

    res.headers['Content-Type'] = 'application/json';
    return res


data = {
    "host": '0.0.0.0',
    "port": 8888,
    "threaded": True
}

_next=None
_next = None
for i in sys.argv[1:]:
    if _next is not None:
	data[_next] = i
	_next = None
	continue
    if i == '-h':
	_next = 'host'
    elif i == '-p':
	_next = 'port'

data['port'] = int(data['port'])

if __name__ == "__main__":
    app.run(**data)
