from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Store, Customer
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from .product import ProductSerializer
from .productcategory import ProductCategorySerializer


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for customer store"""

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")
        depth = 1


class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for stores"""

    seller = UserSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "description",
            "customer_id",
            "seller",
            "products",
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
                    #! THIS EXAMPLE STORE OBJECT NEEDS COMPLETING
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

    def retrieve(self, request, pk=None):
        """
        Retrieve details of a single store.

        @api {GET} stores/:id Retrieve Single Store
        @apiName RetrieveStore
        @apiGroup Stores

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization:
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {Number} pk Store's unique ID.

        @apiSuccess {Number} id Store ID.
        @apiSuccess {String} name Store name.
        @apiSuccess {String} description Store description.
        @apiSuccess {Number} customer_id Customer ID.
        @apiSuccess {Object} seller Seller details.
        @apiSuccess {Number} seller.id Seller ID.
        @apiSuccess {String} seller.first_name Seller's first name.
        @apiSuccess {String} seller.last_name Seller's last name.
        @apiSuccess {Object[]} products List of products.
        @apiSuccess {Number} products.id Product ID.
        @apiSuccess {String} products.name Product name.
        @apiSuccess {Number} products.price Product price.
        @apiSuccess {Number} products.number_sold Number of products sold.
        @apiSuccess {String} products.description Product description.
        @apiSuccess {Number} products.quantity Product quantity.
        @apiSuccess {String} products.created_date Date product was created.
        @apiSuccess {String} products.location Product location.
        @apiSuccess {String} products.image_path Product image URL.
        @apiSuccess {Number} products.average_rating Product average rating.

        @apiSuccessExample {json} Success:
            HTTP/1.1 200 OK
            {
                "id": 1,
                "name": "Joe's Store",
                "description": "Cool Stuff",
                "customer_id": 5,
                "seller": {
                    "id": 6,
                    "first_name": "Joe",
                    "last_name": "Shepherd"
                },
                "products": [
                    {
                        "id": 101,
                        "name": "Scarf",
                        "price": 199.26,
                        "number_sold": 0,
                        "description": "Woolen scarf for cold weather",
                        "quantity": 9,
                        "created_date": "2023-01-01",
                        "location": "Berlin",
                        "image_path": "http://localhost:8000/media/products/clothing.png",
                        "average_rating": 0
                    },
                    {
                        "id": 103,
                        "name": "Hat",
                        "price": 65.77,
                        "number_sold": 0,
                        "description": "A stylish baseball cap",
                        "quantity": 3,
                        "created_date": "2023-01-01",
                        "location": "Dubai",
                        "image_path": "http://localhost:8000/media/products/clothing.png",
                        "average_rating": 0
                    },
                    ... // lists all the rest of the seller's products
                ]
            }
        """

        try:
            customer = Customer.objects.get(user=request.auth.user)
            store = Store.objects.get(pk=pk, customer=customer)
            serializer = StoreSerializer(store, context={"request": request})
            return Response(serializer.data)

        except Store.DoesNotExist as ex:
            return Response(
                {
                    "message": "The requested store does not exist, or you do not have permission to access it."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        @api {GET} /orders GET customer orders
        @apiName GetOrders
        @apiGroup Orders

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {id} payment_id Query param to filter by payment used

        @apiSuccess (200) {Object[]} orders Array of order objects
        @apiSuccess (200) {id} orders.id Order id
        @apiSuccess (200) {String} orders.url Order URI
        @apiSuccess (200) {String} orders.created_date Date order was created
        @apiSuccess (200) {String} orders.payment_type Payment URI
        @apiSuccess (200) {String} orders.customer Customer URI

        @apiSuccessExample {json} Success
            [
                {
                    "id": 1,
                    "url": "http://localhost:8000/orders/1",
                    "created_date": "2019-08-16",
                    "payment_type": "http://localhost:8000/paymenttypes/1",
                    "customer": "http://localhost:8000/customers/5"
                }
            ]
        """
        try:
            store = Store.objects.all()
            serializer = StoreSerializer(store, many=True, context={"request": request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
