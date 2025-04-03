from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ContractForm(FlaskForm):
    template = SelectField('Contract Template', 
                         choices=[
                             ('employment', 'Employment Contract'),
                             ('nda', 'Non-Disclosure Agreement'),
                             ('service', 'Service Agreement')
                         ],
                         validators=[DataRequired()])
    
    party_one_name = StringField('First Party Name', 
                               validators=[DataRequired(), Length(max=100)],
                               render_kw={"placeholder": "e.g., Company ABC Inc."})
    
    party_one_address = TextAreaField('First Party Address', 
                                    validators=[DataRequired()],
                                    render_kw={"placeholder": "Full address including city, state, and zip code"})
    
    party_two_name = StringField('Second Party Name', 
                               validators=[DataRequired(), Length(max=100)],
                               render_kw={"placeholder": "e.g., John Doe"})
    
    party_two_address = TextAreaField('Second Party Address', 
                                    validators=[DataRequired()],
                                    render_kw={"placeholder": "Full address including city, state, and zip code"})
    
    effective_date = DateField('Effective Date', 
                             validators=[DataRequired()],
                             format='%Y-%m-%d')
    
    contract_duration = StringField('Contract Duration', 
                                  validators=[DataRequired()],
                                  render_kw={"placeholder": "e.g., 12 months, 1 year, etc."})
    
    payment_terms = TextAreaField('Payment Terms', 
                                validators=[DataRequired()],
                                render_kw={"placeholder": "Detailed payment terms including amount, schedule, and method"})
    
    scope_of_work = TextAreaField('Scope of Work / Services', 
                                validators=[DataRequired()],
                                render_kw={"placeholder": "Detailed description of work, responsibilities, deliverables, etc."})
    
    additional_terms = TextAreaField('Additional Terms and Conditions', 
                                   validators=[Optional()],
                                   render_kw={"placeholder": "Any additional terms or special conditions (optional)"})
    
    submit = SubmitField('Generate Contract')
