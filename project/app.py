import hashlib
import os
import cherrypy
import sqlite3 as sql

baseDir = os.path.abspath(os.path.dirname(__file__))

config = {
    "/": {"tools.staticdir.root": baseDir},

    "/html": {"tools.staticdir.on": True, "tools.staticdir.dir": "html"},

    "/js": {"tools.staticdir.on": True, "tools.staticdir.dir": "js"},

    "/css": {"tools.staticdir.on": True, "tools.staticdir.dir": "css"},

    "/images": {"tools.staticdir.on": True, "tools.staticdir.dir": "images"},

    "/uploads": {"tools.staticdir.on": True, "tools.staticdir.dir": "uploads"},
}


class Root(object):
    def __init__(self):
        self.actions = Actions()

    @cherrypy.expose
    def index(self):
        self.actions = Actions()
        cherrypy.response.headers['Content-Type'] = 'text/html'
        return open("html/index.html")

    @cherrypy.expose
    def main(self):
        return open("html/main.html")

    @cherrypy.expose
    def upload(self, myFile, author):
        db = sql.connect('database.db')
        ext = os.path.splitext(myFile.filename)[1]

        hasher = hashlib.sha256()
        while True:
            data = myFile.file.read(8192)
            if not data:
                break
            hasher.update(data)
        hash_value = hasher.hexdigest()

        filename = os.path.join("uploads", hash_value + ext)

        with open(filename, "wb") as f:
            while True:
                data = myFile.file.read(8192)
                if not data:
                    break
                f.write(data)

        db.execute('INSERT INTO images(name, author, path) VALUES (?, ?, ?)', (hash_value, author, filename))
        db.commit()
        db.close()

        return "Upload successful!"


class Actions(object):
    def __init__(self):
        self.logged_user = None

    @cherrypy.expose
    def do_login(self, username, password):
        db = sql.connect('database.db')
        cherrypy.tree.mount(cherrypy, '/index')
        cherrypy.log("Login attempt from " + username)

        if str(username).count('@') > 0:
            result = db.execute('SELECT * FROM users WHERE email=? AND password=?', (username, password))
        else:
            result = db.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))

        if result.fetchone():
            self.logged_user = db.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
            return open("html/confirmations/login_successful.html")
        else:
            return open("html/confirmations/login_failed.html")

    @cherrypy.expose
    def do_register(self, name, username, email, password, confirm_password):
        if password != confirm_password:
            return "Passwords do not match!"

        db = sql.connect('database.db')
        cherrypy.tree.mount(cherrypy, '/index')
        cherrypy.log("Registration attempt from " + username)

        result = db.execute('SELECT * FROM users WHERE username=? OR email=?', (username, email))
        if result.fetchone():
            return open("html/confirmations/login_failed.html")
        else:
            db.execute('INSERT INTO users(name, username, email, password) VALUES (?, ?, ?, ?)', (name, username, email, password))
            db.commit()
            self.logged_user = db.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
            db.close()
            return open("html/confirmations/login_successful.html")


if __name__ == "__main__":
    cherrypy.quickstart(Root(), "/", config)
