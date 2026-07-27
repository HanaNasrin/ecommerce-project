from django.db import migrations


def set_product_images(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    mapping = {
        'Wireless Headphones': 'products/wireless-headphones.png',
        'Bluetooth Speaker': 'products/bluetooth-speaker.png',
        'Men T-Shirt': 'products/men-t-shirt.png',
        'Women Jeans': 'products/women-jeans.png',
        'Non-stick Pan': 'products/non-stick-pan.png',
        'Cotton Bedsheet': 'products/cotton-bedsheet.png',
        'Learn Django': 'products/learn-django.png',
        'Python Cookbook': 'products/python-cookbook.png',
        'Building Blocks Set': 'products/building-blocks-set.png',
        'Remote Car': 'products/remote-car.png',
        'Face Moisturizer': 'products/face-moisturizer.png',
        'Lipstick Set': 'products/lipstick-set.png',
        'Yoga Mat': 'products/yoga-mat.png',
        'Dumbbell Set': 'products/dumbbell-set.png',
        'Leather Wallet': 'products/leather-wallet.png',
        'Sunglasses': 'products/sunglasses.png',
        'Electric Kettle': 'products/electric-kettle.png',
        'Air Fryer': 'products/air-fryer.png',
        'Olive Oil 1L': 'products/olive-oil-1l.png',
        'Organic Honey': 'products/organic-honey.png',
    }

    for name, path in mapping.items():
        try:
            p = Product.objects.get(name=name)
            p.image = path
            p.save()
        except Product.DoesNotExist:
            continue


def unset_product_images(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    names = list({
        'Wireless Headphones','Bluetooth Speaker','Men T-Shirt','Women Jeans',
        'Non-stick Pan','Cotton Bedsheet','Learn Django','Python Cookbook',
        'Building Blocks Set','Remote Car','Face Moisturizer','Lipstick Set',
        'Yoga Mat','Dumbbell Set','Leather Wallet','Sunglasses',
        'Electric Kettle','Air Fryer','Olive Oil 1L','Organic Honey'
    })
    Product.objects.filter(name__in=names).update(image='')


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_add_sample_products'),
    ]

    operations = [
        migrations.RunPython(set_product_images, unset_product_images),
    ]
