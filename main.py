import argparse

from src.maintenance.exceptions import ErreurMaintenance
from src.maintenance.models.equipement import Equipement
from src.maintenance.models.enums import (
    PrioriteTicket,
    StatutTicket,
)
from src.maintenance.models.intervention import Intervention
from src.maintenance.models.utilisateur import (
    Demandeur,
    Technicien,
)
from src.maintenance.repositories.json_ticket_repository import (
    JsonTicketRepository,
)
from src.maintenance.services.ticket_service import TicketService


CHEMIN_DONNEES = "data/tickets.json"


def creer_service() -> TicketService:
    repository = JsonTicketRepository(CHEMIN_DONNEES)

    return TicketService(repository)


def creer_demandeur_demo() -> Demandeur:
    return Demandeur(
        identifiant=1,
        nom="Awa Diop",
        email="awa@example.com"
    )


def creer_technicien_demo() -> Technicien:
    return Technicien(
        identifiant=2,
        nom="Modou Niane",
        email="modou@example.com",
        specialite="maintenance informatique"
    )


def creer_equipement_demo() -> Equipement:
    return Equipement(
        identifiant=1,
        nom="Dell Latitude 5420",
        categorie="ordinateur",
        numero_serie="DL-2026-001"
    )


def afficher_tickets(tickets: list) -> None:
    if not tickets:
        print("\nAucun ticket trouvé.")
        return

    print("\n--- Liste des tickets ---")

    for ticket in tickets:
        print(ticket.afficher_resume())

    print(f"\nTotal : {len(tickets)} ticket(s).")


def afficher_ticket(ticket) -> None:
    print("\n--- Détail du ticket ---")
    print(ticket.afficher_resume())
    print(f"Créateur : {ticket.createur.nom}")
    print(f"Équipement : {ticket.equipement.nom}")
    print(f"Description : {ticket.description}")
    print(f"Créé le : {ticket.cree_le.strftime('%d/%m/%Y %H:%M')}")

    if ticket.technicien is not None:
        print(
            "Technicien : "
            f"{ticket.technicien.nom} "
            f"({ticket.technicien.specialite})"
        )

    if ticket.resolu_le is not None:
        print(
            "Résolu le : "
            f"{ticket.resolu_le.strftime('%d/%m/%Y %H:%M')}"
        )

    if ticket.ferme_le is not None:
        print(
            "Fermé le : "
            f"{ticket.ferme_le.strftime('%d/%m/%Y %H:%M')}"
        )

    print("\nInterventions :")

    if not ticket.interventions:
        print("- Aucune intervention enregistrée.")

    for intervention in ticket.interventions:
        print(
            f"- #{intervention.identifiant} | "
            f"{intervention.technicien.nom} | "
            f"{intervention.duree_minutes} min | "
            f"{intervention.description}"
        )


def commande_creer(args) -> None:
    service = creer_service()
    demandeur = creer_demandeur_demo()
    equipement = creer_equipement_demo()

    ticket = service.creer_ticket(
        identifiant=args.id,
        titre=args.titre,
        description=args.description,
        createur=demandeur,
        equipement=equipement,
        priorite=PrioriteTicket(args.priorite)
    )

    print("\nTicket créé avec succès.")
    afficher_ticket(ticket)


def commande_lister(args) -> None:
    service = creer_service()

    statut = (
        StatutTicket(args.statut)
        if args.statut is not None
        else None
    )

    priorite = (
        PrioriteTicket(args.priorite)
        if args.priorite is not None
        else None
    )

    tickets = service.lister_tickets(
        statut=statut,
        priorite=priorite,
        identifiant_technicien=args.technicien_id,
        mot_cle=args.mot_cle
    )

    afficher_tickets(tickets)


def commande_detail(args) -> None:
    service = creer_service()

    ticket = service.repository.trouver_par_id(args.ticket_id)

    afficher_ticket(ticket)


def commande_rechercher(args) -> None:
    service = creer_service()

    tickets = service.lister_tickets(
        mot_cle=args.mot_cle
    )

    afficher_tickets(tickets)


def commande_assigner(args) -> None:
    service = creer_service()
    technicien = creer_technicien_demo()

    ticket = service.assigner_technicien(
        identifiant_ticket=args.ticket_id,
        technicien=technicien
    )

    print("\nTechnicien assigné avec succès.")
    afficher_ticket(ticket)


def prochain_identifiant_intervention(ticket) -> int:
    if not ticket.interventions:
        return 1

    return max(
        intervention.identifiant
        for intervention in ticket.interventions
    ) + 1


def commande_intervenir(args) -> None:
    service = creer_service()
    technicien = creer_technicien_demo()

    ticket = service.repository.trouver_par_id(args.ticket_id)

    intervention = Intervention(
        identifiant=prochain_identifiant_intervention(ticket),
        description=args.description,
        duree_minutes=args.duree,
        technicien=technicien
    )

    ticket = service.ajouter_intervention(
        identifiant_ticket=args.ticket_id,
        intervention=intervention,
        auteur=technicien
    )

    print("\nIntervention ajoutée avec succès.")
    afficher_ticket(ticket)


def commande_resoudre(args) -> None:
    service = creer_service()

    ticket = service.resoudre_ticket(args.ticket_id)

    print("\nTicket résolu avec succès.")
    afficher_ticket(ticket)


def commande_fermer(args) -> None:
    service = creer_service()

    ticket = service.fermer_ticket(args.ticket_id)

    print("\nTicket fermé avec succès.")
    afficher_ticket(ticket)


def commande_supprimer(args) -> None:
    service = creer_service()

    service.supprimer_ticket(args.ticket_id)

    print(
        f"\nLe ticket #{args.ticket_id} "
        "a été supprimé avec succès."
    )

