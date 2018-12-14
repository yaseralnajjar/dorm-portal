from functools import reduce

from django.contrib.auth.models import AbstractUser

from django.db import models as django_models
from django.db.models.signals import post_delete


from i18nfield.fields import I18nCharField

from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet

from .utils import file_cleanup


class DormitoryQuerySet(django_models.QuerySet):
    def apply_room_filters(self, filters):

        if filters:
            filtered_rooms = RoomCharacteristics.objects.filter(filters[0])\
                .prefetch_related('radio_choices', 'integral_choices',
                                  'radio_choices__related_filter', 'integral_choices__related_filter',
                                  'features')

            for current_filter in filters:
                filtered_rooms = filtered_rooms.filter(current_filter)

            room_characteristics = django_models.Prefetch(
                'room_characteristics', queryset=filtered_rooms)

            dorms = self.filter(room_characteristics__in=filtered_rooms)\
                        .prefetch_related(room_characteristics).distinct()

        else:
            dorms = self.prefetch_related('room_characteristics').distinct()

        return dorms

    def apply_dorm_filters(self, filters):
        if filters:
            dorms = self.filter(filters[0])
            for current_filter in filters:
                dorms = dorms.filter(current_filter)

            dorms.prefetch_related('features')
        else:
            dorms = self

        return dorms

    def available(self):
        return self.filter(room_characteristics__allowed_quota__gte=1)

    def superfilter(self, category_id=None, duration_option_id=None,
                    dorm_features_ids=None, radio_integeral_choices=None, room_features_ids=None):

        result = self

        if category_id:
            result = result.filter(category__id=category_id)

        result = result.available()

        dorm_filters = []

        if dorm_features_ids:
            for current_feature in dorm_features_ids:
                current_filter = Filter.objects.filter(id=current_feature['id']).first()
                dorm_filters.append(current_filter.get_query())

        room_filters = []

        if duration_option_id:
            duration_option = RadioOption.objects.filter(duration_option_id).first()
            duration_filter = duration_option.related_filter.get_query(
                duration_option_id)
            room_filters.append(duration_filter)

        if room_features_ids:
            for current_feature in room_features_ids:
                current_filter = Filter.objects.filter(id=current_feature['id']).first()
                room_filters.append(current_filter.get_query())

        if radio_integeral_choices:
            for choice in radio_integeral_choices:
                current_filter = Filter.objects.filter(id=choice['id']).first()
                room_filters.append(current_filter.get_query_polymorphic(choice))

        result = result.apply_dorm_filters(dorm_filters)\
                       .apply_room_filters(room_filters)\
                       .annotate(rooms_left_in_dorm=django_models.Sum(
                           'room_characteristics__allowed_quota'))

        return result


class FilterQuerySet(PolymorphicQuerySet):

    def main_filters(self):
        return self.filter(django_models.Q(name='Duration'))

    def radio_filters(self):

        result = self.instance_of(RadioFilter).exclude(django_models.Q(name='Duration'))

        return result

    def integral_filters(self):

        result = self.instance_of(IntegralFilter)

        return result

    def additional_filters(self):
        return (self.radio_filters() | self.integral_filters()).distinct()

    def dorm_features(self):
        return self.instance_of(FeatureFilter).filter(featurefilter__is_dorm_feature=True)

    def room_features(self):
        return self.instance_of(FeatureFilter).filter(featurefilter__is_dorm_feature=False)


class Filter(PolymorphicModel):
    name = I18nCharField(max_length=60)

    objects = PolymorphicManager.from_queryset(FilterQuerySet)()

    def __str__(self):
        return f'{self.name} filter'


class RadioFilter(Filter):
    is_optional = django_models.BooleanField(default=True)

    def get_query(self, selected_options):
        return (django_models.Q(radio_choices__related_filter__id=self.id) &
                django_models.Q(radio_choices__selected_option__id__in=selected_options))

    def get_query_polymorphic(self, json_choice):
        option_ids = json_choice['choosen_options_ids']
        return self.get_query(option_ids)

    def __str__(self):
        return f'{self.name} radio filter'


class IntegralFilter(Filter):
    is_optional = django_models.BooleanField(default=True)

    def get_query(self, min, max):
        return (django_models.Q(integral_choices__related_filter__id=self.id) &
                django_models.Q(integral_choices__selected_number__gte=min) &
                django_models.Q(integral_choices__selected_number__lte=max))

    def get_query_polymorphic(self, json_min_max):
        return self.get_query(json_min_max['min_value'], json_min_max['max_value'])

    def __str__(self):
        return f'{self.name} intgeral filter'


class FeatureFilter(Filter):

    is_dorm_feature = django_models.BooleanField(default=False)

    def get_query(self):
        return django_models.Q(features__id=self.id)

    def __str__(self):
        return f'{self.name} filter'


class RadioOption(django_models.Model):
    name = I18nCharField(max_length=60)

    related_filter = django_models.ForeignKey(
        RadioFilter, related_name='options', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.name} option'


