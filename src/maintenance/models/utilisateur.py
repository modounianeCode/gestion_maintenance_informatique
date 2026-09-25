class Utilisateur:
    ROLES_VALIDES = {"demandeur", "technicien", "administrateur"}

    def __init__(
        self,
        identifiant: int,
        nom: str,
        email: str,
        role: str = "demandeur"
    ):
        self.identifiant = identifiant
        self.nom = nom.strip()
        self.email = email
        self.role = role

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valeur: str) -> None:
        valeur_normalisee = valeur.lower().strip()

        if not valeur_normalisee or "@" not in valeur_normalisee:
            raise ValueError("L'adresse e-mail est invalide.")

        self._email = valeur_normalisee

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, valeur: str) -> None:
        valeur_normalisee = valeur.lower().strip()

        if valeur_normalisee not in self.ROLES_VALIDES:
            roles = ", ".join(sorted(self.ROLES_VALIDES))
            raise ValueError(
                f"Rôle invalide. Rôles autorisés : {roles}."
            )

        self._role = valeur_normalisee

    def permissions(self) -> list[str]:
        return [
            "creer_ticket",
            "voir_ses_tickets"
        ]

    def se_presenter(self) -> str:
        return (
            f"Utilisateur #{self.identifiant} : "
            f"{self.nom} — rôle : {self.role}."
        )

    def est_technicien(self) -> bool:
        return False

    def est_administrateur(self) -> bool:
        return False


class Demandeur(Utilisateur):
    def __init__(
        self,
        identifiant: int,
        nom: str,
        email: str
    ):
        super().__init__(
            identifiant=identifiant,
            nom=nom,
            email=email,
            role="demandeur"
        )


class Technicien(Utilisateur):
    def __init__(
        self,
        identifiant: int,
        nom: str,
        email: str,
        specialite: str
    ):
        super().__init__(
            identifiant=identifiant,
            nom=nom,
            email=email,
            role="technicien"
        )
        self.specialite = specialite.strip().lower()

    def permissions(self) -> list[str]:
        return super().permissions() + [
            "voir_tickets_assignes",
            "prendre_en_charge_ticket",
            "ajouter_intervention",
            "mettre_a_jour_ticket"
        ]

    def est_technicien(self) -> bool:
        return True


class Administrateur(Utilisateur):
    def __init__(
        self,
        identifiant: int,
        nom: str,
        email: str
    ):
        super().__init__(
            identifiant=identifiant,
            nom=nom,
            email=email,
            role="administrateur"
        )

    def permissions(self) -> list[str]:
        return super().permissions() + [
            "voir_tous_les_tickets",
            "gerer_utilisateurs",
            "gerer_equipements",
            "gerer_statistiques"
        ]

    def est_administrateur(self) -> bool:
        return True