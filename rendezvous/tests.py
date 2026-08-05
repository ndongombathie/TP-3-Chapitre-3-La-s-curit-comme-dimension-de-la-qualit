from datetime import date

from django.test import TestCase

from patients.models import Patient

from .models import TypeConsultation
from .services import RendezVousService, TarifCalculator

# Le 21/07/2026 est un mardi (semaine), le 25/07/2026 est un samedi (weekend).


class TarifCalculatorTest(TestCase):
    def setUp(self):
        self.calculator = TarifCalculator()

    def test_tarif_de_base_semaine_sans_vip(self):
        prix = self.calculator.calculer(TypeConsultation.GENERALISTE, date(2026, 7, 21), False)
        self.assertEqual(prix, 5000)

    def test_majoration_weekend_specialiste(self):
        prix = self.calculator.calculer(TypeConsultation.SPECIALISTE, date(2026, 7, 25), False)
        self.assertEqual(prix, 12000)  # 10000 + 20%

    def test_reduction_vip_urgence(self):
        prix = self.calculator.calculer(TypeConsultation.URGENCE, date(2026, 7, 21), True)
        self.assertEqual(prix, 13500)  # 15000 - 10%

    def test_cumul_majoration_weekend_et_reduction_vip(self):
        prix = self.calculator.calculer(TypeConsultation.SPECIALISTE, date(2026, 7, 25), True)
        self.assertAlmostEqual(prix, 10800)  # 10000 * 1.20 * 0.90

    def test_type_inconnu_leve_une_erreur(self):
        with self.assertRaises(ValueError):
            self.calculator.calculer("INCONNU", date(2026, 7, 21), False)


class RendezVousServiceTest(TestCase):
    def setUp(self):
        self.service = RendezVousService()
        self.patient = Patient.objects.create(
            nom="Ndiaye", prenom="Awa", email="awa@example.com", est_vip=False
        )

    def test_creer_rendez_vous_stocke_le_prix_calcule(self):
        rdv = self.service.creer_rendez_vous(self.patient, TypeConsultation.GENERALISTE, date(2026, 7, 21))
        self.assertEqual(float(rdv.prix), 5000.0)

    def test_facturer_patient_somme_les_rendez_vous(self):
        self.service.creer_rendez_vous(self.patient, TypeConsultation.GENERALISTE, date(2026, 7, 21))
        self.service.creer_rendez_vous(self.patient, TypeConsultation.SPECIALISTE, date(2026, 7, 21))
        self.assertEqual(float(self.service.facturer_patient(self.patient)), 15000.0)

    def test_facturer_patient_sans_rendez_vous_renvoie_zero(self):
        self.assertEqual(self.service.facturer_patient(self.patient), 0)
