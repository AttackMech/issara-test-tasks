from django.core.management.base import BaseCommand
from dealers.models import Dealer
from faker import Faker

class Command(BaseCommand):
    help = 'Adds dealer data to the database'

    def handle(self, *args, **options):
        fake = Faker()

        for _ in range(100):
            dummy_instance = Dealer(
                name=fake.name(),
                name_en=fake.name(),
                license_number=fake.numerify(text="#####/####"),
                status=fake.random_element(elements=('Operational', 'Inoperational')),
                logo=fake.url(),
                email=fake.email(),
                rating_score=fake.random_int(min=10000, max=50000) / 10000.0,
                rating_count=fake.random_int(min=0, max=1000),
                comments_count=fake.random_int(min=0, max=1000),
                popularity=fake.random_int(min=0, max=5000),
                city=fake.random_int(min=0, max=100),
            )
            
            dummy_instance.save()

        self.stdout.write(self.style.SUCCESS('Successfully added data'))
