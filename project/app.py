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
    @cherrypy.expose
    def index(self):
        return open("html/index.html")

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


if __name__ == "__main__":
    cherrypy.quickstart(Root(), "/", config)
