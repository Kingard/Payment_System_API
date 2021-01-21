from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import datetime

# Initialize app
app = Flask(__name__)
basedirectory = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedirectory,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize database
db = SQLAlchemy(app)
# Initialize marshmallow
ma = Marshmallow(app)

# Payment class
class Payment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    CreditCardNumber = db.Column(db.Integer)
    CardHolder = db.Column(db.String(100))
    ExpirationDate = db.Column(db.String)
    SecurityCode = db.Column(db.String(3))
    Amount = db.Column(db.Float(7))
    PaymentProvider = db.Column(db.String(20))

    def __init__(self,CreditCardNumber,CardHolder,ExpirationDate,SecurityCode,Amount,PaymentProvider):
        self.CreditCardNumber = CreditCardNumber
        self.CardHolder = CardHolder
        self.ExpirationDate = ExpirationDate
        self.SecurityCode = SecurityCode
        self.Amount = Amount
        self.PaymentProvider = PaymentProvider

# Client Schema 
class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id','Credit Card Number','Card holder','Expiration date','Security code','Amount','Payment Provider')

# Initialize schema
client_schema = ClientSchema()   # could include strict = True
clients_schema = ClientSchema(many=True)

# Create a client entry (make payment)
@app.route('/payment',methods=['POST'])
def make_payment():
    CreditCardNumber = request.json['CreditCardNumber']
    CardHolder = request.json['Cardholder']
    ExpirationDate = request.json['ExpirationDate']
    SecurityCode = request.json['SecurityCode']
    Amount = request.json['Amount']
    PaymentProvider = ''


    if Amount <= 20:
        PaymentProvider = 'CheapPaymentGateway'
    if Amount > 20 and Amount <= 500:
        PaymentProvider = 'ExpensivePaymentGateway'
    if Amount > 500:
        PaymentProvider = 'PremiumPaymentGateway'

    new_payment = Payment(CreditCardNumber,CardHolder,ExpirationDate,SecurityCode,Amount)
    db.session.add(new_payment)
    db.session.commit()
    return client_schema.jsonify(new_payment)
    






# Run server
if __name__ == '__main__':
    app.run(debug=True)
