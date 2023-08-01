terraform {
  required_providers {
    protomesh = {
      source = "protomesh/protomesh"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.5.1"
    }

  }
}

provider "random" {}

provider "protomesh" {
  address    = "localhost:6680"
  enable_tls = true
}

resource "random_uuid" "petstore" {
}

resource "protomesh_gateway_policy" "petstore" {

  namespace = "gateway"

  resource_id = random_uuid.petstore.result
  name        = "Route to PetStoreService.Register method"

  policy {

    source {
      grpc {
        method_name = "/petstore.PetStoreService/"
        exact_method_name_match = false
      }
    }
    
    handlers {
      handler {
        aws {
          handler {
            lambda {
              function_name = "protomesh-python-petstore"
              qualifier     = "$LATEST"
            }
          }
        }
      }
    }

  }

}
