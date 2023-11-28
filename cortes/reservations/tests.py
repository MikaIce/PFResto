from django.test import TestCase, Client
from django.urls import reverse
from .models import TableReservation
from datetime import date, time
from django.contrib.auth.models import User

#test de reservation
class ReservationTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_successful_reservation(self):
        response = self.client.post(reverse('book-a-table'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '123456789',
            'date': date.today(),
            'time': time(18, 30),
            'people': 2,
            'message': 'No allergies'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TableReservation.objects.count(), 1)

    def test_reservation_exceeds_capacity(self):
        # Remplir la base de données avec des réservations atteignant la capacité maximale
        for _ in range(50):  # Supposons que chaque réservation est pour 1 personne
            TableReservation.objects.create(
                name='Existing Reservation',
                email='existing@example.com',
                phone='123456789',
                date=date.today(),
                time=time(18, 0),
                people=1,
                message='Test'
            )

        # Tenter de faire une autre réservation pour le jour actuel
        response = self.client.post(reverse('book-a-table'), {  # Utilisez 'book_table' au lieu de 'book-a-table'
            'name': 'New Reservation',
            'email': 'new@example.com',
            'phone': '987654321',
            'date': date.today(),
            'time': time(18, 0),
            'people': 1,
            'message': 'Test'
        })

        # Vérifier que la réservation n'a pas été acceptée car la capacité est atteinte
        self.assertNotEqual(response.status_code, 202)  # Redirection non attendue
        self.assertEqual(TableReservation.objects.count(), 50)  # Aucune nouvelle réservation ajoutée

