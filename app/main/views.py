from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, \
    current_app, make_response
from . import main
from ..models import User, Role, Permission, Question
from .forms import EditProfileForm, EditProfileAdminForm, QuestionForm
from .. import db
from ..decorators import admin_required, permission_required
from flask.ext.login import login_required, current_user

@main.route('/', methods=['GET', 'POST'])
def index():
    form = QuestionForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        question = Question(body=form.body.data,
                            author=current_user._get_current_object())
        db.session.add(question)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.timestamp.desc()).paginate(
        page, per_page=current_app.config['SURED_POSTS_PER_PAGE'],
        error_out=False)
    questions = pagination.items
    return render_template('index.html', form=form, questions=questions,\
        pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    questions = user.questions.order_by(Question.timestamp.desc()).all()
    return render_template('user.html', user=user, questions=questions)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user)
        flash('Your Profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.bio = form.bio.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.bio.data = user.bio
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/question/<int:id>')
def question(id):
    question = Question.query.get_or_404(id)
    return render_template('question.html', questions=[question])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    question = Question.query.get_or_404(id)
    if current_user != question.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = QuestionForm()
    if form.validate_on_submit():
        question.body = form.body.data
        db.session.add(question)
        flash('Your question had been updated.')
        return redirect(url_for('.question', id=question.id))
    form.body.data = question.body
    return render_template('edit_question.html', form=form)
