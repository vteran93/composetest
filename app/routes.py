import time
import redis
from app import app
from app.models import User
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, flash, url_for

cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user =  User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid user name or password')

            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        
        return redirect('/index')
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def hello():
    user = {'username': 'Miguel'}
    count = get_hit_count()
    posts = [
        {
        'author': {'username':'Victor'}, 
        'post': 'Beautiful day in Porlant',
        'body': 'is the largest and most populous city in the U.S. state of Oregon and the seat of Multnomah County. It is a major port in the Willamette Valley region of the Pacific Northwest, at the confluence of the Willamette and Columbia rivers'
        },
        {
        'author': {'username':'Victor'}, 
        'post': 'The Avengers movie was so cool',
        'body': ' is a 2018 American superhero film based on the Marvel Comics superhero team the Avengers, produced by Marvel Studios and distributed by Walt Disney Studios Motion Pictures'
        }
    ]

    return render_template('index.html', title='Home', user=user, times=count, posts=posts)