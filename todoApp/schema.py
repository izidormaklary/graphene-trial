
from graphene import Field, List, ID, String, Boolean, Int, ObjectType, Schema, Mutation
from graphene_django import DjangoObjectType, DjangoListField
from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'status', 'date_created')


class Query(ObjectType):
    todos = List(TodoType, description="All todos")
    todo_by_id = Field(TodoType, pk=Int(required=True), description="Getting todo by id")
    todos_not_done = List(TodoType, description="Unfinished todos")

    def resolve_todos(root, info, **kwargs):
        return Todo.objects.all()

    def resolve_todo_by_id(root, info, pk):
        return Todo.objects.get(id=pk)

    def resolve_todos_not_done(root, info):
        return Todo.objects.filter(status=False)


class UpdateTodo(Mutation):
    class Arguments:
        # Mutation to update a todo
        title = String(required=True)
        id = ID(required=True)
        status = Boolean()

    todo = Field(TodoType)

    @classmethod
    def mutate(cls, root, info, title, id, status):
        todo = Todo.objects.get(pk=id)
        todo.title = title
        todo.status = status
        todo.save()

        return UpdateTodo(todo=todo)


class CreateTodo(Mutation):
    class Arguments:
        # Mutation to create a todo
        title = String(required=True)
        status = Boolean()

    # Class attributes define the response of the mutation
    todo = Field(TodoType)

    @classmethod
    def mutate(cls, root, info, title, status):
        todo = Todo()
        todo.title = title
        todo.status = status
        todo.save()

        return CreateTodo(todo=todo)


class Mutation(ObjectType):
    update_todo = UpdateTodo.Field()
    create_todo = CreateTodo.Field()


schema = Schema(query=Query, mutation=Mutation)
