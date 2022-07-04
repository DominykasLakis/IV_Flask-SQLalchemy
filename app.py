from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from funkcijos import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///duomenys.sqlite'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Skaiciuokle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column(db.String(20))
    pajamos = db.Column(db.Float(20))
    data = db.Column(db.Date)

    def __init__(self, vardas, pajamos, data):
        self.data = data
        self.vardas = vardas
        self.pajamos = pajamos


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "Neteisingas slaptažodis"
        else:
            return redirect(url_for('show_all'))
    return render_template('login.html', error=error)


@app.route('/pagrindinis')
def show_all():
    return render_template('pagrindinis.html', skaiciuokle=Skaiciuokle.query.all(), visa=visa_suma(),
                           saugus=saugus_balansas(), atideta=atideta_mokesciams())


@app.route('/naujas2', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['vardas'] or not request.form['pajamos'] or not request.form['data']:
            flash('Prašome užpildyti visus langelius', 'error')
        else:
            ideti = Skaiciuokle(request.form['vardas'], request.form['pajamos'],
                                datetime.strptime(request.form['data'], '%Y-%m-%d'))
            db.session.add(ideti)
            db.session.commit()
            flash('Sėkmingai pridėta!')
            return redirect(url_for('show_all'))
    return render_template('naujas2.html', skaiciuokle=Skaiciuokle.query.all(), visa=visa_suma(),
                           saugus=saugus_balansas(), atideta=atideta_mokesciams())


@app.route('/<int:id>', methods=['POST'])
def delete(id):
    id = Skaiciuokle.query.get(id)
    db.session.delete(id)
    db.session.commit()
    flash('Įrašas ištrintas')
    return redirect(url_for('show_all'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)