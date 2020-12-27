import server
import Config_server
import messenger

host = Config_server.your_host
port = Config_server.your_port

server.app.run(host, port, debug=True, use_reloader=False)

# messenger.window.show()
# messenger.apper.exec_()
