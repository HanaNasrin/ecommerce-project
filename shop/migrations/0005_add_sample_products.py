from django.db import migrations


def create_sample_products(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Product = apps.get_model('shop', 'Product')

    samples = {
        'Electronics': [
            {'name': 'Wireless Headphones', 'description': 'Comfortable wireless headphones with noise cancellation.', 'price': '1999.00', 'stock': 25},
            {'name': 'Bluetooth Speaker', 'description': 'Portable speaker with deep bass and long battery life.', 'price': '1499.00', 'stock': 40},
        ],
        'Clothing': [
            {'name': 'Men T-Shirt', 'description': '100% cotton crew-neck t-shirt.', 'price': '499.00', 'stock': 120},
            {'name': 'Women Jeans', 'description': 'Slim-fit stretch denim jeans.', 'price': '1299.00', 'stock': 60},
        ],
        'Home & Kitchen': [
            {'name': 'Non-stick Pan', 'description': 'Durable non-stick frying pan, 26cm.', 'price': '899.00', 'stock': 80},
            {'name': 'Cotton Bedsheet', 'description': 'Soft 100% cotton double bedsheet set.', 'price': '1999.00', 'stock': 50},
        ],
        'Books': [
            {'name': 'Learn Django', 'description': 'A practical guide to building web apps with Django.', 'price': '799.00', 'stock': 200},
            {'name': 'Python Cookbook', 'description': 'Recipes for mastering Python programming.', 'price': '999.00', 'stock': 150},
        ],
        'Toys': [
            {'name': 'Building Blocks Set', 'description': 'Creative blocks for kids aged 3+.', 'price': '599.00', 'stock': 90},
            {'name': 'Remote Car', 'description': 'High-speed remote controlled car.', 'price': '1299.00', 'stock': 40},
        ],
        'Beauty': [
            {'name': 'Face Moisturizer', 'description': 'Hydrating daily face moisturizer.', 'price': '399.00', 'stock': 150},
            {'name': 'Lipstick Set', 'description': 'Long-lasting matte lipstick set.', 'price': '699.00', 'stock': 70},
        ],
        'Sports': [
            {'name': 'Yoga Mat', 'description': 'Non-slip yoga mat with carry strap.', 'price': '799.00', 'stock': 100},
            {'name': 'Dumbbell Set', 'description': 'Adjustable dumbbell set for home workouts.', 'price': '3499.00', 'stock': 30},
        ],
        'Accessories': [
            {'name': 'Leather Wallet', 'description': 'Genuine leather bi-fold wallet.', 'price': '599.00', 'stock': 140},
            {'name': 'Sunglasses', 'description': 'UV-protected stylish sunglasses.', 'price': '899.00', 'stock': 85},
        ],
        'Appliances': [
            {'name': 'Electric Kettle', 'description': '1.7L rapid boil electric kettle.', 'price': '1599.00', 'stock': 45},
            {'name': 'Air Fryer', 'description': 'Compact air fryer with multiple presets.', 'price': '4999.00', 'stock': 25},
        ],
        'Groceries': [
            {'name': 'Olive Oil 1L', 'description': 'Extra virgin olive oil.', 'price': '699.00', 'stock': 200},
            {'name': 'Organic Honey', 'description': 'Pure organic honey, 500g.', 'price': '499.00', 'stock': 120},
        ],
    }

    for cat_name, products in samples.items():
        try:
            category = Category.objects.get(name=cat_name)
        except Category.DoesNotExist:
            continue

        for p in products:
            Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'category': category,
                    'description': p['description'],
                    'price': p['price'],
                    'image': '',
                    'stock': p['stock'],
                }
            )


def reverse_func(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    names = [
        'Wireless Headphones','Bluetooth Speaker','Men T-Shirt','Women Jeans',
        'Non-stick Pan','Cotton Bedsheet','Learn Django','Python Cookbook',
        'Building Blocks Set','Remote Car','Face Moisturizer','Lipstick Set',
        'Yoga Mat','Dumbbell Set','Leather Wallet','Sunglasses',
        'Electric Kettle','Air Fryer','Olive Oil 1L','Organic Honey'
    ]
    Product.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_add_initial_categories'),
    ]

    operations = [
        migrations.RunPython(create_sample_products, reverse_func),
    ]
