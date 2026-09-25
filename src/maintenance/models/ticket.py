from datetime import datetime

from src.maintenance.exceptions import (
    AutorisationRefuseeErreur,
    TechnicienNonAssigneErreur,
    TicketInvalideErreur,
    TransitionStatutInvalideErreur
)
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


class Ticket:
    def __init__(
        self,
        identifiant: int,
        titre: str,
        description: str,
        createur: Demandeur,
        equipement: Equipement,
        priorite: PrioriteTicket = PrioriteTicket.MOYENNE
    ):
        if not titre.strip():
            raise TicketInvalideErreur(
                "Le titre du ticket est obligatoire."
            )

        if not description.strip():
            raise TicketInvalideErreur(
                "La description du ticket est obligatoire."
            )

        if not equipement.est_utilisable():
            raise TicketInvalideErreur(
                "Impossible de créer un ticket pour un équipement non disponible."
            )

        self.identifiant = identifiant
        self.titre = titre.strip()
        self.description = description.strip()
        self.createur = createur
        self.equipement = equipement
        self.priorite = priorite
        self.statut = StatutTicket.OUVERT
        self.technicien: Technicien | None = None
        self.interventions: list[Intervention] = []
        self.cree_le = datetime.now()
        self.resolu_le: datetime | None = None
        self.ferme_le: datetime | None = None

    def assigner_technicien(self, technicien: Technicien) -> None:
        if self.statut == StatutTicket.FERME:
            raise TransitionStatutInvalideErreur(
                "Impossible d'assigner un technicien à un ticket fermé."
            )

        self.technicien = technicien
        self.statut = StatutTicket.EN_COURS

    def ajouter_intervention(
        self,
        intervention: Intervention,
        auteur: Technicien
    ) -> None:
        if self.statut == StatutTicket.FERME:
            raise TransitionStatutInvalideErreur(
                "Impossible d'ajouter une intervention à un ticket fermé."
            )

        if self.technicien is None:
            raise TechnicienNonAssigneErreur(
                "Aucun technicien n'est assigné à ce ticket."
            )

        if auteur.identifiant != self.technicien.identifiant:
            raise AutorisationRefuseeErreur(
                "Seul le technicien assigné peut intervenir sur ce ticket."
            )

        if intervention.technicien.identifiant != auteur.identifiant:
            raise AutorisationRefuseeErreur(
                "Le technicien de l'intervention doit être son auteur."
            )

        self.interventions.append(intervention)

    def resoudre(self) -> None:
        if self.technicien is None:
            raise TechnicienNonAssigneErreur(
                "Un ticket ne peut pas être résolu sans technicien assigné."
            )

        if not self.interventions:
            raise TicketInvalideErreur(
                "Un ticket ne peut pas être résolu sans intervention."
            )

        if self.statut == StatutTicket.FERME:
            raise TransitionStatutInvalideErreur(
                "Un ticket fermé ne peut pas être résolu."
            )

        self.statut = StatutTicket.RESOLU
        self.resolu_le = datetime.now()

    def fermer(self) -> None:
        if self.statut != StatutTicket.RESOLU:
            raise TransitionStatutInvalideErreur(
                "Seul un ticket résolu peut être fermé."
            )

        self.statut = StatutTicket.FERME
        self.ferme_le = datetime.now()

    def est_ouvert(self) -> bool:
        return self.statut == StatutTicket.OUVERT

    def est_ferme(self) -> bool:
        return self.statut == StatutTicket.FERME

    def nombre_interventions(self) -> int:
        return len(self.interventions)

    def duree_totale_interventions(self) -> int:
        return sum(
            intervention.duree_minutes
            for intervention in self.interventions
        )

    def afficher_resume(self) -> str:
        nom_technicien = (
            self.technicien.nom
            if self.technicien is not None
            else "Non assigné"
        )

        return (
            f"Ticket #{self.identifiant} | "
            f"{self.titre} | "
            f"Statut : {self.statut.value} | "
            f"Priorité : {self.priorite.value} | "
            f"Technicien : {nom_technicien} | "
            f"Interventions : {self.nombre_interventions()} | "
            f"Durée totale : {self.duree_totale_interventions()} min"
        )