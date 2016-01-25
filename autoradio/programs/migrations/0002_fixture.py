# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core import serializers
import os

fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
#fixture_filename = 'initial_data.json'

def load_fixture(apps, schema_editor):

    #print ""
    #print "Insert password for  user 'autoradio' (administrator superuser)"
    #call_command("createsuperuser",username="autoradio",email="autoradio@casa.it") 
    from django.core.management import call_command
    call_command("createsuperuser",username="autoradio",email="autoradio@casa.it",interactive=False) 

    from django.contrib.auth.models import User
    u = User.objects.get(username__exact='autoradio')
    u.set_password('autoradio')
    u.save()

    for fixture_filename in os.listdir(fixture_dir):
        if fixture_filename[-5:] == ".json":
            
            fixture_file = os.path.join(fixture_dir, fixture_filename)
            print "load fixture from file: ",fixture_file

            fixture = open(fixture_file, 'rb')
            objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
            for obj in objects:
                obj.save()
            fixture.close()

#def load_fixture(apps, schema_editor):
#    call_command('loaddata', 'initial_data', app_label='stations') 

def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    MyModel = apps.get_model("programs", "MediaCategory")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "ParentCategory")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "ChildCategory")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "Giorno")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "Configure")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "ProgramType")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "Show")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "Episode")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "Enclosure")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "Schedule")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "ScheduleDone")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "PeriodicSchedule")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("programs", "AperiodicSchedule")
    MyModel.objects.all().delete()

#    MyModel = apps.get_model("stations", "UserProfile")
#    MyModel.objects.get(user=apps.get_model("auth", "User").objects.get(username="autoradio")).delete()
#    apps.get_model("auth", "User").objects.get(username="autoradio").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
