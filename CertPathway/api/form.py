"""REST API for interest form."""
import flask
import CertPathway
import logging

@CertPathway.app.route('/api/v1/form/', methods=['POST'])
def post_form():
    """Submit filled form"""
    data = flask.request.get_json()
    budgets = data['budgets']
    completionTimes = data['completionTimes']
    certificates = data['certificates']
    otherCertificates = data['otherCertificates']
    CertPathway.app.logger.info('Budgets: %s, Completion Times: %s, Certificates: %s, Other Certificates: %s', budgets, completionTimes, certificates, otherCertificates)

    # TODO: how are we tracking email?
    # email = mlanting@umich.edu

    # TODO: finish db setup
    # connection = CertPathway.model.get_db()
    # connection.execute("PRAGMA foreign_keys = ON;")

    # TODO: finish db call for budgets
    for budget in budgets:
        """
        connection.execute(
            INSERT INTO
                budget(email, cost),
                VALUES (?, ?)
            ,
            (email, budget)     
        )
        """
    
    # TODO: finish db call for completionTimes
    for time in completionTimes:
        """
        connection.execute(
            INSERT INTO
                time(email, time),
                VALUES (?, ?)
            ,
            (email, time)     
        )
        """

    # TODO: what is the purpose of the "keywords" table?
    # TODO: how are we parsing + tracking certificates?
    # TODO: how are we parsing + tracking otherCertificates? 

    return flask.jsonify(success=True), 200

@CertPathway.app.route('/api/v1/form/')
def get_form():
    """Return interest form info"""
    context = {
        "certificates": [
            "Accounting",
            "Architecture and Engineering",
            "Animal Health",
            "Business and Operations",
            "Beauty and Personal Care",
            "Construction and Trades",
            "Construction/Manufacturing",
            "Creative Media",
            "Cybersecurity",
            "Education and Training",
            "Design/Technology",
            "Food Service",
            "Education",
            "Finance/Mortgage",
            "Food and Beverage",
            "Food Service/Hospitality",
            "Health and Fitness",
            "Health and Safety",
            "Healthcare",
            "Information Technology",
            "Legal",
            "Personal Care and Service",
            "Office Administration",
            "Production and Public Safety",
            "Pharmacy/Healthcare",
            "Science",
            "Project Management",
            "Social Services",
            "Real Estate",
            "Technology"
            "Supply Chain/Procurement",
            "Transportation/Logistics",
        ],
        "budgets": [
            "$0 - $100",
            "$100 - $500",
            "$500 - $1,000",
            "$1,000 - $5,000",
            "$5,000+",
        ],
        "completion_times": [
            "Few hours to a day",
            "Few days to a few weeks",
            "Few weeks to a few months",
            "Several months to a year",
            "1-2 years",
            "2+ years",
        ],
        "submitted": "not submitted"
    }
    return flask.jsonify(**context)