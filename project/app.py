import hashlib
import json
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
        cherrypy.response.headers['Content-Type'] = 'text/html'

    @cherrypy.expose
    def index(self):
        if len(self.actions.logged_user.keys()) > 0 and self.actions.logged_user[cherrypy.request.headers['USER-AGENT']]:
            return """<body onload="window.location.href='/main'"></body>"""
        return open("html/index.html")

    @cherrypy.expose
    def about(self):
        if len(self.actions.logged_user.keys()) == 0 or not self.actions.logged_user[cherrypy.request.headers['USER-AGENT']]:
            return """<body onload="window.location.href='/'"></body>"""
        return open("html/about.html").read().replace("{{SIDEBAR PROFILE}}", self.actions.get_sidebar_profile())

    @cherrypy.expose
    def main(self):
        if len(self.actions.logged_user.keys()) == 0 or not self.actions.logged_user[cherrypy.request.headers['USER-AGENT']]:
            return """<body onload="window.location.href='/'"></body>"""
        return open("html/main.html").read().replace("{{SIDEBAR PROFILE}}", self.actions.get_sidebar_profile())

    @cherrypy.expose
    def gallery(self):
        if len(self.actions.logged_user.keys()) == 0 or not self.actions.logged_user[cherrypy.request.headers['USER-AGENT']]:
            return """<body onload="window.location.href='/'"></body>"""

        db = sql.connect('database.db')
        gallery = db.execute('SELECT * FROM images').fetchall()
        db.close()

        gallery_html = ""
        for image in gallery:
            gallery_html += """
            <a href="/image?imgid={}">
            <img src="../{}" alt="">
            </a>""".format(image[0], image[4])

        return (open("html/gallery.html").read()
                .replace("{{SIDEBAR PROFILE}}", self.actions.get_sidebar_profile())
                .replace("{{GALLERY}}", gallery_html))

    @cherrypy.expose
    def profile(self):
        if len(self.actions.logged_user.keys()) == 0 or not self.actions.logged_user[cherrypy.request.headers['USER-AGENT']]:
            return """<body onload="window.location.href='/'"></body>"""
        user = self.actions.get_logged_user()
        return (open("html/profile.html").read()
                .replace("{{SETTINGS FORM}}", self.actions.get_settings())
                .replace("{{SIDEBAR PROFILE}}", self.actions.get_sidebar_profile())
                .replace("{{NAME}}", user[1])
                .replace("{{USERNAME}}", user[2])
                .replace("{{EMAIL}}", user[3])
                .replace("{{PHONE}}", user[5] if user[5] else "")
                .replace("{{LOCATION}}", user[7] + "," + user[6] if user[6] and user[7] else "")
                .replace("{{BIO}}", user[8] if user[8] else "")
                .replace("{{PROFILE PICTURE}}", user[9]))

    @cherrypy.expose
    def image(self, imgid):
        if len(self.actions.logged_user.keys()) == 0 or not self.actions.logged_user[cherrypy.request.headers['USER-AGENT']]:
            return """<body onload="window.location.href='/'"></body>"""

        db = sql.connect('database.db')

        # Get image info
        image = db.execute('SELECT * FROM images WHERE id=?', (imgid,)).fetchone()
        image_uploader = image[1]
        image_name = image[2]
        image_author = image[3]
        image_path = image[4]

        # Get votes
        votes = db.execute('SELECT * FROM votes WHERE idimg=?', (imgid,)).fetchall()
        upvotes = 0
        downvotes = 0
        for vote in votes:
            if vote[3] == 1:
                upvotes += 1
            else:
                downvotes += 1

        # Get comments
        comments = db.execute('SELECT * FROM comments WHERE idimg=?', (imgid,)).fetchall()
        comments_html = ""
        for comment in comments:
            comments_html += f"""<h1><b>{comment[3]}</b></h1>
            <p class="comment-content">{comment[4]}</p>
            <h4><i>Commented by {comment[2]} at {comment[5]}</i></h4>
            <hr>"""

        db.close()
        return (open("html/image.html").read()
                .replace("{{SIDEBAR PROFILE}}", self.actions.get_sidebar_profile())
                .replace("{{IMAGE UPLOADER}}", f"{image_uploader}")
                .replace("{{IMAGE NAME}}", f"{image_name} by {image_author}")
                .replace("{{PATH}}", f"{image_path}")
                .replace("{{UPVOTES}}", f"{upvotes}")
                .replace("{{DOWNVOTES}}", f"{downvotes}")
                .replace("{{COMMENTS}}", comments_html))

    @cherrypy.expose
    def upload(self):
        if len(self.actions.logged_user.keys()) == 0 or not self.actions.logged_user[cherrypy.request.headers['USER-AGENT']]:
            return """<body onload="window.location.href='/'"></body>"""
        return open("html/upload.html")


