from django.test import TestCase

from patients.models import Patient

# Create your tests here.

class PatientSearchTestCase(TestCase):
    
    def setUp(self):
        # Create some test patients
        Patient.objects.create(nom="diop", prenom="saliou")
        Patient.objects.create(nom="mbaye", prenom="modou")
        Patient.objects.create(nom="ndiaye", prenom="fatou")
        Patient.objects.create(nom="mbath", prenom="ndongo")
        
    def test_search_patient(self):
        # test qui aurait échoué avant votre correctif.
        response = self.client.get('/patients/recherche/', {'q': "' OR '1'='1"})
        self.assertEqual(response.context["resultats"].count(), 0)
