from django.db import models
# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Favoriteinformation(models.Model):
    favorite_id = models.CharField(primary_key=True, max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('Movieinformation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'favoriteinformation'


class Movieinformation(models.Model):
    movie_id = models.CharField(primary_key=True, max_length=10)
    movie_name = models.CharField(max_length=50)
    movie_year = models.CharField(max_length=5, blank=True, null=True)
    movie_director = models.CharField(max_length=50, blank=True, null=True)
    movie_screenwriter = models.CharField(max_length=50, blank=True, null=True)
    movie_roles = models.CharField(max_length=250, blank=True, null=True)
    movie_style = models.CharField(max_length=50, blank=True, null=True)
    movie_country = models.CharField(max_length=15, blank=True, null=True)
    movie_language = models.CharField(max_length=20, blank=True, null=True)
    movie_date = models.CharField(max_length=30, blank=True, null=True)
    movie_long = models.CharField(max_length=10, blank=True, null=True)
    movie_imdb = models.CharField(max_length=15, blank=True, null=True)
    movie_evaluation = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movieinformation'


class Surfinformation(models.Model):
    surf_id = models.CharField(primary_key=True, max_length=10)
    date_time = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=60, blank=True, null=True)
    movie = models.ForeignKey(Movieinformation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'surfinformation'

class Registerinfo(models.Model):
    user_account = models.CharField(primary_key=True, max_length=12)
    user_name = models.CharField(max_length=25)
    user_password = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=15)
    createtime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'registerinfo'


class Userinformation(models.Model):
    user_name = models.ForeignKey(Registerinfo, models.DO_NOTHING, db_column='user_name', related_name='name')
    user_account = models.OneToOneField(Registerinfo, models.DO_NOTHING, db_column='user_account', primary_key=True, related_name='id')
    user_password = models.ForeignKey(Registerinfo, models.DO_NOTHING, db_column='user_password', related_name='password')
    user_phone = models.ForeignKey(Registerinfo, models.DO_NOTHING, db_column='user_phone', blank=True, related_name='mobile')
    user_email = models.CharField(max_length=20, blank=True, null=True)
    user_sex = models.CharField(max_length=10, blank=True, null=True)
    user_age = models.IntegerField(blank=True, null=True)
    user_hobby = models.CharField(max_length=255, blank=True, null=True)
    surf = models.ForeignKey(Surfinformation, models.DO_NOTHING, null=True)
    favorite = models.ForeignKey(Favoriteinformation, models.DO_NOTHING, null=True)

    class Meta:
        managed = False
        db_table = 'userinformation'

