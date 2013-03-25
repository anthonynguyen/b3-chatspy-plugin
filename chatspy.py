# Chatspy Plugin for B3
# By clearskies (Anthony Nguyen)
# GPL licensed

import b3
import b3.events
import b3.plugin

__version__ = "0.2"
__author__ = "clearskies (Anthony Nguyen)"

class ChatspyPlugin(b3.plugin.Plugin):
	requiresConfigFile = False
	_listeners = []
	_teams = {1: "^3SPEC", 2: "^1RED", 3: "^4BLUE"}

	def onStartup(self):
		self._admin = self.console.getPlugin("admin")
		self._admin.registerCommand(self, "chatspy", 100, self.cmd_chatspy, "spy")

		self.registerEvent(b3.events.EVT_CLIENT_DISCONNECT)
		self.registerEvent(b3.events.EVT_CLIENT_PRIVATE_SAY)
		self.registerEvent(b3.events.EVT_CLIENT_TEAM_SAY)

	def onEvent(self, event):
		if event.type == b3.events.EVT_CLIENT_TEAM_SAY:
			for listener in self._listeners:
				if event.client.team != listener.team:
					listener.message("^7[{0}^7] {1}: {2}".format(self._teams[event.client.team], event.client.exactName, event.data))
			print self._listeners
		elif event.type == b3.events.EVT_PRIVATE_SAY:
			for listener in self._listeners:
				if event.client != listener and event.target != listener:
					listener.message("^7[{0}^7{1}^7]->[{2}^7{3}^7]: {4}".format(self._teams[event.client.team][:2], event.client.exactName, self._teams[event.target.team][:2], event.target.exactName, event.data))
		elif event.type == b3.events.EVT_CLIENT_DISCONNECT:
			if event.client in self._listeners: self._listeners.remove(event.client)

	def cmd_chatspy(self, data, client, cmd = None):
		"""
		<on|off|> - turns the chat spy on or off, or gives its status
		"""
		if not data:
			if client in self._listeners:
				client.message("^7The Chat Spy is [^2ON^7]")
			else:
				client.message("^7The Chat Spy is [^1OFF^7]")
		if data == "on":
			if client not in self._listeners:
				self._listeners.append(client)
				client.message("^7Spy: [^2ON^7]")
			else:
				client.message("You are already spying on chats!")
		if data == "off":
			if client in self._listeners:
				self._listeners.remove(client)
				client.message("^7Spy: [^1OFF^7]")
			else:
				client.message("You are not spying on chats!")

if __name__ == "__main__":
	from b3.fake import fakeConsole, joe, moderator, superadmin
	plugin = ChatspyPlugin(fakeConsole)
	plugin.onStartup()
	superadmin.connects(cid = 0)
	superadmin.team = 1
	joe.connects(cid = 1)
	joe.team = 2
	moderator.connects(cid = 2)
	moderator.team = 3
	superadmin.says("!spy on")
	joe.says2team("haha")
	superadmin.says("!spy on")
	superadmin.says("!help spy")
	joe.says2team("admin is a big fat noob")
	superadmin.disconnects()