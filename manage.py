#!/usr/bin/env python
import os
from sured import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from sured.models import User, Role, Post, Permission, Comment, Tag
from sured.logger.models import AccountCreation, PostCreation

app = create_app(os.getenv('SURED_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post,
                Permission=Permission, Comment=Comment,
                AccountCreation=AccountCreation, PostCreation=PostCreation,
                Tag=Tag)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    ''' unit tests'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy_dev():
    ''' deploy in development(using faked data)'''
    from flask.ext.migrate import init, migrate,  upgrade
    from sured.models import Role, User, Post, Comment

    #migrade database
    init()
    migrate()
    upgrade()

    # create roles
    Role.insert_roles()

    # fake users
    User.generate_fake()

    # fake tags
    Tag.generate_fake()

    # fake questions
    Post.generate_fake()

    # fake answers
    Comment.generate_fake()

if __name__ == '__main__':
    manager.run()
