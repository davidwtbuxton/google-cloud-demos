# Generated by Django 4.0.7 on 2022-08-07 10:04

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('googleimages', '0001_initial'),
        ('wagtailcore', '0069_log_entry_jsonfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('date', models.DateField(verbose_name='Post date')),
                ('intro', models.CharField(max_length=250)),
                ('body', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPageGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='googleimages.googleimage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='home.blogpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]