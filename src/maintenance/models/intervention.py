from dataclasses import dataclass, field
from datetime import datetime

from src.maintenance.exceptions import InterventionInvalideErreur
from src.maintenance.models.utilisateur import Technicien


@dataclass
class Intervention:
    identifiant: int
    description: str
    duree_minutes: int
    technicien: Technicien
    cree_le: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        self.description = self.description.strip()

        if not self.description:
            raise InterventionInvalideErreur(
                "La description de l'intervention est obligatoire."
            )

        if self.duree_minutes <= 0:
            raise InterventionInvalideErreur(
                "La durée de l'intervention doit être supérieure à zéro."
            )

    def est_longue(self) -> bool:
        return self.duree_minutes > 120

    def afficher_resume(self) -> str:
        return (
            f"Intervention #{self.identifiant} | "
            f"Technicien : {self.technicien.nom} | "
            f"Durée : {self.duree_minutes} minutes | "
            f"Description : {self.description}"
        )