def commande_statistiques(args) -> None:
    service = creer_service()

    statistiques = service.obtenir_statistiques()

    print("\n=== STATISTIQUES DES TICKETS ===")
    print(f"Total : {statistiques['total']}")

    print("\nPar statut :")
    print(f"- Ouverts : {statistiques['ouvert']}")
    print(f"- En cours : {statistiques['en_cours']}")
    print(f"- Résolus : {statistiques['resolu']}")
    print(f"- Fermés : {statistiques['ferme']}")

    print("\nPar priorité :")
    print(f"- Basse : {statistiques['basse']}")
    print(f"- Moyenne : {statistiques['moyenne']}")
    print(f"- Haute : {statistiques['haute']}")
    print(f"- Critique : {statistiques['critique']}")

    print(
        "\nDurée totale des interventions : "
        f"{statistiques['duree_totale_interventions']} min"
    )
def creer_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Application de gestion de maintenance informatique."
        )
    )

    sous_commandes = parser.add_subparsers(
        dest="commande",
        required=True
    )

    parser_creer = sous_commandes.add_parser(
        "creer",
        help="Créer un nouveau ticket."
    )

    parser_creer.add_argument(
        "--id",
        type=int,
        required=True,
        help="Identifiant unique du ticket."
    )

    parser_creer.add_argument(
        "--titre",
        required=True,
        help="Titre du ticket."
    )

    parser_creer.add_argument(
        "--description",
        required=True,
        help="Description détaillée du problème."
    )

    parser_creer.add_argument(
        "--priorite",
        choices=[
            priorite.value
            for priorite in PrioriteTicket
        ],
        default=PrioriteTicket.MOYENNE.value,
        help="Priorité du ticket."
    )

    parser_creer.set_defaults(fonction=commande_creer)

    parser_lister = sous_commandes.add_parser(
        "lister",
        help="Lister les tickets enregistrés."
    )

    parser_lister.add_argument(
        "--statut",
        choices=[
            statut.value
            for statut in StatutTicket
        ],
        help="Filtrer par statut."
    )

    parser_lister.add_argument(
        "--priorite",
        choices=[
            priorite.value
            for priorite in PrioriteTicket
        ],
        help="Filtrer par priorité."
    )

    parser_lister.add_argument(
        "--technicien-id",
        type=int,
        help="Filtrer par identifiant de technicien."
    )

    parser_lister.add_argument(
        "--mot-cle",
        help="Rechercher dans le titre et la description."
    )

    parser_lister.set_defaults(fonction=commande_lister)

    parser_detail = sous_commandes.add_parser(
        "detail",
        help="Afficher le détail d'un ticket."
    )

    parser_detail.add_argument(
        "--ticket-id",
        type=int,
        required=True,
        help="Identifiant du ticket."
    )

    parser_detail.set_defaults(fonction=commande_detail)

    parser_rechercher = sous_commandes.add_parser(
        "rechercher",
        help="Rechercher des tickets avec un mot-clé."
    )

    parser_rechercher.add_argument(
        "mot_cle",
        help="Mot ou expression à rechercher."
    )

    parser_rechercher.set_defaults(
        fonction=commande_rechercher
    )

    parser_assigner = sous_commandes.add_parser(
        "assigner",
        help="Assigner le technicien de démonstration."
    )

    parser_assigner.add_argument(
        "--ticket-id",
        type=int,
        required=True,
        help="Identifiant du ticket."
    )

    parser_assigner.set_defaults(fonction=commande_assigner)

    parser_intervenir = sous_commandes.add_parser(
        "intervenir",
        help="Ajouter une intervention au ticket."
    )

    parser_intervenir.add_argument(
        "--ticket-id",
        type=int,
        required=True,
        help="Identifiant du ticket."
    )

    parser_intervenir.add_argument(
        "--description",
        required=True,
        help="Description de l'intervention."
    )

    parser_intervenir.add_argument(
        "--duree",
        type=int,
        required=True,
        help="Durée de l'intervention en minutes."
    )

    parser_intervenir.set_defaults(
        fonction=commande_intervenir
    )

    parser_resoudre = sous_commandes.add_parser(
        "resoudre",
        help="Marquer un ticket comme résolu."
    )

    parser_resoudre.add_argument(
        "--ticket-id",
        type=int,
        required=True,
        help="Identifiant du ticket."
    )

    parser_resoudre.set_defaults(fonction=commande_resoudre)

    parser_fermer = sous_commandes.add_parser(
        "fermer",
        help="Fermer un ticket résolu."
    )

    parser_fermer.add_argument(
        "--ticket-id",
        type=int,
        required=True,
        help="Identifiant du ticket."
    )

    parser_fermer.set_defaults(fonction=commande_fermer)

    parser_supprimer = sous_commandes.add_parser(
        "supprimer",
        help="Supprimer définitivement un ticket."
    )

    parser_supprimer.add_argument(
        "--ticket-id",
        type=int,
        required=True,
        help="Identifiant du ticket."
    )

    parser_supprimer.set_defaults(
        fonction=commande_supprimer
    )
    parser_statistiques = sous_commandes.add_parser(
        "statistiques",
        help="Afficher les statistiques des tickets."
    )

    parser_statistiques.set_defaults(
        fonction=commande_statistiques
    )
    return parser


def main() -> None:
    parser = creer_parser()
    args = parser.parse_args()

    try:
        args.fonction(args)

    except ErreurMaintenance as erreur:
        print(f"\nErreur métier : {erreur}")

    except ValueError as erreur:
        print(f"\nValeur invalide : {erreur}")


if __name__ == "__main__":
    main()