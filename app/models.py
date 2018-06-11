"""
Definition of models.
"""

from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

#############################################################################################################################


class Category(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    visible = models.SmallIntegerField()
    note = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Countrytable(models.Model):
    country = models.CharField(max_length=40, blank=True, null=True)
    countrycode = models.CharField(primary_key=True, max_length=5)

    def __unicode__(self):
        return self.country

    class Meta:
        managed = False
        db_table = 'countrytable'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['country']

class PenguinnessPhotos(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    species = models.ForeignKey('Speciestable', models.DO_NOTHING)
    credit = models.CharField(max_length=60, blank=True, null=True)

    def __unicode__(self):
        return self.species

    class Meta:
        managed = False
        db_table = 'penguinness_photos'
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos' 
        ordering = ['species']

class Reference(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('Speciestable', models.DO_NOTHING, db_column='parent', blank=True, null=True)
    sitekey = models.ForeignKey('Sitetable', models.DO_NOTHING, db_column='sitekey', blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deptha = models.CharField(max_length=60, blank=True, null=True)
    sd_depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sample_size_depth = models.IntegerField(blank=True, null=True)
    depthsample = models.CharField(max_length=200, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    durationa = models.CharField(max_length=200, blank=True, null=True)
    sd_duration = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_duration = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sample_size_duration = models.IntegerField(blank=True, null=True)
    durationsample = models.CharField(max_length=200, blank=True, null=True)
    methods = models.TextField(blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=60, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.parent.species


    class Meta:
        managed = False
        db_table = 'reference'
        verbose_name = 'Reference'
        verbose_name_plural = 'References'
        ordering = ['parent__species']

class Sitetable(models.Model):
    id = models.IntegerField(primary_key=True)
    countrycode = models.ForeignKey(Countrytable, models.DO_NOTHING, db_column='countrycode')
    site = models.CharField(max_length=60)
    lat = models.DecimalField(max_digits=6, decimal_places=2)
    lon = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.site

    class Meta:
        managed = False
        db_table = 'sitetable'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'


class Speciestable(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    latin = models.CharField(max_length=60, blank=True, null=True)
    species = models.CharField(max_length=60, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category', blank=True, null=True)
    subcategory = models.ForeignKey('Subcategory', models.DO_NOTHING, db_column='subcategory', blank=True, null=True)
    subgroup = models.ForeignKey('Subgroup', models.DO_NOTHING, db_column='subgroup', blank=True, null=True)
    mass = models.IntegerField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    visible = models.SmallIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    oisooupas = models.SmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.species

    class Meta:
        managed = False
        db_table = 'speciestable'
        verbose_name = 'Species'
        verbose_name_plural = 'Species'
        ordering = ['species']

class Subcategory(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category', blank=True, null=True)
    position = models.SmallIntegerField(blank=True, null=True)
    visible = models.SmallIntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'subcategory'
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'


class Subgroup(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, models.DO_NOTHING, db_column='subcategory', blank=True, null=True)
    position = models.SmallIntegerField(blank=True, null=True)
    visible = models.SmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'subgroup'
        verbose_name = 'Subgroup'
        verbose_name_plural = 'Subgroups'