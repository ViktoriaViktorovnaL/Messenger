import server
import Config_server

host = Config_server.your_host
port = Config_server.your_port

server.app.run(host, port, debug=True, use_reloader=False)
