import csv
import os


from flask import Blueprint, render_template, abort, url_for, flash
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app import config
from app.db import db
from app.db.models import Transaction
from app.transactions.forms import csv_upload
from werkzeug.utils import secure_filename, redirect
from calculator import Calculator

transactions = Blueprint('transactions', __name__,
                        template_folder='templates')

calc_obj = Calculator()

@transactions.route('/transactions/<int:page>', methods=['GET'], defaults={"page": 1})
@login_required
def transactions_browse(page):
    page = page
    per_page = 1000
    pagination = Transaction.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_transactions.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@transactions.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transactions_upload():

    form = csv_upload()
    if form.validate_on_submit():
        #log = logging.getLogger("myApp")
        #log1 = logging.getLogger("uploadCsv")
        #log1.info("UPLOADED A NEW FILE")
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(config.Config.UPLOAD_FOLDER, filename)
        form.file.data.save(filepath)
        transaction_list = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                balance = calc_obj.add(int(row["\ufeffAMOUNT"]))
                transaction_list.append(Transaction(row["\ufeffAMOUNT"],row['TYPE'], balance))


        current_user.transactions = transaction_list
        db.session.commit()
        flash('You Uploaded Transactions Successfully!', 'success')
        return redirect(url_for('transactions.transactions_browse'))

    try:
        return render_template('upload_transactions.html', form=form)
    except TemplateNotFound:
        abort(404)