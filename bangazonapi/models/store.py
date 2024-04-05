from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE
from .customer import Customer


class Store(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE
    name = models.CharField(
        max_length=50,
    )
    description = models.CharField(
        max_length=255,
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="stores"
    )

    @property
    def seller(self):
        return self.customer.user

    @property
    def products(self):
        return self.customer.products
