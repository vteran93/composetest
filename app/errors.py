from flask import render_template
from app import app, db

NOT_FOUND_CODE = 404
INTERNAL_ERROR = 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), NOT_FOUND_CODE

@app.errorhandler(500)
def internal_error(error):
 db.session.rollback()
 return render_template('500.html'), INTERNAL_ERROR
