from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Store, Customer
from .product import ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for stores"""

    # products = ProductSerializer(Many=True)

    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "description",
            "customer",
            # "products",
        )


class Stores(ViewSet):

    def create(self, request):
        """
        @apt {POST} /stores POST new stores
        @apiName CreateStore
        @apiGroup Store
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {String} name Short form name of store
        @apiParam {String} description Short from description of store
        @apiParam {Number} customer_id Customer of customer
        @apiParamExample {json} Input
            {
                "name": "Example Store Name",
                "description": "Example Store Description",
                "customer_id": 4
            }
        @apiSuccess (200) {Object} store Created store
        @apiSuccess (200) {id} store.id Store Id
        @apiSuccess (200) {String} store.name Short form name of store
        @apiSuccess (200) {String} store.description Long form description of store
        @apiSuccess (200) {String} store.customer_id Id of Store owner
        @apiSuccessExample {json} Success
            {
                "id": 1,
                "name": "",
                "description": "Kite",
                "customer" :
                {
                    "customer_id": "http://localhost:8000/customers/1",
                }
            }
        """

        new_store = Store()
        new_store.name = request.data["name"]
        new_store.description = request.data["description"]

        customer = Customer.objects.get(user=request.auth.user)

        new_store.customer = customer

        new_store.save()

        serializer = StoreSerializer(new_store, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
