import unittest

from src.maintenance.exceptions import (
    AutorisationRefuseeErreur,
    TechnicienNonAssigneErreur,
    TicketInvalideErreur,
    TransitionStatutInvalideErreur,
)
from src.maintenance.models.equipement import Equipement
from src.maintenance.models.enums import (
    PrioriteTicket,
    StatutTicket,
)
from src.maintenance.models.intervention import Intervention
from src.maintenance.models.ticket import Ticket
from src.maintenance.models.utilisateur import (
    Demandeur,
    Technicien,
)


class TestTicket(unittest.TestCase):
    def setUp(self):
        self.demandeur = Demandeur(
            identifiant=1,
            nom="Awa Diop",
            email="awa@example.com"
        )

        self.technicien = Technicien(
            identifiant=2,
            nom="Modou Niane",
            email="modou@example.com",
            specialite="maintenance informatique"
        )

        self.equipement = Equipement(
            identifiant=1,
            nom="Dell Latitude 5420",
            categorie="ordinateur",
            numero_serie="DL-2026-001"
        )

    def creer_ticket(self) -> Ticket:
        return Ticket(
            identifiant=1,
            titre="Ordinateur qui ne démarre pas",
            description="Le voyant est allumé, mais l'écran reste noir.",
            createur=self.demandeur,
            equipement=self.equipement,
            priorite=PrioriteTicket.HAUTE
        )

    def creer_intervention(self) -> Intervention:
        return Intervention(
            identifiant=1,
            description="Remplacement du câble d'alimentation.",
            duree_minutes=30,
            technicien=self.technicien
        )

    def test_nouveau_ticket_est_ouvert(self):
        ticket = self.creer_ticket()

        self.assertEqual(ticket.statut, StatutTicket.OUVERT)
        self.assertIsNone(ticket.technicien)
        self.assertEqual(ticket.nombre_interventions(), 0)
        self.assertEqual(ticket.duree_totale_interventions(), 0)

    def test_assignation_technicien_met_ticket_en_cours(self):
        ticket = self.creer_ticket()

        ticket.assigner_technicien(self.technicien)

        self.assertEqual(ticket.technicien, self.technicien)
        self.assertEqual(ticket.statut, StatutTicket.EN_COURS)

    def test_ticket_ne_peut_pas_etre_resolu_sans_technicien(self):
        ticket = self.creer_ticket()

        with self.assertRaises(TechnicienNonAssigneErreur):
            ticket.resoudre()

    def test_ticket_ne_peut_pas_etre_resolu_sans_intervention(self):
        ticket = self.creer_ticket()

        ticket.assigner_technicien(self.technicien)

        with self.assertRaises(TicketInvalideErreur):
            ticket.resoudre()

    def test_technicien_assigne_peut_ajouter_intervention(self):
        ticket = self.creer_ticket()
        ticket.assigner_technicien(self.technicien)

        intervention = self.creer_intervention()

        ticket.ajouter_intervention(
            intervention=intervention,
            auteur=self.technicien
        )

        self.assertEqual(ticket.nombre_interventions(), 1)
        self.assertEqual(ticket.duree_totale_interventions(), 30)
        self.assertEqual(
            ticket.interventions[0].description,
            "Remplacement du câble d'alimentation."
        )

    def test_autre_technicien_ne_peut_pas_intervenir(self):
        ticket = self.creer_ticket()

        autre_technicien = Technicien(
            identifiant=99,
            nom="Cheikh Fall",
            email="cheikh@example.com",
            specialite="reseau"
        )

        ticket.assigner_technicien(self.technicien)

        intervention = Intervention(
            identifiant=2,
            description="Tentative de diagnostic réseau.",
            duree_minutes=15,
            technicien=autre_technicien
        )

        with self.assertRaises(AutorisationRefuseeErreur):
            ticket.ajouter_intervention(
                intervention=intervention,
                auteur=autre_technicien
            )

    def test_ticket_resolu_peut_etre_ferme(self):
        ticket = self.creer_ticket()

        ticket.assigner_technicien(self.technicien)

        intervention = self.creer_intervention()

        ticket.ajouter_intervention(
            intervention=intervention,
            auteur=self.technicien
        )

        ticket.resoudre()
        ticket.fermer()

        self.assertEqual(ticket.statut, StatutTicket.FERME)
        self.assertIsNotNone(ticket.resolu_le)
        self.assertIsNotNone(ticket.ferme_le)
        self.assertTrue(ticket.est_ferme())

    def test_ticket_non_resolu_ne_peut_pas_etre_ferme(self):
        ticket = self.creer_ticket()

        with self.assertRaises(TransitionStatutInvalideErreur):
            ticket.fermer()

    def test_ticket_ferme_ne_peut_plus_recevoir_intervention(self):
        ticket = self.creer_ticket()

        ticket.assigner_technicien(self.technicien)

        premiere_intervention = self.creer_intervention()

        ticket.ajouter_intervention(
            intervention=premiere_intervention,
            auteur=self.technicien
        )

        ticket.resoudre()
        ticket.fermer()

        nouvelle_intervention = Intervention(
            identifiant=10,
            description="Nouvelle tentative après fermeture.",
            duree_minutes=10,
            technicien=self.technicien
        )

        with self.assertRaises(TransitionStatutInvalideErreur):
            ticket.ajouter_intervention(
                intervention=nouvelle_intervention,
                auteur=self.technicien
            )

    def test_equipement_non_disponible_ne_peut_pas_avoir_ticket(self):
        self.equipement.declarer_en_panne()

        with self.assertRaises(TicketInvalideErreur):
            self.creer_ticket()

    def test_titre_vide_declenche_erreur(self):
        with self.assertRaises(TicketInvalideErreur):
            Ticket(
                identifiant=9,
                titre="   ",
                description="Description valide.",
                createur=self.demandeur,
                equipement=self.equipement
            )

    def test_resume_du_ticket_contient_les_informations_utiles(self):
        ticket = self.creer_ticket()

        ticket.assigner_technicien(self.technicien)

        resume = ticket.afficher_resume()

        self.assertIn("Ticket #1", resume)
        self.assertIn("Ordinateur qui ne démarre pas", resume)
        self.assertIn("en_cours", resume)
        self.assertIn("Modou Niane", resume)


if __name__ == "__main__":
    unittest.main()