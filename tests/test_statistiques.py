import unittest

from src.maintenance.models.equipement import Equipement
from src.maintenance.models.enums import (
    PrioriteTicket,
)
from src.maintenance.models.intervention import Intervention
from src.maintenance.models.utilisateur import (
    Demandeur,
    Technicien,
)
from src.maintenance.repositories.ticket_repository import (
    TicketRepository,
)
from src.maintenance.services.ticket_service import TicketService


class TestStatistiques(unittest.TestCase):
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

    def creer_ticket(
        self,
        identifiant: int,
        titre: str,
        priorite: PrioriteTicket
    ):
        return self.service.creer_ticket(
            identifiant=identifiant,
            titre=titre,
            description=f"Description du ticket : {titre}.",
            createur=self.demandeur,
            equipement=self.equipement,
            priorite=priorite
        )

    def test_statistiques_sans_ticket(self):
        statistiques = self.service.obtenir_statistiques()

        self.assertEqual(statistiques["total"], 0)
        self.assertEqual(statistiques["ouvert"], 0)
        self.assertEqual(
            statistiques["duree_totale_interventions"],
            0
        )

    def test_statistiques_avec_tickets(self):
        ticket_1 = self.creer_ticket(
            identifiant=1,
            titre="Écran noir",
            priorite=PrioriteTicket.HAUTE
        )

        ticket_2 = self.creer_ticket(
            identifiant=2,
            titre="Imprimante bloquée",
            priorite=PrioriteTicket.MOYENNE
        )

        self.service.assigner_technicien(
            identifiant_ticket=ticket_1.identifiant,
            technicien=self.technicien
        )

        intervention = Intervention(
            identifiant=1,
            description="Vérification du câble d'alimentation.",
            duree_minutes=25,
            technicien=self.technicien
        )

        self.service.ajouter_intervention(
            identifiant_ticket=ticket_1.identifiant,
            intervention=intervention,
            auteur=self.technicien
        )

        statistiques = self.service.obtenir_statistiques()

        self.assertEqual(statistiques["total"], 2)
        self.assertEqual(statistiques["ouvert"], 1)
        self.assertEqual(statistiques["en_cours"], 1)
        self.assertEqual(statistiques["haute"], 1)
        self.assertEqual(statistiques["moyenne"], 1)
        self.assertEqual(
            statistiques["duree_totale_interventions"],
            25
        )


if __name__ == "__main__":
    unittest.main()