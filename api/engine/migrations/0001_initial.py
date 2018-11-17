# Generated by Django 2.0 on 2018-11-17 16:42

from django.db import migrations, models
import django.db.models.deletion
import i18nfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=1)),
                ('code', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Dormitory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', i18nfield.fields.I18nCharField(max_length=60)),
                ('about', i18nfield.fields.I18nCharField(max_length=1000)),
                ('geo_longitude', models.CharField(max_length=20)),
                ('geo_latitude', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='DormitoryCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', i18nfield.fields.I18nCharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', i18nfield.fields.I18nCharField(max_length=60)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='RadioOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', i18nfield.fields.I18nCharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='RoomCharacteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_quota', models.IntegerField(default=0)),
                ('allowed_quota', models.IntegerField(default=0)),
                ('dormitory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_characteristics', to='engine.Dormitory')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureFilter',
            fields=[
                ('filter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.Filter')),
                ('is_dorm_feature', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('engine.filter',),
        ),
        migrations.CreateModel(
            name='IntegralChoice',
            fields=[
                ('choice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.Choice')),
                ('selected_number', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('engine.choice',),
        ),
        migrations.CreateModel(
            name='IntegralFilter',
            fields=[
                ('filter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.Filter')),
                ('is_optional', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('engine.filter',),
        ),
        migrations.CreateModel(
            name='RadioChoice',
            fields=[
                ('choice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.Choice')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('engine.choice',),
        ),
        migrations.CreateModel(
            name='RadioFilter',
            fields=[
                ('filter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.Filter')),
                ('is_optional', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('engine.filter',),
        ),
        migrations.AddField(
            model_name='filter',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_engine.filter_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='dormitory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dormitories', to='engine.DormitoryCategory'),
        ),
        migrations.AddField(
            model_name='choice',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_engine.choice_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='roomcharacteristics',
            name='features',
            field=models.ManyToManyField(related_name='room_characteristics', to='engine.FeatureFilter'),
        ),
        migrations.AddField(
            model_name='roomcharacteristics',
            name='integral_choices',
            field=models.ManyToManyField(related_name='integral_choices', to='engine.IntegralChoice'),
        ),
        migrations.AddField(
            model_name='roomcharacteristics',
            name='radio_choices',
            field=models.ManyToManyField(related_name='radio_choices', to='engine.RadioChoice'),
        ),
        migrations.AddField(
            model_name='radiooption',
            name='related_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='engine.RadioFilter'),
        ),
        migrations.AddField(
            model_name='radiochoice',
            name='related_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radio_choices', to='engine.RadioFilter'),
        ),
        migrations.AddField(
            model_name='radiochoice',
            name='selected_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radio_choices', to='engine.RadioOption'),
        ),
        migrations.AddField(
            model_name='integralchoice',
            name='related_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integral_choices', to='engine.IntegralFilter'),
        ),
        migrations.AddField(
            model_name='dormitory',
            name='features',
            field=models.ManyToManyField(related_name='features', to='engine.FeatureFilter'),
        ),
    ]
