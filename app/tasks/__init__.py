"""Tasks module."""
from .tasks import (send_scanr_to_preprod,
                    send_scanr_to_prod,
                    etl_scanr,
                    etl_authors,
                    etl_organizations)

__all__ = ["send_scanr_to_preprod",
           "send_scanr_to_prod",
           "etl_scanr",
           "etl_authors",
           "etl_organizations"]

ALL_TASKS = {
    "send_scanr_to_preprod": send_scanr_to_preprod,
    "send_scanr_to_prod": send_scanr_to_prod,
    "etl_scanr": etl_scanr,
    "etl_authors": etl_authors,
    "etl_organizations": etl_organizations,
}

TASKS_INFO = {
    "send_scanr_to_preprod": {
        "description": ("Cette tâche récupère les données de la collection " +
                        "scanr, les formatte et écrit un csv sur le serveur " +
                        "FTP destiné à la préprod de scanR."),
        "name": "Export scanR -> Préprod",
        "execution_name": "send_scanr_to_preprod"
    },
    "send_scanr_to_prod": {
        "description": ("Cette tâche récupère les données de la collection" +
                        "scanr, les formatte et écrit un csv sur le serveur" +
                        "FTP destiné à la prod de scanR."),
        "name": "Export scanR -> Prod",
        "execution_name": "send_scanr_to_prod"
    },
    "etl_scanr": {
        "description": ("Actualise la collection Scanr à partir de " +
                        "la collection Publications."),
        "name": "Actualiser scanR",
        "execution_name": "etl_scanr"
    },
    "etl_authors": {
        "description": ("Creer ou rafraîchi la collection authors " +
                        "qui contient un document par auteur identifié dans " +
                        "une publication et le nombre de publications qui " +
                        "lui sont associées"),
        "name": "Aggréger auteurs",
        "execution_name": "etl_authors"
    },
    "etl_organizations": {
        "description": ("Creer ou rafraîchi la collection organizations " +
                        "qui contient un document par publi dans " +
                        "avec la liste des affiliations"),
        "name": "Export organizations",
        "execution_name": "etl_organizations"
    }
}
