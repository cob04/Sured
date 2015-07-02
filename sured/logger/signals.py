from flask import render_template, current_app, flash, url_for
from .models import AccountCreation, PostCreation
from ..models import model_saved, post_saved, comment_saved
from .. import db
from flask.ext.login import current_user

def log_account_creation(app, user):
    account = AccountCreation(account_id=user.id)
    db.session.add(account)
    db.session.commit()

model_saved.connect(log_account_creation, current_app)

def log_post_creation(app, request):
    print request.path
    print request.user_agent.browser
    print request.user_agent.platform
    print request.remote_addr
    print request.method

post_saved.connect(log_post_creation, current_app)

def flash_new_comment(app, comment):
    if comment.author != current_user:
        flash('%s has posted an anwser to your question'\
                %comment.author.username)

comment_saved.connect(flash_new_comment, current_app)
