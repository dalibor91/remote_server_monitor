#!/usr/bin/env python
import sys
import os
import hashlib


class User:
	def __init__(self, user, passwd="", ip='*'):
		self.setUser(user).setPass(passwd).setIp(ip)

	def setIp(self, ip):
		self.ip = ip
		return self

	def setUser(self, user):
		self.user = user
		return self

	def setPass(self, passwd):
		self.passwd = hashlib.sha224(passwd).hexdigest()
		return self

	def getIp(self):
		return self.ip

	def getUser(self):
		return self.user

	def getPass(self):
		return self.passwd

	def update(self, _file):
		lines = []
		with open(_file, "r") as f:
			for line in f.readlines():
				try:
					uname = "%s:" % self.getUser()
					if line.index(uname) == 0:
						lines.append("%s:%s:%s\n" % (self.getUser(), self.getPass(), self.getIp()))
				except:
					lines.append(line)
		try:
			open(_file, 'w').write(''.join(lines))
		except:
			raise Exception("Unable to write to %s" % _file)
		return True

	def delete(self, _file):
		try:
			lines = []
			with open(_file, "r") as f:
				for line in f.readlines():
					try:
						uname = "%s:" % self.getUser()
						if line.strip().index(uname) is not 0:
							lines.append(line)
					except:
						lines.append(line)
			open(_file, 'w').write(''.join(lines))
			return True
		except Exception, s:
			raise Exception("Unable to read or write %s" % _file)
		return False

	def save(self, _file):
		try:
			open(_file, "a").write("%s:%s:%s\n" % (self.getUser(), self.getPass(), self.getIp()))
		 	return True
		except:
			raise Exception("Unable to write to %s" % _file)
		return False

def _input(text, default=None, required=False):
	print(text)
	inpt = raw_input()

	if inpt == '':
		if required :
			return _input(text, default, required)
		return default
	return inpt

def _addUser(f):
	u = User(_input("Enter Username", None, True), _input("Enter Password", None, True), _input("Enter IP", '*'))
	u.save(f)

def _updateUser(f):
	u = User(_input("Enter Username", None, True), _input("Enter Password", None, True), _input("Enter IP", '*'))
	u.update(f)

def _deleteUser(f):
	u = User(_input("Enter Username", None, True))
	u.delete(f)
	
def _loadUser(fl, user):
	with open(fl, "r") as f:
		for line in f.readlines():
			try:
				uname = "%s:" % user
				if line.index(uname) == 0:
					u = User(user)
					
					data = line.split(':')
					if len(data) == 3:
						u.passwd = data[1]
						u.ip = data[2]
			except:
				continue
	return None


if __name__ == '__main__':
	if (len(sys.argv) < 2) or not((sys.argv[1] != 'add') or (sys.argv[1] != 'remove') or (sys.argv[1] != 'update')):
		print("""
	Manage users to database
		users.py (add|remove|update) [-f file_with_users]
	""". strip());
		sys.exit(0)

	cmd = sys.argv[1]

	data = {
		"db": "%s/.pysock.db" % os.path.expanduser("~")
	}

	_next = None
	for i in sys.argv[1:]:
		if _next is not None:
			data[_next] = i
			_next = None
			continue
		if i == '-f':
			_next = 'db'


	if cmd == 'add':
		_addUser(data['db'])
	elif cmd == 'remove':
		_deleteUser(data['db'])
	elif cmd == 'update':
		_updateUser(data['db'])



sys.exit(0)
