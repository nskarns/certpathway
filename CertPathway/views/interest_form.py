import flask
from flask import Flask, render_template
from flask import Flask, redirect, url_for, session
import CertPathway 

@CertPathway.app.route("/interest-form/")
def show_interest_form():
    """Display /interest-form/ route."""

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
        ]
    }

    return render_template("interest_form.html", **context)