from src.maintenance.models.utilisateur import (
    Administrateur,
    Demandeur,
    Technicien
)


demandeur = Demandeur(
    identifiant=1,
    nom="Awa Diop",
    email="awa@example.com"
)

technicien = Technicien(
    identifiant=2,
    nom="Modou Niane",
    email="modou@example.com",
    specialite="Maintenance informatique"
)

administrateur = Administrateur(
    identifiant=3,
    nom="Fatou Ndiaye",
    email="fatou@example.com"
)

utilisateurs = [demandeur, technicien, administrateur]

for utilisateur in utilisateurs:
    print(utilisateur.se_presenter())
    print(f"Permissions : {utilisateur.permissions()}")
    print(f"Technicien ? {utilisateur.est_technicien()}")
    print(f"Administrateur ? {utilisateur.est_administrateur()}")
    print("-" * 50)
from src.maintenance.models.equipement import Equipement
from src.maintenance.models.enums import PrioriteTicket
from src.maintenance.models.ticket import Ticket


ordinateur = Equipement(
    identifiant=10,
    nom="Dell Latitude 5420",
    categorie="ordinateur",
    numero_serie="DL-2026-001"
)

ticket = Ticket(
    identifiant=1,
    titre="Ordinateur qui ne démarre pas",
    description="Le voyant s'allume mais l'écran reste noir.",
    createur=demandeur,
    equipement=ordinateur,
    priorite=PrioriteTicket.HAUTE
)

print(ticket.afficher_resume())

ticket.assigner_technicien(technicien)
print(ticket.afficher_resume())

ticket.resoudre()
print(ticket.afficher_resume())

ticket.fermer()
print(ticket.afficher_resume())
from src.maintenance.models.intervention import Intervention


intervention = Intervention(
    identifiant=1,
    description="Remplacement du câble d'alimentation.",
    duree_minutes=30,
    technicien=technicien
)

print(intervention.afficher_resume())
print(f"Intervention longue ? {intervention.est_longue()}")