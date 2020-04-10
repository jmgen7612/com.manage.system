from app import create_app,db
from flask_script import Manager
from flask_migrate import MigrateCommand
from flask_cors import CORS
from app.models import User

app=create_app('default')
manager=Manager(app)
# migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

CORS(app,supports_credentials=True, resources={r"/auth/*": {"origins": "*"},r"/case/*": {"origins": "*"},r"/result/*": {"origins": "*"}})

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User)

# manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()