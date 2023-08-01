from aws_lambda_typing import context as context_, events, responses

from typing import List

from google.protobuf.descriptor import ServiceDescriptor
from google.protobuf.empty_pb2 import Empty

from grpc import ServicerContext

from .petstore_pb2 import Pet, DESCRIPTOR as PETSTORE_DESCRIPTOR

from protomesh_py.lambda_grpc import GrpcRouter, GrpcHandler, AbstractGrpcService

import json

class PetStoreService(AbstractGrpcService):

    __pets: List[Pet] = []

    def get_service_descriptor(self) -> ServiceDescriptor:
        return PETSTORE_DESCRIPTOR.services_by_name["PetStoreService"]
        
    def Register(self, request: Pet, context: ServicerContext) -> Pet:

        self.__pets.append(request)

        request.attributes["foo"] = "bar"

        return request


    def List(self, request: Empty, context: ServicerContext):
        
        for pet in self.__pets:
            pet.attributes["nounce"] = json.dumps(context.invocation_metadata())
            yield pet


router = GrpcRouter()

router.register_service(PetStoreService())

handler = GrpcHandler(router)

def lambda_handler(event: events.APIGatewayProxyEventV1, context: context_.Context) -> responses.APIGatewayProxyResponseV1:
    return handler(event, context)