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
    date = models.DateTimeField()
    movie = models.ForeignKey('Movieinformation', models.DO_NOTHING)
    user = models.ForeignKey('Userinformation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'favoriteinformation'


class MovieInfo2(models.Model):
    movie_name = models.CharField(primary_key=True, max_length=100, blank=True)
    person = models.CharField(max_length=15, blank=True, null=True)
    star4 = models.CharField(max_length=10, blank=True, null=True)
    star5 = models.CharField(max_length=10, blank=True, null=True)
    star3 = models.CharField(max_length=10, blank=True, null=True)
    star2 = models.CharField(max_length=10, blank=True, null=True)
    star1 = models.CharField(max_length=10, blank=True, null=True)
    good = models.CharField(max_length=10, blank=True, null=True)
    introduction = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_info2'

class Moviecomments(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    movie_name = models.CharField(max_length=50, blank=True, null=True)
    user_name = models.CharField(max_length=20, blank=True, null=True)
    evaluation = models.CharField(max_length=10, blank=True, null=True)
    time = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    up = models.CharField(max_length=5, blank=True, null=True)
    down = models.CharField(max_length=5, blank=True, null=True)
    response = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'moviecomments'



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


class Registerinfo(models.Model):
    user_account = models.CharField(primary_key=True, max_length=12)
    user_name = models.CharField(max_length=25)
    user_password = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=15)
    createtime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'registerinfo'


class Scoreinformation(models.Model):
    eva_id = models.CharField(primary_key=True, max_length=10)
    user = models.ForeignKey('Userinformation', models.DO_NOTHING)
    movie = models.ForeignKey(Movieinformation, models.DO_NOTHING)
    movie_score = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'scoreinformation'


class Surfinformation(models.Model):
    surf_id = models.CharField(primary_key=True, max_length=10)
    date_time = models.DateTimeField()
    link = models.CharField(max_length=60, blank=True, null=True)
    movie_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'surfinformation'


class Userinformation(models.Model):
    user_name = models.CharField(max_length=25)
    user_account = models.CharField(primary_key=True, max_length=12)
    user_password = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=15)
    user_email = models.CharField(max_length=20, blank=True, null=True)
    user_sex = models.CharField(max_length=10, blank=True, null=True)
    user_age = models.IntegerField(blank=True, null=True)
    user_hobby = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userinformation'
