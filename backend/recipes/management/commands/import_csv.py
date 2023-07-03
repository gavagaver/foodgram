import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Max

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Loads data from csv-files. Use: python manage import_csv'

    MODELS_FILES = {
        Ingredient: 'ingredients.csv',
    }

    def start_import(self):
        directory = f'{settings.DATA_PATH}\n'
        file_names = "\n".join(list(self.MODELS_FILES.values()))
        info = ('Data will be added from the following directory:\n'
                + directory
                + 'List of files:\n'
                + file_names)

        self.stdout.write(
            self.style.MIGRATE_HEADING('Start importing data from csv-files')
        )
        self.stdout.write(
            self.style.HTTP_INFO(info)
        )

    def load_data(self):
        self.stdout.write(
            self.style.HTTP_INFO(
                'Loading data to the database...'
            )
        )
        try:
            for model, file_name in self.MODELS_FILES.items():
                file_path = os.path.join(
                    settings.BASE_DIR,
                    f'{file_name}'
                )
                try:
                    last_id = (
                        Ingredient.objects.aggregate(Max('id'))['id__max']
                    )
                except:
                    last_id = 0
                with open(file_path, 'r', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    data = [model(instance_id, *row) for instance_id, row in
                            enumerate(reader, last_id + 1)]
                    model.objects.bulk_create(data)
            self.stdout.write(
                self.style.SUCCESS(
                    'Success! Data from csv-files uploaded to the database.'
                )
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(
                    f'Error while uploading: {error}'
                )
            )

    def handle(self, *args, **options):
        self.start_import()
        self.load_data()
