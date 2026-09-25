from src.maintenance.models.enums import (
    PrioriteTicket,
    StatutTicket
)
from src.maintenance.models.equipement import Equipement
from src.maintenance.models.intervention import Intervention
from src.maintenance.models.ticket import Ticket
from src.maintenance.models.utilisateur import (
    Demandeur,
    Technicien
)
from src.maintenance.repositories.ticket_repository import (
    TicketRepository
)


class TicketService:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def creer_ticket(
        self,
        identifiant: int,
        titre: str,
        description: str,
        createur: Demandeur,
        equipement: Equipement,
        priorite: PrioriteTicket = PrioriteTicket.MOYENNE
    ) -> Ticket:
        ticket = Ticket(
            identifiant=identifiant,
            titre=titre,
            description=description,
            createur=createur,
            equipement=equipement,
            priorite=priorite
        )

        self.repository.ajouter(ticket)

        return ticket

    def assigner_technicien(
        self,
        identifiant_ticket: int,
        technicien: Technicien
    ) -> Ticket:
        ticket = self.repository.trouver_par_id(
            identifiant_ticket
        )

        ticket.assigner_technicien(technicien)
        self.repository.mettre_a_jour(ticket)
        return ticket

    def ajouter_intervention(
        self,
        identifiant_ticket: int,
        intervention: Intervention,
        auteur: Technicien
    ) -> Ticket:
        ticket = self.repository.trouver_par_id(
            identifiant_ticket
        )

        ticket.ajouter_intervention(
            intervention=intervention,
            auteur=auteur
        )
        self.repository.mettre_a_jour(ticket)
        return ticket

    def resoudre_ticket(
        self,
        identifiant_ticket: int
    ) -> Ticket:
        ticket = self.repository.trouver_par_id(
            identifiant_ticket
        )

        ticket.resoudre()
        self.repository.mettre_a_jour(ticket)
        return ticket

    def fermer_ticket(
        self,
        identifiant_ticket: int
    ) -> Ticket:
        ticket = self.repository.trouver_par_id(
            identifiant_ticket
        )

        ticket.fermer()
        self.repository.mettre_a_jour(ticket)
        return ticket

    def lister_tickets(
            self,
            statut: StatutTicket | None = None,
            priorite: PrioriteTicket | None = None,
            identifiant_technicien: int | None = None,
            mot_cle: str | None = None
    ) -> list[Ticket]:
        tickets = self.repository.lister_tous()

        if statut is not None:
            tickets = [
                ticket
                for ticket in tickets
                if ticket.statut == statut
            ]

        if priorite is not None:
            tickets = [
                ticket
                for ticket in tickets
                if ticket.priorite == priorite
            ]

        if identifiant_technicien is not None:
            tickets = [
                ticket
                for ticket in tickets
                if ticket.technicien is not None
                   and ticket.technicien.identifiant
                   == identifiant_technicien
            ]

        if mot_cle is not None:
            mot_cle_normalise = mot_cle.lower().strip()

            tickets = [
                ticket
                for ticket in tickets
                if mot_cle_normalise in ticket.titre.lower()
                   or mot_cle_normalise in ticket.description.lower()
            ]

        return sorted(
            tickets,
            key=lambda ticket: ticket.cree_le,
            reverse=True
        )

    def obtenir_statistiques(self) -> dict:
        tickets = self.repository.lister_tous()

        statistiques = {
            "total": len(tickets),
            "ouvert": 0,
            "en_cours": 0,
            "resolu": 0,
            "ferme": 0,
            "basse": 0,
            "moyenne": 0,
            "haute": 0,
            "critique": 0,
            "duree_totale_interventions": 0,
        }

        for ticket in tickets:
            statistiques[ticket.statut.value] += 1
            statistiques[ticket.priorite.value] += 1
            statistiques[
                "duree_totale_interventions"
            ] += ticket.duree_totale_interventions()

        return statistiques
    def supprimer_ticket(self, identifiant_ticket: int) -> None:
        self.repository.supprimer(identifiant_ticket)