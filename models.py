from app import db
from datetime import datetime

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(100), nullable=False)
    party_one_name = db.Column(db.String(100), nullable=False)
    party_one_address = db.Column(db.Text, nullable=False)
    party_two_name = db.Column(db.String(100), nullable=False)
    party_two_address = db.Column(db.Text, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    contract_duration = db.Column(db.String(100), nullable=False)
    payment_terms = db.Column(db.Text, nullable=False)
    scope_of_work = db.Column(db.Text, nullable=False)
    additional_terms = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Contract {self.id}: {self.party_one_name} - {self.party_two_name}>"
