from flask import request, session, render_template, redirect
from time import sleep
import bcrypt


def password_protected(func):
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(f'/authenticate?redirect={request.path}')
    
    wrapper.__name__ = func.__name__
    
    return wrapper


def create_authentication_routes(app, authentication_page):
    @app.route('/authenticate', methods=['GET', 'POST'])
    def authenticate():
        redirect_url = request.args.get('redirect')

        if request.method == 'POST':
            if bcrypt.checkpw(request.form['password'].encode(), app.config['SITE_PASSWORD']):
                session['logged_in'] = True

                return redirect(redirect_url)
            else:
                sleep(1)

        return render_template(authentication_page, redirect_url=redirect_url)


    @app.route('/logout')
    def logout():
        del session['logged_in']

        return redirect('/')
