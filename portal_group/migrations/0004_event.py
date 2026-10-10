# Generated for the school events calendar.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal_group', '0003_alter_advertisement_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['event_date', 'event_time', 'title']},
        ),
    ]
