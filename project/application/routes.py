from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, PokemonPost, Like
from .forms import LoginForm, SignUpForm, ForgotPasswordForm, ResetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def root():
    return redirect(url_for('main.index'))

@main.route('/home')
@login_required
def index():
    pokemon_posts = PokemonPost.query.all()
    return render_template('index.html', pokemon_posts=pokemon_posts)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/like/<int:pokemon_post_id>', methods=['POST'])
@login_required
def like(pokemon_post_id):
    post = PokemonPost.query.get_or_404(pokemon_post_id)
    like = Like.query.filter_by(user_id=current_user.id, pokemon_post_id=pokemon_post_id).first()
    
    if like:
        db.session.delete(like)
        flash('You have unliked the post.')
    else:
        new_like = Like(user_id=current_user.id, pokemon_post_id=pokemon_post_id)
        db.session.add(new_like)
        flash('You have liked the post.')
    
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('If an account with that email already exists, a reset email will been sent.', 'info')
            return redirect(url_for('main.login'))
        else:
            flash('Email not found.', 'warning')
            return redirect(url_for('main.forgot_password'))
    return render_template('forgot_password.html', title='Forgot Password', form=form)

@main.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if not check_password_hash(user.password, form.old_pass.data):
            flash("Your old password is wrong.", "error")
        else:
            user.password = generate_password_hash(form.new_pass.data)
            db.session.commit()
            flash("Your password has been reset.", "success")
            return redirect(url_for('main.index'))

@main.route('/forgot_password', method=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        email = User.query.filter_by(email=email)
    return render_template('forgotpass.html', title='Forgot Password', form=form)

@main.route('reset_password', method=["GET", "POST"])
def reset_password():
    form = ResetPasswordForm

    if validate_on_submit():
        user = User.query.get(current_user.id)
        if user.password != form.old_pass.data:
            flash("Your old password is wrong", "error")
            return redirect(url_for("reset_password"))
        user.password = form.new_pass.data
        user.confirm.password = form.confirm_pass.data

        if form.old_pass.data == form.new_pass.data:
            flash("Your password is the same as the old one", "error")
            return redirect(url_for("reset_password"))

        db.session.commit()
        flash("Password has been reset", "success")
        return redirect(url_for("index"))
    
    return render_template('resetpass.html', title="ResetPassword", form=form)
