import unittest

from src.maintenance.exceptions import InterventionInvalideErreur
from src.maintenance.models.intervention import Intervention
from src.maintenance.models.utilisateur import Technicien


class TestIntervention(unittest.TestCase):
    def setUp(self):
        self.technicien = Technicien(
            identifiant=1,
            nom="Modou Niane",
            email="modou@example.com",
            specialite="maintenance informatique"
        )

    def test_intervention_valide(self):
        intervention = Intervention(
            identifiant=1,
            description="Nettoyage de l'ordinateur.",
            duree_minutes=45,
            technicien=self.technicien
        )

        self.assertEqual(
            intervention.description,
            "Nettoyage de l'ordinateur."
        )
        self.assertFalse(intervention.est_longue())

    def test_intervention_longue(self):
        intervention = Intervention(
            identifiant=2,
            description="Réinstallation complète du système.",
            duree_minutes=150,
            technicien=self.technicien
        )

        self.assertTrue(intervention.est_longue())

    def test_description_vide_declenche_erreur(self):
        with self.assertRaises(InterventionInvalideErreur):
            Intervention(
                identifiant=3,
                description="   ",
                duree_minutes=20,
                technicien=self.technicien
            )

    def test_duree_invalide_declenche_erreur(self):
        with self.assertRaises(InterventionInvalideErreur):
            Intervention(
                identifiant=4,
                description="Diagnostic matériel.",
                duree_minutes=0,
                technicien=self.technicien
            )
if __name__ == "__main__":
    unittest.main()