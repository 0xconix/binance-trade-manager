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

def get_params(request):
    params = {}
    params['pair'] = request.form['pair']
    params['order_type'] = request.form['order_type']
    params['amount'] = request.form['amount']
    params['initial_price'] = request.form['initial_price']
    params['tp1_price'] = request.form['tp1_price']
    params['tp1_percent'] = request.form['tp1_percent']
    params['tp2_price'] = request.form['tp2_price']
    params['tp2_percent'] = request.form['tp2_percent']
    params['tp3_price'] = request.form['tp3_price']
    params['tp3_percent'] = request.form['tp3_percent']
    params['sl_price'] = request.form['sl_price']
    params['sl_ut'] = request.form['sl_ut']
    params['sl_be'] = SLType.TP1 if request.form.get('sl_be', False) else SLType.FIXED
    
    return params

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    scenario = Scenario.query.get_or_404(id)

    if request.method == 'POST':
        params = get_params(request)
        scenario.pair = params['pair']
        scenario.order_type = params['order_type']
        scenario.amount = params['amount']
        scenario.initial_price = params['initial_price']
        scenario.tp1_price = params['tp1_price']
        scenario.tp1_percent = params['tp1_percent']
        scenario.tp2_price = params['tp2_price']
        scenario.tp2_percent = params['tp2_percent']
        scenario.tp3_price = params['tp3_price']
        scenario.tp3_percent = params['tp3_percent']
        scenario.sl_price = params['sl_price']
        scenario.sl_ut = params['sl_ut']
        scenario.sl_be = params['sl_be']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your scenario !'

    else:
        scenarios = Scenario.query.order_by(Scenario.date_created).all()
        return render_template('update.html', scenarios=scenarios, scenario=scenario)

@app.route('/close/<int:id>')
def close(id):
    scenario_to_close = Scenario.query.get_or_404(id)

    try:
        db.session.delete(scenario_to_close)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that scenario'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_scenario = Scenario(**get_params(request))

        try:
            db.session.add(new_scenario)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your new scenario !'

    else:
        scenarios = Scenario.query.order_by(Scenario.date_created).all()
        print(scenarios)
        return render_template('index.html', scenarios=scenarios)

if __name__ == '__main__':
    app.run(debug=True)