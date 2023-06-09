# Generated by Django 4.1.7 on 2023-04-02 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='price')),
                ('discount', models.SmallIntegerField(default=0, verbose_name='discount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('archived', models.BooleanField(default=False, verbose_name='archived')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['name', 'price'],
            },
        ),
    ]
