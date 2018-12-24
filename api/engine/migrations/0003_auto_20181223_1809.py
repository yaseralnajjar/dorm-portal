# Generated by Django 2.1.3 on 2018-12-23 16:09

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_auto_20181219_1844'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_creation_date', models.DateField(auto_now=True)),
                ('stars', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(Decimal('0.0')), django.core.validators.MaxValueValidator(Decimal('5.0'))])),
                ('description', models.TextField()),
                ('dormitory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='engine.Dormitory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('0', 'pending'), ('1', 'rejected'), ('2', 'confirmed'), ('3', 'waiting-manager-action'), ('4', 'manager-updated'), ('5', 'expired-dont-choose-this')], default='0', max_length=2),
        ),
    ]