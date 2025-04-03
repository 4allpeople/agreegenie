import os
import logging
from flask import Flask, render_template, redirect, url_for, flash, session, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import weasyprint
from io import BytesIO
import jinja2

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
from datetime import datetime
from flask_wtf import CSRFProtect

csrf = CSRFProtect(app)


@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///contracts.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

# Create a custom Jinja2 environment for contract templates
contract_template_loader = jinja2.FileSystemLoader('contract_templates')
contract_template_env = jinja2.Environment(loader=contract_template_loader)

from forms import ContractForm
from models import Contract

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_contract', methods=['GET', 'POST'])
def create_contract():
    form = ContractForm()
    
    if form.validate_on_submit():
        contract_data = {
            'template_name': form.template.data,
            'party_one_name': form.party_one_name.data,
            'party_one_address': form.party_one_address.data,
            'party_two_name': form.party_two_name.data,
            'party_two_address': form.party_two_address.data,
            'effective_date': form.effective_date.data.isoformat(),
            'contract_duration': form.contract_duration.data,
            'payment_terms': form.payment_terms.data,
            'scope_of_work': form.scope_of_work.data,
            'additional_terms': form.additional_terms.data
        }
        
        # Store contract data in the session for preview
        session['contract_data'] = contract_data
        
        # Save to database
        new_contract = Contract(
            template_name=form.template.data,
            party_one_name=form.party_one_name.data,
            party_one_address=form.party_one_address.data,
            party_two_name=form.party_two_name.data,
            party_two_address=form.party_two_address.data,
            effective_date=form.effective_date.data,
            contract_duration=form.contract_duration.data,
            payment_terms=form.payment_terms.data,
            scope_of_work=form.scope_of_work.data,
            additional_terms=form.additional_terms.data
        )
        db.session.add(new_contract)
        db.session.commit()
        
        session['contract_id'] = new_contract.id
        
        return redirect(url_for('preview_contract'))
    
    return render_template('create_contract.html', form=form)

@app.route('/preview_contract')
def preview_contract():
    contract_data = session.get('contract_data')
    if not contract_data:
        flash('No contract data found. Please create a contract first.', 'error')
        return redirect(url_for('create_contract'))
    
    # Load and render the selected template with contract data
    template_name = contract_data['template_name']
    template_file = f"{template_name}_contract.html"
    try:
        template = contract_template_env.get_template(template_file)
        rendered_contract = template.render(**contract_data)
    except Exception as e:
        app.logger.error(f"Error rendering contract: {str(e)}")
        flash(f'Error rendering contract template: {str(e)}', 'error')
        return redirect(url_for('create_contract'))
    
    return render_template('preview_contract.html', 
                           contract=rendered_contract, 
                           contract_data=contract_data)

@app.route('/download_contract')
def download_contract():
    contract_data = session.get('contract_data')
    if not contract_data:
        flash('No contract data found. Please create a contract first.', 'error')
        return redirect(url_for('create_contract'))
    
    # Render contract HTML
    template_name = contract_data['template_name']
    template_file = f"{template_name}_contract.html"
    
    try:
        template = contract_template_env.get_template(template_file)
        rendered_contract = template.render(**contract_data)
        
        # Create PDF from HTML
        pdf = BytesIO()
        html = weasyprint.HTML(string=rendered_contract)
        html.write_pdf(pdf)
        
        # Rewind the buffer
        pdf.seek(0)
        
        # Create a filename
        filename = f"{template_name}_contract_{contract_data['party_one_name']}_{contract_data['party_two_name']}.pdf"
        filename = filename.replace(" ", "_")
        
        return send_file(
            pdf,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        app.logger.error(f"Error generating PDF: {str(e)}")
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('preview_contract'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
if __name__ == "__main__":
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
