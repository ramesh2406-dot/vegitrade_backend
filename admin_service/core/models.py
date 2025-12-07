from djongo import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    stock_kg = models.FloatField()
    supplier_name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.price_per_kg}/kg"

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"
