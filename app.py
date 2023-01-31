from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Item %r' %self.id

@app.route('/')
def index():
    items = Item.query.order_by().all()
    return render_template('index.html', items=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/kurs')
def kurs():
    return render_template('kurs.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        amount = request.form['amount']
        item = Item(title=title, price=price, amount=amount)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Опачки! Произошла какая-то вредная ошибка!"
    else:
        return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()