import unittest

from src.maintenance.models.utilisateur import (
    Technicien,
    Utilisateur
)

class TestUtilisateur(unittest.TestCase):
    def test_demandeur_ne_est_pas_technicien(self):
        demandeur = Utilisateur(
            identifiant=10,
            nom="Awa Diop",
            email="awa@example.com",
            role="demandeur"
        )

        self.assertFalse(demandeur.est_technicien())

    def test_technicien_a_permissions_de_traitement(self):
        technicien = Technicien(
            identifiant=11,
            nom="Modou Niane",
            email="modou@example.com",
            specialite="maintenance informatique"
        )

        self.assertIn(
            "prendre_en_charge_ticket",
            technicien.permissions()
        )
        self.assertIn(
            "ajouter_intervention",
            technicien.permissions()
        )

    def test_creation_utilisateur_valide(self):
        utilisateur = Technicien(
            identifiant=1,
            nom="Modou Niane",
            email="modou@example.com",
            specialite="maintenance informatique"
        )

        self.assertEqual(utilisateur.nom, "Modou Niane")
        self.assertEqual(utilisateur.email, "modou@example.com")
        self.assertTrue(utilisateur.est_technicien())
        self.assertEqual(utilisateur.role, "technicien")
        self.assertEqual(
            utilisateur.specialite,
            "maintenance informatique"
        )

    def test_email_est_normalise(self):
        utilisateur = Utilisateur(
            identifiant=2,
            nom="Awa Diop",
            email=" AWA@EXAMPLE.COM ",
            role="demandeur"
        )

        self.assertEqual(utilisateur.email, "awa@example.com")

    def test_email_invalide_declenche_une_erreur(self):
        with self.assertRaises(ValueError):
            Utilisateur(
                identifiant=3,
                nom="Ibrahima Fall",
                email="ibrahima.sans.arobase",
                role="demandeur"
            )

    def test_role_invalide_declenche_une_erreur(self):
        with self.assertRaises(ValueError):
            Utilisateur(
                identifiant=4,
                nom="Fatou Ndiaye",
                email="fatou@example.com",
                role="directeur"
            )


if __name__ == "__main__":
    unittest.main()