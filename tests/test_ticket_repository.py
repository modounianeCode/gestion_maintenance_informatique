import unittest

from src.maintenance.exceptions import (
    TicketDejaExistantErreur,
    TicketIntrouvableErreur
)
from src.maintenance.models.equipement import Equipement
from src.maintenance.models.enums import (
    PrioriteTicket,
    StatutTicket
)
from src.maintenance.models.ticket import Ticket
from src.maintenance.models.utilisateur import (
    Demandeur,
    Technicien
)
from src.maintenance.repositories.ticket_repository import (
    TicketRepository
)


class TestTicketRepository(unittest.TestCase):
    def setUp(self):
        self.repository = TicketRepository()

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
        identifiant: int = 1,
        titre: str = "Ordinateur qui ne démarre pas",
        description: str = "Le voyant est allumé, mais l'écran reste noir.",
        priorite: PrioriteTicket = PrioriteTicket.HAUTE
    ) -> Ticket:
        return Ticket(
            identifiant=identifiant,
            titre=titre,
            description=description,
            createur=self.demandeur,
            equipement=self.equipement,
            priorite=priorite
        )

    def test_ajouter_et_trouver_ticket(self):
        ticket = self.creer_ticket()

        self.repository.ajouter(ticket)

        ticket_trouve = self.repository.trouver_par_id(1)

        self.assertEqual(ticket_trouve, ticket)

    def test_ajouter_ticket_avec_identifiant_existant_declenche_erreur(self):
        self.repository.ajouter(self.creer_ticket())

        with self.assertRaises(TicketDejaExistantErreur):
            self.repository.ajouter(self.creer_ticket())

    def test_ticket_inexistant_declenche_erreur(self):
        with self.assertRaises(TicketIntrouvableErreur):
            self.repository.trouver_par_id(999)

    def test_lister_tous_les_tickets(self):
        self.repository.ajouter(self.creer_ticket(1))
        self.repository.ajouter(
            self.creer_ticket(
                identifiant=2,
                titre="Imprimante bloquée"
            )
        )

        tickets = self.repository.lister_tous()

        self.assertEqual(len(tickets), 2)

    def test_supprimer_ticket(self):
        self.repository.ajouter(self.creer_ticket())

        self.repository.supprimer(1)

        with self.assertRaises(TicketIntrouvableErreur):
            self.repository.trouver_par_id(1)

    def test_filtrer_par_statut(self):
        ticket_ouvert = self.creer_ticket(1)

        ticket_en_cours = self.creer_ticket(
            identifiant=2,
            titre="Imprimante bloquée"
        )
        ticket_en_cours.assigner_technicien(self.technicien)

        self.repository.ajouter(ticket_ouvert)
        self.repository.ajouter(ticket_en_cours)

        tickets = self.repository.filtrer_par_statut(
            StatutTicket.EN_COURS
        )

        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0].identifiant, 2)

    def test_filtrer_par_priorite(self):
        ticket_haute = self.creer_ticket(
            identifiant=1,
            priorite=PrioriteTicket.HAUTE
        )

        ticket_basse = self.creer_ticket(
            identifiant=2,
            titre="Nettoyage ordinateur",
            priorite=PrioriteTicket.BASSE
        )

        self.repository.ajouter(ticket_haute)
        self.repository.ajouter(ticket_basse)

        tickets = self.repository.filtrer_par_priorite(
            PrioriteTicket.BASSE
        )

        self.assertEqual(len(tickets), 1)
        self.assertEqual(
            tickets[0].priorite,
            PrioriteTicket.BASSE
        )

    def test_filtrer_par_technicien(self):
        ticket_assigne = self.creer_ticket(1)
        ticket_assigne.assigner_technicien(self.technicien)

        ticket_non_assigne = self.creer_ticket(
            identifiant=2,
            titre="Routeur indisponible"
        )

        self.repository.ajouter(ticket_assigne)
        self.repository.ajouter(ticket_non_assigne)

        tickets = self.repository.filtrer_par_technicien(
            self.technicien.identifiant
        )

        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0].identifiant, 1)

    def test_rechercher_par_mot_cle(self):
        ticket = self.creer_ticket(
            identifiant=1,
            titre="Imprimante bloquée",
            description="Le papier est coincé dans l'imprimante."
        )

        self.repository.ajouter(ticket)

        tickets = self.repository.rechercher_par_mot_cle(
            "papier"
        )

        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0].identifiant, 1)


if __name__ == "__main__":
    unittest.main()