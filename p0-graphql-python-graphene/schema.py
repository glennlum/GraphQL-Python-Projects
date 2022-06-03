'''A simple graphql Query and Mutation implemented with Graphene'''

import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    '''A User type'''
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime(required=False)


class Query (graphene.ObjectType):
    '''A Query type'''
    users = graphene.List(User, first=graphene.Int())
    is_staff = graphene.Boolean()

    def resolve_users(self, info, first):
        '''Returns the first n users'''
        return [
            User(username='Alice', last_login=datetime.now()),
            User(username='John', last_login=datetime.now()),
            User(username='Billy', last_login=datetime.now())
        ][:first]

    def resolve_is_staff(self, info):
        '''Always returns true'''
        return True


class CreateUser(graphene.Mutation):
    '''A CreateUser mutation'''
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        '''Returns the created User'''
        if info.context.get('is_vip'):
            username = username.upper()
        user = User(username=username)
        return CreateUser(user=user)


class Mutations (graphene.ObjectType):
    '''A Mutation type'''
    create_user = CreateUser.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutations,
    auto_camelcase=False
)
# auto_camelcase = false , prevents obj field name conversion to camel case

result = schema.execute(
    '''
    mutation createUser ($username: String){
        create_user(username: $username){
            user {
                username
            }
        }
    }
    ''',
    variable_values={'username': 'Bob'},
    context={'is_vip': True}
)

items = dict(result.data.items())  # place results in a python dict
print(json.dumps(items, indent=4))  # return a json formatted result
