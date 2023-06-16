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
    def about(self):
        return open("html/about.html")

    @cherrypy.expose
    def main(self):
        return open("html/main.html")

    @cherrypy.expose
    def gallery(self):
        return open("html/gallery.html")

    @cherrypy.expose
    def profile(self):
        return open("html/profile.html")

    @cherrypy.expose
    def upload(self):
        return open("html/upload.html")


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
            self.logged_user = db.execute('SELECT username FROM users WHERE email=?', username)
        else:
            result = db.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            self.logged_user = username

        if result.fetchone():
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
            self.logged_user = username
            db.close()
            return open("html/confirmations/login_successful.html")

    @cherrypy.expose
    def upload_image(self, my_file, my_file_name, my_file_author):
        db = sql.connect('database.db')
        fname, ext = os.path.splitext(my_file.filename)[0:2]

        fdata = []
        while True:
            d = my_file.file.read(8192)
            if not d:
                break
            fdata.append(d)

        hasher = hashlib.sha256()
        for d in fdata:
            hasher.update(d)
        hash_value = hasher.hexdigest()

        dirs = os.listdir(".")
        if "uploads" not in dirs:
            os.mkdir("uploads")
        filename = os.path.join("uploads", hash_value + ext)

        with open(filename, "wb") as f:
            for d in fdata:
                f.write(d)

        name = my_file_name if my_file_name else fname
        author = self.logged_user if not my_file_author else my_file_author
        db.execute('INSERT INTO images(name, author, path) VALUES (?, ?, ?)', (name, author, filename))
        db.commit()
        db.close()

        return "Upload successful!"

    @cherrypy.expose
    def load_image(self, image_name):
        db = sql.connect('database.db')
        result = db.execute('SELECT path FROM images WHERE name=?', image_name)
        db.close()
        return open(result.fetchone()[0])


if __name__ == "__main__":
    cherrypy.quickstart(Root(), "/", config)
