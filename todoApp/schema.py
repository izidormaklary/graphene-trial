import graphene
from graphene_django import DjangoObjectType
from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'status', 'date_created')


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)

    def resolve_todos(root, info, **kwargs):
        return Todo.objects.all()


schema = graphene.Schema(query=Query)
