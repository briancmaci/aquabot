from flask import render_template, request, flash, redirect, url_for
from . import admin
from .forms import LoginForm, RegistrationForm, PostFactForm
from ..models import db, User, Post, AdditionalFact, TagButton
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse


@admin.route('/')
@admin.route('/index')
@login_required
def index():
    return render_template('index.html', title="aquabot")


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('.login'))
    return render_template('register.html', title='Register', form=form)


@admin.route('/post_fact', methods=['GET', 'POST'])
@login_required
def post_fact():
    form = PostFactForm()

    if form.validate_on_submit():
        post = Post(user_id=current_user.id)
        post.header = form.header.data
        post.title = form.title.data
        post.title_url = form.title_url.data
        post.image_url = form.image_url.data
        post.body = form.body.data
        db.session.add(post)
        db.session.flush()

        for fact in form.additional_facts.data:
            additionalFact = AdditionalFact(post_id=post.id)
            additionalFact.title = fact["title"]
            additionalFact.text = fact["text"]
            additionalFact.is_long = fact["is_long"]
            db.session.add(additionalFact)

        for tag in form.tag_buttons.data:
            tagButton = TagButton(post_id=post.id)
            tagButton.title = tag["title"]
            tagButton.url = tag["url"]
            db.session.add(tagButton)


        db.session.commit()
        flash(post)
        flash('Congratulations you have a valid post!')

    else:
        flash('Something is wrong. buuut. I do not know what')
        flash(form.errors)

    flash(form.data)
    return render_template('post_fact.html', title='Post an LGBTQ Fact', form=form)


@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))