class Actions(object):
    def __init__(self):
        self.logged_user = {}

    @cherrypy.expose
    def get_logged_user(self):
        return self.logged_user[cherrypy.request.headers['USER-AGENT']]

    @cherrypy.expose
    def logout(self):
        self.logged_user[cherrypy.request.headers['USER-AGENT']] = None
        return """<body onload="window.location.href='/'"></body>"""

    def update_logged_user(self, email):
        db = sql.connect('database.db')
        self.logged_user[cherrypy.request.headers['USER-AGENT']] = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        db.close()

    @cherrypy.expose
    def get_sidebar_profile(self):
        return """<img src="uploads/profile-pictures/{}" alt="">
                    <div class="name_job">
                        <div class="name">{}</div>
                    </div>""".format(self.logged_user[cherrypy.request.headers['USER-AGENT']][9], self.logged_user[cherrypy.request.headers['USER-AGENT']][1])

    @cherrypy.expose
    def do_login(self, email, password):
        db = sql.connect('database.db')
        cherrypy.tree.mount(cherrypy, '/index')
        cherrypy.log("Login attempt from " + email)

        user = db.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password)).fetchone()
        db.close()

        if user:
            self.logged_user[cherrypy.request.headers['USER-AGENT']] = user
            return open("html/confirmations/login_successful.html")
        else:
            return open("html/confirmations/login_failed.html")

    @cherrypy.expose
    def do_register(self, username, email, password):
        db = sql.connect('database.db')
        cherrypy.tree.mount(cherrypy, '/index')
        cherrypy.log("Registration attempt from " + username)

        result = db.execute('SELECT * FROM users WHERE username=? OR email=?', (username, email))
        if result.fetchone():
            db.close()
            return open("html/confirmations/login_failed.html")
        else:
            db.execute('INSERT INTO users(name, username, email, password, profile_pic) VALUES (?, ?, ?, ?, ?)',
                       (username, username, email, password, 'default.jpeg'))
            db.commit()
            self.logged_user[cherrypy.request.headers['USER-AGENT']] = db.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password)).fetchone()
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
        author = self.logged_user[cherrypy.request.headers['USER-AGENT']][1] if not my_file_author else my_file_author
        db.execute('INSERT INTO images(username, name, author, path) VALUES (?, ?, ?, ?)',
                   (self.logged_user[cherrypy.request.headers['USER-AGENT']][2], name, author, filename))
        db.commit()
        db.close()

        return "Upload successful!"

    @cherrypy.expose
    def update_settings(self, name, username, email, password, phone, country, city, bio):
        db = sql.connect('database.db')

        if username != self.logged_user[cherrypy.request.headers['USER-AGENT']][2]:
            existing_user = db.execute('SELECT * FROM users WHERE username=?', (username,))
            if existing_user.fetchone():
                return "Username already exists!<br><a href='/profile'>Go back</a>"
        if email != self.logged_user[cherrypy.request.headers['USER-AGENT']][3]:
            existing_email = db.execute('SELECT * FROM users WHERE email=?', (email,))
            if existing_email.fetchone():
                return "Email already registered!<br><a href='/profile'>Go back</a>"
        if password == "":
            password = self.logged_user[cherrypy.request.headers['USER-AGENT']][4]


        db.execute('UPDATE users SET name=?, username=?, email=?, password=?, phone=?, country=?, city=?, bio=?, profile_pic=? WHERE username=?',
            (name, username, email, password, phone, country, city, bio, 'default.jpeg', self.logged_user[cherrypy.request.headers['USER-AGENT']],))
        db.commit()
        db.close()
        self.update_logged_user(email)
        return open("html/confirmations/settings_updated.html")

    @cherrypy.expose
    def get_settings(self):
        result = self.logged_user[cherrypy.request.headers['USER-AGENT']]
        return """<form action="actions/update_settings" method="post" style="margin-left: 10%">
                    <p>Name:</p> <input id="settings-name" name="name" type="text" class="text" placeholder="Name" value="{}">
                    <p>Username:</p> <input id="settings-username" name="username" type="text" class="text" placeholder="User Name" value={} required>
                    <p>Email:</p> <input id="settings-email" name="email" type="email" class="text" placeholder="Email" value={} required>
                    <p>Password:</p> <input id="settings-password" name="password" type="password" class="text" placeholder="Enter Password" value={} required>
                    <p>Phone Number:</p> <input id="settings-phone" name="phone" type="text" class="text" placeholder="Phone Number" value={}>
                    <p>Country:</p> <input id="settings-country" name="country" type="text" class="text" placeholder="Country" value={}>
                    <p>City:</p> <input id="settings-city" name="city" type="text" class="text" placeholder="City" value={}>
                    <p>Bio:</p> <textarea id="settings-bio" name="bio" rows="4" class="bio-text" placeholder="Bio" value={}></textarea>
                    <button type="submit" class="submit-btn">Apply</button>
                </form>
        """.format(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])

    @cherrypy.expose
    def newcomment(self, imageid, comment_title, comment):
        db = sql.connect('database.db')
        user = self.logged_user[cherrypy.request.headers['USER-AGENT']][2]
        db.execute('INSERT INTO comments(idimg, user, title, comment) VALUES (?, ?, ?, ?)', (imageid, user, comment_title, comment))
        db.commit()
        db.close()
        return "Comment added!"

    @cherrypy.expose
    def upvote(self, imageid):
        db = sql.connect('database.db')
        current_votes = db.execute('SELECT * FROM votes WHERE idimg=? AND user=?', (imageid, self.logged_user[cherrypy.request.headers['USER-AGENT']][2])).fetchone()
        if current_votes is None:
            db.execute('INSERT INTO votes(idimg, user, vote) VALUES (?, ?, ?)', (imageid, self.logged_user[cherrypy.request.headers['USER-AGENT']][2], 1))
        else:
            if current_votes[3] == 1:
                return "You have already upvoted this image!"
            else:
                db.execute('UPDATE votes SET vote = 1 WHERE idimg = ? AND user = ?', (imageid, self.logged_user[cherrypy.request.headers['USER-AGENT']][2]))
        db.commit()
        db.close()
        Root().image(imageid)
        return "Upvote added!"

    @cherrypy.expose
    def downvote(self, imageid):
        db = sql.connect('database.db')
        current_votes = db.execute('SELECT * FROM votes WHERE idimg=? AND user=?', (imageid, self.logged_user[cherrypy.request.headers['USER-AGENT']][2])).fetchone()
        if current_votes is None:
            db.execute('INSERT INTO votes(idimg, user, vote) VALUES (?, ?, ?)', (imageid, self.logged_user[cherrypy.request.headers['USER-AGENT']][2], -1))
        else:
            if current_votes[3] == -1:
                return "You have already downvoted this image!"
            else:
                db.execute('UPDATE votes SET vote = -1 WHERE idimg = ? AND user = ?', (imageid, self.logged_user[cherrypy.request.headers['USER-AGENT']][2]))
        db.commit()
        db.close()
        Root().image(imageid)
        return "Downvote added!"

    @cherrypy.expose
    def get_votes(self, imageid):
        db = sql.connect('database.db')
        result = db.execute('SELECT * FROM votes WHERE idimg=?', imageid).fetchall()
        up = 0
        down = 0
        for i in result:
            if i[3] == 1:
                up += 1
            elif i[3] == -1:
                down += 1
        db.close()
        return {'up': up, 'down': down}


if __name__ == "__main__":
    cherrypy.quickstart(Root(), "/", config)
