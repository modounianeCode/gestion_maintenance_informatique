import unittest

from src.maintenance.models.equipement import Equipement
from src.maintenance.models.enums import (
    PrioriteTicket,
    StatutTicket
)
from src.maintenance.models.intervention import Intervention
from src.maintenance.models.utilisateur import (
    Demandeur,
    Technicien
)
from src.maintenance.repositories.ticket_repository import (
    TicketRepository
)
from src.maintenance.services.ticket_service import TicketService


class TestTicketService(unittest.TestCase):
    def setUp(self):
        self.repository = TicketRepository()
        self.service = TicketService(self.repository)

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

    def test_creer_ticket_via_service(self):
        ticket = self.service.creer_ticket(
            identifiant=1,
            titre="Écran noir",
            description="L'ordinateur démarre, mais l'écran reste noir.",
            createur=self.demandeur,
            equipement=self.equipement,
            priorite=PrioriteTicket.HAUTE
        )

        self.assertEqual(ticket.identifiant, 1)
        self.assertEqual(ticket.statut, StatutTicket.OUVERT)

        ticket_trouve = self.repository.trouver_par_id(1)
        self.assertEqual(ticket_trouve, ticket)

    def test_parcours_complet_ticket_via_service(self):
        ticket = self.service.creer_ticket(
            identifiant=1,
            titre="Connexion Internet instable",
            description="La connexion se coupe régulièrement.",
            createur=self.demandeur,
            equipement=self.equipement
        )

        self.service.assigner_technicien(
            identifiant_ticket=ticket.identifiant,
            technicien=self.technicien
        )

        intervention = Intervention(
            identifiant=1,
            description="Vérification du câble réseau.",
            duree_minutes=20,
            technicien=self.technicien
        )

        self.service.ajouter_intervention(
            identifiant_ticket=ticket.identifiant,
            intervention=intervention,
            auteur=self.technicien
        )

        self.service.resoudre_ticket(ticket.identifiant)
        self.service.fermer_ticket(ticket.identifiant)

        ticket_final = self.repository.trouver_par_id(
            ticket.identifiant
        )

        self.assertEqual(ticket_final.statut, StatutTicket.FERME)

    def test_lister_tickets_par_priorite(self):
        self.service.creer_ticket(
            identifiant=1,
            titre="Panne réseau",
            description="Le routeur ne répond pas.",
            createur=self.demandeur,
            equipement=self.equipement,
            priorite=PrioriteTicket.CRITIQUE
        )

        tickets = self.service.lister_tickets(
            priorite=PrioriteTicket.CRITIQUE
        )

        self.assertEqual(len(tickets), 1)
        self.assertEqual(
            tickets[0].priorite,
            PrioriteTicket.CRITIQUE
        )

    def test_supprimer_ticket_via_service(self):
        ticket = self.service.creer_ticket(
            identifiant=1,
            titre="Souris défectueuse",
            description="La souris ne répond plus.",
            createur=self.demandeur,
            equipement=self.equipement
        )

        self.service.supprimer_ticket(ticket.identifiant)

        self.assertEqual(
            len(self.service.lister_tickets()),
            0
        )


if __name__ == "__main__":
    unittest.main()