import janus as js

class MyPlugin(js.Plugin):
    name = 'janus.plugin.mimic'

    def sup(self, greets):
        self.send_message({'wat': greets})


ec2 = "18.235.63.230"

ext= "/janus"

ws_server = "ws://" + ec2 + ":8188/"
http_server = "http://" + ec2 + ":8088" + ext
servers= [ws_server, http_server]

server = servers[1]
print(server)
my_plugin = MyPlugin()


print("New Session")
session = js.Session(server, secret='mimicMele')
session.register_plugin(my_plugin)


print("Keep session alive")
session_ka = js.KeepAlive(session)
session_ka.daemon = True
session_ka.start()


print("send message")
my_plugin.sup('dawg')