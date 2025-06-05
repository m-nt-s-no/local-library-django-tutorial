import os
import django
from faker import Faker
import random

# Configure settings for project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')

# Load the Django project's settings
django.setup()

# Import models
from catalog.models import Genre, Book, BookInstance, Author, Language

# Initialize Faker instance
fake = Faker()
Faker.seed(1) # generate consistent sample data

for _ in range(10):
    auth = Author.objects.get_or_create(first_name = fake.first_name(), 
                                        last_name = fake.last_name())
    auth.save()
    book = Book(title = fake.sentence(nb_words = 5), 
                author = auth, 
                isbn = fake.isbn13())
    book.save()
