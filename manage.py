from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand
from flask_cors import CORS
app=create_app('default')
manager=Manager(app)
# migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

CORS(app,supports_credentials=True, resources={r"/auth/*": {"origins": "*"},r"/case/*": {"origins": "*"},r"/result/*": {"origins": "*"}})

if __name__ == "__main__":
    #runserver -h 172.22.70.204
    manager.run()