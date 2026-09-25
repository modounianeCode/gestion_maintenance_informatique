# Gestion de maintenance informatique

Application Python en ligne de commande permettant de gérer des tickets
de maintenance pour des équipements informatiques.

Le projet a été réalisé dans le cadre de l'apprentissage de la
programmation orientée objet en Python.

## Fonctionnalités

- Création de tickets de maintenance
- Affichage de la liste des tickets
- Recherche par mot-clé
- Filtrage par statut, priorité et technicien
- Assignation d'un technicien
- Ajout d'interventions techniques
- Résolution et fermeture des tickets
- Suppression de tickets
- Statistiques sur les tickets et interventions
- Sauvegarde persistante des données dans un fichier JSON
- Tests unitaires automatisés

## Concepts Python utilisés

- Classes et objets
- Encapsulation avec `@property`
- Héritage et polymorphisme
- Composition
- `dataclass`
- Énumérations avec `Enum`
- Exceptions personnalisées
- Annotations de type
- Architecture en couches
- Tests unitaires avec `unittest`
- Sérialisation JSON
- Interface en ligne de commande avec `argparse`

## Architecture du projet

```text
poo2_python/
├── data/
│   └── tickets.json
├── src/
│   └── maintenance/
│       ├── models/
│       │   ├── utilisateur.py
│       │   ├── equipement.py
│       │   ├── intervention.py
│       │   ├── ticket.py
│       │   └── enums.py
│       ├── repositories/
│       │   ├── ticket_repository.py
│       │   └── json_ticket_repository.py
│       ├── services/
│       │   └── ticket_service.py
│       └── exceptions.py
├── tests/
├── main.py
└── README.md
```

## Installation

### Prérequis

- Python 3.10 ou version supérieure
- Git, recommandé pour le versionnage

### Créer et activer l'environnement virtuel

Sous Linux ou macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows :

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Aucune dépendance externe n'est nécessaire pour cette version du projet.

## Lancer l'application

Afficher l'aide :

```bash
python main.py --help
```

Créer un ticket :

```bash
python main.py creer \
  --id 100 \
  --titre "Clavier défectueux" \
  --description "Certaines touches ne répondent plus." \
  --priorite haute
```

Lister les tickets :

```bash
python main.py lister
```

Filtrer les tickets ouverts :

```bash
python main.py lister --statut ouvert
```

Afficher le détail d'un ticket :

```bash
python main.py detail --ticket-id 100
```

Assigner un technicien :

```bash
python main.py assigner --ticket-id 100
```

Ajouter une intervention :

```bash
python main.py intervenir \
  --ticket-id 100 \
  --description "Nettoyage et remplacement du clavier." \
  --duree 45
```

Résoudre un ticket :

```bash
python main.py resoudre --ticket-id 100
```

Fermer un ticket :

```bash
python main.py fermer --ticket-id 100
```

Afficher les statistiques :

```bash
python main.py statistiques
```

Supprimer un ticket :

```bash
python main.py supprimer --ticket-id 100
```

## Exécuter les tests

Depuis la racine du projet :

```bash
python -m unittest discover -s tests -v
```

Le projet contient actuellement 37 tests automatisés couvrant les modèles,
les règles métier, le repository, les services et les statistiques.

## Cycle de vie d'un ticket

```text
ouvert
  ↓ assignation d'un technicien
en_cours
  ↓ ajout d'au moins une intervention
resolu
  ↓ fermeture
ferme
```

Un ticket ne peut pas être résolu sans technicien assigné ni intervention.
Un ticket fermé ne peut plus recevoir d'intervention.

## Améliorations futures

- Gestion de plusieurs techniciens et demandeurs
- Gestion de plusieurs équipements
- Authentification des utilisateurs
- Base de données SQLite ou PostgreSQL
- Interface web avec Flask, FastAPI ou Django
- API REST
- Tableau de bord graphique
- Notifications par e-mail
- Gestion des pièces jointes, photos et rapports d'intervention

## Auteur

**Modou Niane**

Étudiant en Licence d'Informatique — Option Génie logiciel  
Université de Thiès