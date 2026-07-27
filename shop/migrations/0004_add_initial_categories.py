from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    categories = [
        'Electronics',
        'Clothing',
        'Home & Kitchen',
        'Books',
        'Toys',
        'Beauty',
        'Sports',
        'Accessories',
        'Appliances',
        'Groceries',
    ]

    for name in categories:
        Category.objects.get_or_create(name=name)


def reverse_func(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    names = [
        'Electronics',
        'Clothing',
        'Home & Kitchen',
        'Books',
        'Toys',
        'Beauty',
        'Sports',
        'Accessories',
        'Appliances',
        'Groceries',
    ]
    Category.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order_address_order_city_order_phone_order_pincode'),
    ]

    operations = [
        migrations.RunPython(create_categories, reverse_func),
    ]
