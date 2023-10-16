from urllib.parse import urljoin
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

def get_abs_url(url):
    return urljoin(request.url_root, url)

class events(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    title = db.Column("title", db.String(100))
    date = db.Column("date", db.String(50))
    description = db.Column("description", db.String(1000))

    def __init__(self, name, title, date, description):
        self.name = name
        self.title = title
        self.date = date
        self.description = description
        
@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html", values=events.query.all())

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':

        name = request.form["nm"]
        title = request.form["ttl"]
        date = request.form["dt"]
        description = request.form["descr"]

        event = events(name, title, date, description)
        db.session.add(event)
        db.session.commit()

        return redirect("/")
    
    else:
        return render_template("form.html")
    
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


