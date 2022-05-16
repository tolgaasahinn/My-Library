from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS  books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, "
#                "author varchar(250) NOT NULL,subject TEXT NOT NULL, rating FLOAT NOT NULL)")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/tolga/OneDrive/Masaüstü/library-start/books-collection.db'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    subject = db.Column(db.String(250), nullable=False)
    complete = db.Column(db.Boolean)
    rating = db.Column(db.Float)


db.create_all()

all_books = db.session.query(Books).all()

@app.route('/rate_page/<string:id>', methods=["GET","POST"])
def rate_page(id):
    book_change= Books.query.get(id)

    return render_template('rate_page.html',book=book_change)



@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_book = Books(title=f"{request.form.get('Name')}", author=f"{request.form.get('Author')}",
                         subject=f"{request.form.get('subject')}", rating=float(f"{request.form.get('rate')}"),
                         complete=False)
        db.session.add(new_book)
        db.session.commit()
        db.session.query(Books).all()
        return redirect(url_for('home'))
    all_books = db.session.query(Books).all()
    return render_template("add.html", books=all_books)


@app.route('/complete/<string:id>', methods=["GET"])
def complete(id):
    new_book = Books.query.filter_by(id=id).first()
    if not new_book.complete:
        new_book.complete = False
    else:
        new_book.complete = True
    db.session.commit()
    return redirect(url_for("home"))


@app.route('/delete/<string:id>', methods=["GET"])
def delete(id):
    book_to_delete = Books.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/rate', methods=["GET","POST"])
def rate_change():
    if request.method == "POST":
        book_id = request.form["id"]
        book_change_Rate = Books.query.get(book_id)
        book_change_Rate.update.rating = f"{request.form.get('rating')}"
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Books.query.get(book_id)
    return render_template("rate_page.html", book=book_selected)
if __name__ == "__main__":
    app.run(debug=True)
