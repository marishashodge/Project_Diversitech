"""Models and database functions for DiversiTech Poject."""

from flask_sqlalchemy import SQL SQLAlchemy

db = SQLAlchemy


##############################################################################
# Model definitions

class Company(db.Model):
    """Company list."""

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    number_of_employees = db.Column(db.Integer, nullable=True)
    report_date = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Show info about company."""

        return "<Company company_id=%s email=%s>" % (self.company_id, self.email)


# class Users(db.Model):
#     """Users who would like to rate a company."""

#     __tablename__ = "users"

#     user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name = db.Column(db.Integer, nullable=True, default="Anonymous")
#     email = db.Column(db.String(100), nullable=True)
#     password = db.Column(db.String(64), nullable=True)
#     company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
#     employer_status = db.Column(db.String(64))
#     rating = db.Column(db.Integer)
#     pros = db.String(db.String(800))
#     cons = db.String(db.String(800))

#     def __repr__(self):
#         """Show info about user"""

#         return "<User user_id=%s email=%s>" % (self.user_id, self.email)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."