class Choice(PolymorphicModel):
    pass


class IntegralChoice(Choice):
    selected_number = django_models.IntegerField(default=0)

    related_filter = django_models.ForeignKey(
        IntegralFilter, related_name='integral_choices', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.related_filter.name} choice with number {self.selected_number}'


class RadioChoice(Choice):
    selected_option = django_models.ForeignKey(
        RadioOption, related_name='radio_choices', on_delete=django_models.CASCADE)
    related_filter = django_models.ForeignKey(
        RadioFilter, related_name='radio_choices', on_delete=django_models.CASCADE)

    def __str__(self):
        return f'{self.related_filter.name} choice with {self.selected_option}'


class Currency(django_models.Model):
    symbol = django_models.CharField(max_length=1)
    code = django_models.CharField(max_length=9)

    def __str__(self):
        return f'{self.code} Currency with Symbol {self.symbol}'

    class Meta:
        verbose_name_plural = 'Currencies'


class DormitoryCategory(django_models.Model):
    name = I18nCharField(max_length=60)

    class Meta:
        verbose_name_plural = 'Dormitory Categories'


class User(AbstractUser):
    is_manager = django_models.BooleanField(default=False)


class Dormitory(django_models.Model):
    name = django_models.CharField(max_length=60)
    about = I18nCharField(max_length=1000)

    geo_longitude = django_models.CharField(max_length=20)
    geo_latitude = django_models.CharField(max_length=20)
    address = django_models.CharField(max_length=150)

    contact_name = django_models.CharField(max_length=60)
    contact_email = django_models.CharField(max_length=60)
    contact_number = django_models.CharField(max_length=60)
    contact_fax = django_models.CharField(max_length=60)

    cover = django_models.ImageField()

    category = django_models.ForeignKey(
        DormitoryCategory, related_name='dormitories', on_delete=django_models.CASCADE)

    features = django_models.ManyToManyField(
        FeatureFilter, related_name='features')

    manager = django_models.ForeignKey(
        User, related_name='dormitories', on_delete=django_models.CASCADE)

    objects = DormitoryQuerySet.as_manager()

    def is_owner(self, manager):
        return self.manager == manager

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Dormitories'


class BankAccount(django_models.Model):
    bank_name = django_models.CharField(max_length=60)

    account_name = django_models.CharField(max_length=60)
    account_number = django_models.CharField(max_length=60)

    iban = django_models.CharField(max_length=60)
    swift = django_models.CharField(max_length=60)

    currency = django_models.ForeignKey(
        Currency, related_name='bank_accounts', on_delete=django_models.CASCADE)

    dormitory = django_models.ForeignKey(
        Dormitory, related_name='bank_accounts', on_delete=django_models.CASCADE)

    def is_owner(self, manager):
        return self.dormitory.manager == manager

    def __str__(self):
        return f'BankAccount id {self.id} name {self.bank_name} in {self.dormitory.name}'


class DormitoryPhoto(django_models.Model):
    photo = django_models.ImageField(upload_to='')
    is_3d = django_models.BooleanField(default=False)

    dormitory = django_models.ForeignKey(
        Dormitory, related_name='photos', on_delete=django_models.CASCADE)

    def is_owner(self, manager):
        return self.dormitory.manager == manager


post_delete.connect(file_cleanup, sender=DormitoryPhoto, dispatch_uid="gallery.image.file_cleanup")


class RoomCharacteristics(django_models.Model):
    total_quota = django_models.IntegerField(default=0)
    allowed_quota = django_models.IntegerField(default=0)

    price_currency = django_models.ForeignKey(
        Currency, related_name='room_characteristics', on_delete=django_models.CASCADE)

    room_confirmation_days = django_models.IntegerField(default=2)

    radio_choices = django_models.ManyToManyField(
        RadioChoice, related_name='radio_choices')

    integral_choices = django_models.ManyToManyField(
        IntegralChoice, related_name='integral_choices')

    features = django_models.ManyToManyField(
        FeatureFilter, related_name='room_characteristics')

    dormitory = django_models.ForeignKey(
        Dormitory, related_name='room_characteristics', on_delete=django_models.CASCADE)

    def get_price(self):
        # we use contains as we have multiple langs names
        return self.integral_choices.filter(related_filter__name__contains='Price')\
                                    .first().selected_number

    def get_room_type(self):
        return self.radio_choices.filter(related_filter__name__contains='Room Type')\
            .first().selected_option.name

    def get_people_allowed_number(self):
        return self.integral_choices.filter(related_filter__name__contains='People Allowed Number')\
                                    .first().selected_number

    def __str__(self):
        return f'Room id {self.id} in {self.dormitory.name}'

    class Meta:
        verbose_name_plural = 'Rooms'


class RoomPhoto(django_models.Model):
    photo = django_models.ImageField()
    is_3d = django_models.BooleanField(default=False)

    room_characteristics = django_models.ForeignKey(
        RoomCharacteristics, related_name='photos', on_delete=django_models.CASCADE)
