"""Utility file to seed diversity database."""

from sqlalchemy import func
from model import Company

from model import connect_to_db, db
from server import app


def load_companies():
    """Load companies into database."""

    print "Companies"

    Company.query.delete()

    for row in open("Diversitech-Table_20160209.tsv"):
        row = row.rstrip()
        print row
