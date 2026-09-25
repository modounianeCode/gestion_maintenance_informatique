class ErreurMaintenance(Exception):
    """Classe de base pour les erreurs métier du projet."""


class TicketInvalideErreur(ErreurMaintenance):
    """Le ticket contient des données ou un état invalide."""


class TransitionStatutInvalideErreur(ErreurMaintenance):
    """Le changement de statut demandé n'est pas autorisé."""


class TechnicienNonAssigneErreur(ErreurMaintenance):
    """L'action exige un technicien assigné au ticket."""


class InterventionInvalideErreur(ErreurMaintenance):
    """L'intervention contient des informations invalides."""


class AutorisationRefuseeErreur(ErreurMaintenance):
    """L'utilisateur ne possède pas le droit d'effectuer cette action."""

class TicketIntrouvableErreur(ErreurMaintenance):
    """Le ticket demandé n'existe pas."""


class TicketDejaExistantErreur(ErreurMaintenance):
    """Un ticket avec cet identifiant existe déjà."""