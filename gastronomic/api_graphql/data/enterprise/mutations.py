from graphene import Field
from graphene import Mutation
from graphene.types.scalars import ID
from graphql import GraphQLError
from graphql_relay.node.node import from_global_id

from enterprises.models import Enterprise
from api_graphql.data.enterprise.types import EnterpriseNode
from api_graphql.data.enterprise.inputs import CreateEnterpriseInput
from api_graphql.data.enterprise.inputs import UpdateEnterpriseInput
from api_graphql.utils import delete_attributes_none
from api_graphql.utils import transform_global_ids

# Create your mutations here


class CreateEnterprise(Mutation):
    """Clase para crear establecimientos"""

    enterprise = Field(EnterpriseNode)

    class Arguments:
        input = CreateEnterpriseInput(required=True)

    def mutate(self, info, input):
        input = delete_attributes_none(**vars(input))
        enterprise = Enterprise.objects.create(**input)

        return CreateEnterprise(enterprise=enterprise)


class UpdateEnterprise(Mutation):
    """Clase para actualizar establecimientos"""

    enterprise = Field(EnterpriseNode)

    class Arguments:
        input = UpdateEnterpriseInput(required=True)

    def mutate(self, info, input):
        input = delete_attributes_none(**vars(input))
        input = transform_global_ids(**input)

        Enterprise.objects.filter(pk=input.get('id')).update(**input)
        enterprise = Enterprise.objects.get(pk=input.get('id'))

        return UpdateEnterprise(enterprise=enterprise)


class DeleteEnterprise(Mutation):
    """Clase para eliminar establecimientos"""

    enterprise = Field(EnterpriseNode)

    class Arguments:
        input = ID(required=True)

    def mutate(self, info, input):
        input = from_global_id(input)[1]

        try:
            enterprise = Enterprise.objects.get(pk=input)
            Enterprise.objects.filter(pk=input).delete()
        except Enterprise.DoesNotExist:
            raise GraphQLError('Enterprise does not delete')

        return CreateEnterprise(enterprise=enterprise)
