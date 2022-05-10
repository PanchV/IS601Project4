import pytest
from werkzeug.security import generate_password_hash
from app import db
from app.db.models import User, Transaction

TEST_EMAIL = 'panchpandu11@gmail.com'
TEST_PASSWORD = 'password'
TEST_HASH = generate_password_hash(TEST_PASSWORD)

#27
@pytest.fixture()
def _add_transaction(test_user):
    """ add a transaction """
    assert db.session.query(Transaction).count() == 0

    transactions = []
    transactions.append(Transaction(4, TransactionType.CREDIT))
    transactions.append( Transaction(-2, TransactionType.DEBIT) )
    transactions.append( Transaction(-6, TransactionType.DEBIT) )
    transactions.append( Transaction(9, TransactionType.CREDIT) )
    transactions.append( Transaction(-3, TransactionType.DEBIT) )
    transactions.append( Transaction(-2, TransactionType.DEBIT) )

    test_user.transactions += transactions
    db.session.commit()