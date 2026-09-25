from src.maintenance.exceptions import (
    TicketDejaExistantErreur,
    TicketIntrouvableErreur
)
from src.maintenance.models.enums import (
    PrioriteTicket,
    StatutTicket
)
from src.maintenance.models.ticket import Ticket
from src.maintenance.models.utilisateur import Technicien


class TicketRepository:
    def __init__(self):
        self._tickets: dict[int, Ticket] = {}

    def ajouter(self, ticket: Ticket) -> None:
        if ticket.identifiant in self._tickets:
            raise TicketDejaExistantErreur(
                f"Le ticket #{ticket.identifiant} existe déjà."
            )

        self._tickets[ticket.identifiant] = ticket

    def trouver_par_id(self, identifiant: int) -> Ticket:
        ticket = self._tickets.get(identifiant)

        if ticket is None:
            raise TicketIntrouvableErreur(
                f"Le ticket #{identifiant} est introuvable."
            )

        return ticket

    def lister_tous(self) -> list[Ticket]:
        return list(self._tickets.values())

    def supprimer(self, identifiant: int) -> None:
        if identifiant not in self._tickets:
            raise TicketIntrouvableErreur(
                f"Le ticket #{identifiant} est introuvable."
            )

        del self._tickets[identifiant]

    def filtrer_par_statut(
        self,
        statut: StatutTicket
    ) -> list[Ticket]:
        return [
            ticket
            for ticket in self._tickets.values()
            if ticket.statut == statut
        ]

    def filtrer_par_priorite(
        self,
        priorite: PrioriteTicket
    ) -> list[Ticket]:
        return [
            ticket
            for ticket in self._tickets.values()
            if ticket.priorite == priorite
        ]

    def filtrer_par_technicien(
        self,
        identifiant_technicien: int
    ) -> list[Ticket]:
        return [
            ticket
            for ticket in self._tickets.values()
            if ticket.technicien is not None
            and ticket.technicien.identifiant == identifiant_technicien
        ]

    def rechercher_par_mot_cle(
        self,
        mot_cle: str
    ) -> list[Ticket]:
        mot_cle_normalise = mot_cle.lower().strip()

        return [
            ticket
            for ticket in self._tickets.values()
            if mot_cle_normalise in ticket.titre.lower()
            or mot_cle_normalise in ticket.description.lower()
        ]

    def mettre_a_jour(self, ticket: Ticket) -> None:
        if ticket.identifiant not in self._tickets:
            raise TicketIntrouvableErreur(
                f"Le ticket #{ticket.identifiant} est introuvable."
            )

        self._tickets[ticket.identifiant] = ticket