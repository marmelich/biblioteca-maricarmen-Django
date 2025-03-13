from django.core.management.base import BaseCommand
from biblioteca.models import Llengua, Llibre, Exemplar, Usuari
from django.utils.timezone import now
import random
from faker import Faker

class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **kwargs):
        fake = Faker()
        Faker.seed(0)

        # Diccionario de idiomas con los códigos correctos
        llengues_data = {
            "Català": "es",   # Faker no soporta "ca_ES", usamos español
            "Castellano": "es",
            "English": "en_US",
            "Français": "fr_FR",
        }

        # Crear lenguas
        llengues = {}
        for nom, locale in llengues_data.items():
            llengues[nom] = Llengua.objects.create(nom=nom)

        # Crear libros con títulos y autores en el mismo idioma
        llibres = []
        for nom, obj in llengues.items():
            fake_locale = Faker(llengues_data[nom])  # Usa el código de idioma correcto
            for _ in range(10):
                llibre = Llibre.objects.create(
                    titol=fake_locale.catch_phrase() if nom in ["Català", "Castellano"] else fake_locale.sentence(nb_words=4),
                    autor=fake_locale.name(),
                    data_edicio=fake_locale.date_this_century(),
                    llengua=obj,
                    ISBN=fake_locale.isbn13(),
                    editorial=fake_locale.company(),
                    pagines=random.randint(100, 1000),
                )
                llibres.append(llibre)

        # Crear 2 ejemplares por libro
        for llibre in llibres:
            for _ in range(2):
                Exemplar.objects.create(cataleg=llibre, registre=fake.uuid4())

        # Crear usuarios
        fake = Faker("es_ES")  # Usamos nombres en español para los usuarios
        for _ in range(50):
            Usuari.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

        self.stdout.write(self.style.SUCCESS("✅ Datos insertados correctamente."))
