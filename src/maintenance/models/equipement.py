class Equipement:
    STATUTS_VALIDES = {
        "disponible",
        "en_panne",
        "en_maintenance",
        "retire"
    }

    def __init__(
        self,
        identifiant: int,
        nom: str,
        categorie: str,
        numero_serie: str,
        statut: str = "disponible"
    ):
        self.identifiant = identifiant
        self.nom = nom.strip()
        self.categorie = categorie.strip().lower()
        self.numero_serie = numero_serie.strip().upper()
        self.statut = statut

    @property
    def statut(self) -> str:
        return self._statut

    @statut.setter
    def statut(self, valeur: str) -> None:
        valeur_normalisee = valeur.lower().strip()

        if valeur_normalisee not in self.STATUTS_VALIDES:
            statuts = ", ".join(sorted(self.STATUTS_VALIDES))
            raise ValueError(
                f"Statut invalide. Statuts autorisés : {statuts}."
            )

        self._statut = valeur_normalisee

    def afficher_resume(self) -> str:
        return (
            f"Équipement #{self.identifiant} : {self.nom} "
            f"({self.categorie}) — statut : {self.statut}."
        )

    def est_utilisable(self) -> bool:
        return self.statut == "disponible"

    def declarer_en_panne(self) -> None:
        if self.statut == "retire":
            raise ValueError(
                "Un équipement retiré ne peut pas être déclaré en panne."
            )

        self.statut = "en_panne"

    def retirer(self) -> None:
        self.statut = "retire"