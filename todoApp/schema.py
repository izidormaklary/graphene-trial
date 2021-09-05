import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'status', 'date_created')


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)
    todo_by_id = graphene.Field(TodoType, pk=graphene.Int(required=True), description="Getting todo by id")

    def resolve_todos(root, info, **kwargs):
        return Todo.objects.all()

    def resolve_todo_by_id(root, info, pk):
        return Todo.objects.get(id=pk)


class UpdateTodo(graphene.Mutation):
    class Arguments:
        # Mutation to update a todo
        title = graphene.String(required=True)
        id = graphene.ID()
        status = graphene.Boolean()

    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls, root, info, title, id, status):
        todo = Todo.objects.get(pk=id)
        todo.title = title
        todo.status = status
        todo.save()

        return UpdateTodo(todo=todo)


class CreateTodo(graphene.Mutation):
    class Arguments:
        # Mutation to create a todo
        title = graphene.String(required=True)
        status = graphene.Boolean()

    # Class attributes define the response of the mutation
    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls, root, info, title, status):
        todo = Todo()
        todo.title = title
        todo.status = status
        todo.save()

        return CreateTodo(todo=todo)


class Mutation(graphene.ObjectType):
    update_todo = UpdateTodo.Field()
    create_todo = CreateTodo.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
