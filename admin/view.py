from flask import Blueprint, render_template, request

admin = Blueprint(
    'admin',
    '__name__',
    template_folder='templates/admin',
    static_folder='static/admin',
    )

@admin.route('/')
def home():
    return render_template('home.html')

@admin.route('/about')
def about():
    return render_template('about.html')

@admin.route('/nice')
def nice():
    return render_template('nice.html')
