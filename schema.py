import imp
from app import ma

class TodoSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'description']

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)