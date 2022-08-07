from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class OrderType(enum.Enum):
    MARKET = 1
    LIMIT = 2

class UT(enum.Enum):
    M5 = 1
    M15 = 2
    M30 = 3
    H1 = 4
    H2 = 5
    H4 = 6
    D1 = 7
    W1 = 8
    MH1 = 9

class SLType(enum.Enum):
    TP1 = 1
    TP2 = 2
    TP3 = 3
    FIXED = 4


class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pair = db.Column(db.String(10), nullable=False)
    order_type = db.Column(db.Enum(OrderType), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    initial_price = db.Column(db.Float, nullable=False)
    tp1_price = db.Column(db.Float, nullable=False)
    tp1_percent = db.Column(db.Float, nullable=False)
    tp2_price = db.Column(db.Float, nullable=False)
    tp2_percent = db.Column(db.Float, nullable=False)
    tp3_price = db.Column(db.Float, nullable=False)
    tp3_percent = db.Column(db.Float, nullable=False)
    sl_price = db.Column(db.Float, nullable=False)
    sl_ut = db.Column(db.Enum(UT))
    sl_be = db.Column(db.Enum(SLType), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Scenario {self.id}>'

@app.route('/update/<int:id>')
def update(id):
    print(f'update {id=}')
    return redirect('/')

@app.route('/close/<int:id>')
def close(id):
    print(f'close {id=}')
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.form)
        pair = request.form['pair']
        order_type = request.form['order_type']
        amount = request.form['amount']
        initial_price = request.form['initial_price']
        tp1_price = request.form['tp1_price']
        tp1_percent = request.form['tp1_percent']
        tp2_price = request.form['tp2_price']
        tp2_percent = request.form['tp2_percent']
        tp3_price = request.form['tp3_price']
        tp3_percent = request.form['tp3_percent']
        sl_price = request.form['sl_price']
        sl_ut = request.form['sl_ut']
        sl_be = SLType.TP1 if request.form.get('sl_be', False) else SLType.FIXED
        

        new_scenario = Scenario(
            pair = pair,
            order_type = order_type,
            amount = amount,
            initial_price = initial_price,
            tp1_price = tp1_price,
            tp1_percent = tp1_percent,
            tp2_price = tp2_price,
            tp2_percent = tp2_percent,
            tp3_price = tp3_price,
            tp3_percent = tp3_percent,
            sl_price = sl_price,
            sl_ut = sl_ut,
            sl_be = sl_be
        )

        #try:
        db.session.add(new_scenario)
        db.session.commit()
        return redirect('/')
        #except:
        #    return 'There was an issue adding your new scenario !'

    else:
        scenarios = Scenario.query.order_by(Scenario.date_created).all()
        print(scenarios)
        return render_template('index.html', scenarios=scenarios)

if __name__ == '__main__':
    app.run(debug=True)