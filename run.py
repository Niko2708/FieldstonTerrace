from app import app, db
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'Post':Post}

if __name__ == "__main__":
    db.create_all()
    app.run()