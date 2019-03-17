from flask import Flask
from app import create_app, db
from flask_script import Server, Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from config import Config
from app.models.user import User

app = create_app('default')
migrate = Migrate(app, db)
manager = Manager(app=app)


def make_shell_context():
	return dict(app=app, db=db, User=User)

manager.add_command('runserver',
                    Server(host=Config.MAIN_HOST, port=Config.MAIN_POST, use_debugger=True, use_reloader=True))
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run(default_command='runserver')
