from flask import Flask
from student_records.database import DB_URL, db
from student_records.telegram_api.urls import tg

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL

    app.register_blueprint(tg)
    db.init_app(app)
    return app


def create_database_tables(app):
    with app.app_context():
        db.create_all()


app = create_app()
create_database_tables(app)

@app.route('/')
def index():
    return {"Hello":"world"}

if __name__ == '__main__':
    app.run(debug=True)
