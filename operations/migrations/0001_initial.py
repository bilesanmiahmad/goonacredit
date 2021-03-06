# Generated by Django 2.1.2 on 2018-10-09 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_number', models.CharField(max_length=50, verbose_name='reference number')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='expiry date')),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Farm name')),
                ('address', models.TextField(blank=True, verbose_name='Farm address')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('size', models.IntegerField(blank=True, null=True, verbose_name='size')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
        ),
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('type', models.CharField(choices=[('S', 'Service'), ('P', 'Product')], default='P', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='amount')),
                ('details', models.TextField(blank=True, verbose_name='transaction details')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BigIntegerField(verbose_name='Account number')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='balance')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True, verbose_name='summary')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visited_farm', to='operations.Farm')),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visited_farmer', to=settings.AUTH_USER_MODEL)),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visiting_officer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_transactions', to='operations.TransactionAccount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_transactions', to='operations.TransactionAccount'),
        ),
        migrations.AddField(
            model_name='card',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='operations.TransactionAccount'),
        ),
    ]
