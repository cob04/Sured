from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, \
    current_app, make_response, abort
from . import main
from ..models import User, Role, Permission, Post, Comment, post_saved
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
     CommentForm
from .. import db
from ..decorators import admin_required, permission_required
from flask.ext.login import login_required, current_user

@main.before_app_request
def before_request():
    if request.endpoint  != 'static':
        post_saved.send(current_app, request=request)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['SURED_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,\
        pagination=pagination)

@main.route('/users/<username>', methods=['GET', 'POST'])
def user(username):
    form = PostForm()
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    else:
        if current_user.can(Permission.WRITE_ARTICLES) and \
                form.validate_on_submit():
            post = Post(title=form.body.data,
                        body=form.body.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            return redirect(url_for('.user', username=user.username))
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts,\
                            form=form)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid User.', 'danger')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.', 'warning')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username, 'success')
    return redirect(url_for('.user', username=username))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid User.', 'danger')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.', 'warning')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are no longer following %s.' % username, 'warning')
    return redirect(url_for('.user', username=username))

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.', 'danger')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination=user.followers.paginate(
        page, per_page=current_app.config['SURED_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp':item.timestamp}
                for item in pagination.items]
    return render_template('followers.html', user=user, title='Followers of',
                            endpoint='.followers', pagination=pagination,
                            follows=follows)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user)
        flash('Your Profile has been updated.', 'success')
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
        flash('The profile has been updated.', 'success')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.bio.data = user.bio
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/questions/')
def posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['SURED_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('posts.html', posts=posts, pagination=pagination)

    
@main.route('/questions/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                        post=post,
                        author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your answer has been published.', 'success')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
               current_app.config['SURED_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['SURED_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                            comments=comments, pagination=pagination)

@main.route('/questions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.body.data
        post.body = form.body.data
        db.session.add(post)
        flash('Your post has been updated.', 'success')
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/comments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user != comment.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.body = form.body.data
        db.session.add(comment)
        flash('Your answer has been modified', 'success')
        return redirect(url_for('.post', id=comment.post_id))
    form.body.data = comment.body
    return render_template('edit_comment.html', form=form)

@main.route('/comments/select/<int:id>')
@login_required
def select_answer(id):
    comment = Comment.query.get_or_404(id)
    if current_user != comment.post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    for c in comment.post.comments:
        if c.answer:
            c.answer = False
            db.session.add(comment)
    comment.answer = True
    db.session.add(comment)
    flash('Answer to question selected', 'success')
    return redirect(url_for('.post', id=comment.post_id))

@main.route('/unanswered/')
def unanswered():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.comments == None).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['SURED_COMMENTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('posts.html', posts=posts, pagination=pagination)

@main.route('/help/')
def help():
    return render_template('help.html')
