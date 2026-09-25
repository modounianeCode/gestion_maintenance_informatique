import json
from datetime import datetime
from pathlib import Path

from src.maintenance.exceptions import (
    TicketDejaExistantErreur,
    TicketIntrouvableErreur,
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


class JsonTicketRepository:
    def __init__(self, chemin_fichier: str | Path):
        self.chemin_fichier = Path(chemin_fichier)
        self.chemin_fichier.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def _lire_donnees(self) -> list[dict]:
        if not self.chemin_fichier.exists():
            return []

        contenu = self.chemin_fichier.read_text(
            encoding="utf-8"
        ).strip()

        if not contenu:
            return []

        return json.loads(contenu)

    def _ecrire_donnees(self, donnees: list[dict]) -> None:
        contenu = json.dumps(
            donnees,
            ensure_ascii=False,
            indent=2
        )

        self.chemin_fichier.write_text(
            contenu,
            encoding="utf-8"
        )

    def _utilisateur_vers_dict(
        self,
        utilisateur: Demandeur | Technicien
    ) -> dict:
        donnees = {
            "identifiant": utilisateur.identifiant,
            "nom": utilisateur.nom,
            "email": utilisateur.email,
            "role": utilisateur.role,
        }

        if isinstance(utilisateur, Technicien):
            donnees["specialite"] = utilisateur.specialite

        return donnees

    def _utilisateur_depuis_dict(
        self,
        donnees: dict
    ) -> Demandeur | Technicien:
        if donnees["role"] == "technicien":
            return Technicien(
                identifiant=donnees["identifiant"],
                nom=donnees["nom"],
                email=donnees["email"],
                specialite=donnees.get(
                    "specialite",
                    "maintenance informatique"
                )
            )

        return Demandeur(
            identifiant=donnees["identifiant"],
            nom=donnees["nom"],
            email=donnees["email"]
        )

    def _equipement_vers_dict(
        self,
        equipement: Equipement
    ) -> dict:
        return {
            "identifiant": equipement.identifiant,
            "nom": equipement.nom,
            "categorie": equipement.categorie,
            "numero_serie": equipement.numero_serie,
            "statut": equipement.statut,
        }

    def _equipement_depuis_dict(
        self,
        donnees: dict
    ) -> Equipement:
        return Equipement(
            identifiant=donnees["identifiant"],
            nom=donnees["nom"],
            categorie=donnees["categorie"],
            numero_serie=donnees["numero_serie"],
            statut=donnees["statut"],
        )

    def _intervention_vers_dict(
        self,
        intervention: Intervention
    ) -> dict:
        return {
            "identifiant": intervention.identifiant,
            "description": intervention.description,
            "duree_minutes": intervention.duree_minutes,
            "technicien": self._utilisateur_vers_dict(
                intervention.technicien
            ),
            "cree_le": intervention.cree_le.isoformat(),
        }

    def _intervention_depuis_dict(
        self,
        donnees: dict
    ) -> Intervention:
        technicien = self._utilisateur_depuis_dict(
            donnees["technicien"]
        )

        intervention = Intervention(
            identifiant=donnees["identifiant"],
            description=donnees["description"],
            duree_minutes=donnees["duree_minutes"],
            technicien=technicien,
        )

        intervention.cree_le = datetime.fromisoformat(
            donnees["cree_le"]
        )

        return intervention

    def _ticket_vers_dict(self, ticket: Ticket) -> dict:
        return {
            "identifiant": ticket.identifiant,
            "titre": ticket.titre,
            "description": ticket.description,
            "createur": self._utilisateur_vers_dict(
                ticket.createur
            ),
            "equipement": self._equipement_vers_dict(
                ticket.equipement
            ),
            "priorite": ticket.priorite.value,
            "statut": ticket.statut.value,
            "technicien": (
                self._utilisateur_vers_dict(ticket.technicien)
                if ticket.technicien is not None
                else None
            ),
            "interventions": [
                self._intervention_vers_dict(intervention)
                for intervention in ticket.interventions
            ],
            "cree_le": ticket.cree_le.isoformat(),
            "resolu_le": (
                ticket.resolu_le.isoformat()
                if ticket.resolu_le is not None
                else None
            ),
            "ferme_le": (
                ticket.ferme_le.isoformat()
                if ticket.ferme_le is not None
                else None
            ),
        }

    def _ticket_depuis_dict(self, donnees: dict) -> Ticket:
        createur = self._utilisateur_depuis_dict(
            donnees["createur"]
        )

        equipement = self._equipement_depuis_dict(
            donnees["equipement"]
        )

        ticket = Ticket(
            identifiant=donnees["identifiant"],
            titre=donnees["titre"],
            description=donnees["description"],
            createur=createur,
            equipement=equipement,
            priorite=PrioriteTicket(donnees["priorite"]),
        )

        if donnees["technicien"] is not None:
            technicien = self._utilisateur_depuis_dict(
                donnees["technicien"]
            )

            ticket.technicien = technicien

        ticket.statut = StatutTicket(donnees["statut"])

        ticket.interventions = [
            self._intervention_depuis_dict(intervention)
            for intervention in donnees["interventions"]
        ]

        ticket.cree_le = datetime.fromisoformat(
            donnees["cree_le"]
        )

        if donnees["resolu_le"] is not None:
            ticket.resolu_le = datetime.fromisoformat(
                donnees["resolu_le"]
            )

        if donnees["ferme_le"] is not None:
            ticket.ferme_le = datetime.fromisoformat(
                donnees["ferme_le"]
            )

        return ticket

    def _charger_tickets(self) -> dict[int, Ticket]:
        donnees = self._lire_donnees()

        return {
            ticket_dict["identifiant"]: self._ticket_depuis_dict(
                ticket_dict
            )
            for ticket_dict in donnees
        }

    def _sauvegarder_tickets(
        self,
        tickets: dict[int, Ticket]
    ) -> None:
        donnees = [
            self._ticket_vers_dict(ticket)
            for ticket in tickets.values()
        ]

        self._ecrire_donnees(donnees)

    def ajouter(self, ticket: Ticket) -> None:
        tickets = self._charger_tickets()

        if ticket.identifiant in tickets:
            raise TicketDejaExistantErreur(
                f"Le ticket #{ticket.identifiant} existe déjà."
            )

        tickets[ticket.identifiant] = ticket
        self._sauvegarder_tickets(tickets)

    def trouver_par_id(self, identifiant: int) -> Ticket:
        tickets = self._charger_tickets()

        ticket = tickets.get(identifiant)

        if ticket is None:
            raise TicketIntrouvableErreur(
                f"Le ticket #{identifiant} est introuvable."
            )

        return ticket

    def lister_tous(self) -> list[Ticket]:
        tickets = self._charger_tickets()

        return list(tickets.values())

    def supprimer(self, identifiant: int) -> None:
        tickets = self._charger_tickets()

        if identifiant not in tickets:
            raise TicketIntrouvableErreur(
                f"Le ticket #{identifiant} est introuvable."
            )

        del tickets[identifiant]

        self._sauvegarder_tickets(tickets)

    def mettre_a_jour(self, ticket: Ticket) -> None:
        tickets = self._charger_tickets()

        if ticket.identifiant not in tickets:
            raise TicketIntrouvableErreur(
                f"Le ticket #{ticket.identifiant} est introuvable."
            )

        tickets[ticket.identifiant] = ticket

        self._sauvegarder_tickets(tickets)

    def filtrer_par_statut(
        self,
        statut: StatutTicket
    ) -> list[Ticket]:
        return [
            ticket
            for ticket in self.lister_tous()
            if ticket.statut == statut
        ]

    def filtrer_par_priorite(
        self,
        priorite: PrioriteTicket
    ) -> list[Ticket]:
        return [
            ticket
            for ticket in self.lister_tous()
            if ticket.priorite == priorite
        ]

    def filtrer_par_technicien(
        self,
        identifiant_technicien: int
    ) -> list[Ticket]:
        return [
            ticket
            for ticket in self.lister_tous()
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
            for ticket in self.lister_tous()
            if mot_cle_normalise in ticket.titre.lower()
            or mot_cle_normalise in ticket.description.lower()
        ]