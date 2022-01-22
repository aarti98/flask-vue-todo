from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(400))


    def __init__(self, title, description):
        # Add data to the instance. But why ??
        self.title = title
        self.description = description