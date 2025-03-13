from django.contrib.auth import get_user_model
from biblioteca.models import Llengua, Llibre, Exemplar, Usuari
from django.utils.timezone import now
import random
from faker import Faker

fake = Faker()
User = get_user_model()

# Crear lenguas
llengues = {
    "Català": Llengua.objects.create(nom="Català"),
    "Castellano": Llengua.objects.create(nom="Castellano"),
    "English": Llengua.objects.create(nom="English"),
    "Français": Llengua.objects.create(nom="Français"),
}

# Crear libros
llibres = []
for llengua, obj in llengues.items():
    for _ in range(10):
        llibre = Llibre.objects.create(
            titol=fake.sentence(nb_words=4),
            autor=fake.name(),
            data_edicio=fake.date_this_century(),
            llengua=obj,
            ISBN=fake.isbn13(),
            editorial=fake.company(),
            pagines=random.randint(100, 1000),
        )
        llibres.append(llibre)

# Crear ejemplares (2 por libro)
for llibre in llibres:
    for _ in range(2):
        Exemplar.objects.create(cataleg=llibre, registre=fake.uuid4())

# Crear usuarios
for _ in range(50):
    Usuari.objects.create_user(
        username=fake.user_name(),
        email=fake.email(),
        password="password123",
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )

print("Datos insertados correctamente.")
