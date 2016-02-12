"""Models and database functions for DiversiTech Poject."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class Company(db.Model):
    """Company list."""

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    # number_of_employees = db.Column(db.Integer, nullable=True)
    report_date = db.Column(db.String(64))
    female_overall = db.Column(db.Integer)
    male_overall = db.Column(db.Integer)

    def __repr__(self):
        """Show info about company."""

        return "<Company company_id=%s name=%s>" % (self.company_id, self.name)


class Category(db.Model):
    """Diversity categories."""

    __tablename__ = "categories"

    diversity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    percentage = db.Column(db.Integer)

    def __repr__(self):
        """Show info about categories."""

        return "<Category diversity_id=%s category=%s company_id=%s percentage=%s>" % (self.diversity_id, self.category, self.company_id, self.percentage)

    company = db.relationship('Company', backref=db.backref("categories", order_by=diversity_id))


class Review(db.Model):
    """Company reviews table."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    rating = db.Column(db.Integer)
    employee_status = db.Column(db.String(64))
    review_title = db.Column(db.String(64))
    pros = db.Column(db.String(500))
    cons = db.Column(db.String(500))

    def __repr__(self):
        """Show info about comment."""

        return "<Review review_id=%s company_id=%s rating=%s" % (self.review_id, self.company_id, self.rating)

    company = db.relationship('Company', backref=db.backref("review", order_by=review_id))




##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///diversity'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
