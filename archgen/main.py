import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from archgen.generator import generate_project

# Initialisation
app = typer.Typer()
console = Console()

# --- 1. CONFIGURATION (Les choix possibles) ---
# On utilise des clés simples (en minuscule, sans espace) pour le code
PROJECT_TYPES = ["web", "api", "cli", "mobile", "game", "platform"]
LANGUAGES = ["python", "go", "javascript", "typescript", "java", "csharp"]
# Liste des 10 architectures (exemple, tu pourras ajuster)
ARCHITECTURES = [
    "mvc",
    "clean",
    "hexagonal",
    "microservices",
    "event_driven",
    "monolith",
    "n_tiers",
    "mvvm",
    "soa",
    "serverless",
]


@app.callback()
def main():
    """
    Bienvenue
    """
    pass


@app.command()
def create():
    """
    Lance l'assistant pour configurer un nouveau projet.
    """
    console.print(
        "[bold blue]🛠  Bienvenue dans Archigen[/bold blue] - Créateur d'Architectures\n"
    )

    # --- 2. QUESTIONNAIRE INTERACTIF ---

    # 1. Nom du projet
    # Prompt.ask pose une question et attend une réponse
    project_name = Prompt.ask(
        "Quel est le [bold green]nom de ton projet[/bold green] ?"
    )

    # 2. Type de projet
    # L'argument 'choices' force l'utilisateur à choisir dans la liste.
    # S'il tape autre chose, Rich redemande automatiquement !
    project_type = Prompt.ask(
        "Quel [bold green]type de projet[/bold green] veux-tu créer ?",
        choices=PROJECT_TYPES,
        default="api",  # Valeur par défaut si on appuie sur Entrée
    )

    # 3. Langage
    language = Prompt.ask(
        f"Quel [bold green]langage[/bold green] utiliser pour ce projet {project_type} ?",
        choices=LANGUAGES,
        default="python",
    )

    # 4. Architecture
    architecture = Prompt.ask(
        "Quelle [bold green]architecture[/bold green] souhaites-tu implémenter ?",
        choices=ARCHITECTURES,
        default="clean",
    )

    # --- 3. RÉSUMÉ ET CONFIRMATION ---
    console.print("\n[bold yellow]📋 Vérification de la configuration :[/bold yellow]")

    # On crée un joli tableau pour récapituler (ça fait très pro)
    table = Table(show_header=False, box=None)
    table.add_row("Nom du projet", f"[bold white]{project_name}[/bold white]")
    table.add_row("Type", f"[cyan]{project_type}[/cyan]")
    table.add_row("Langage", f"[magenta]{language}[/magenta]")
    table.add_row("Architecture", f"[green]{architecture}[/green]")
    console.print(table)

    console.print("")  # Saut de ligne

    # Confirm.ask renvoie True (Oui) ou False (Non)
    # ... (le début du fichier reste identique)

    if Confirm.ask("Ces informations sont-elles correctes ?"):
        console.print(f"\n[bold green]🚀 C'est parti ! Génération de {project_name} en cours...[/bold green]")

        # 👇 APPEL DU GÉNÉRATEUR 👇
        success = generate_project(project_name, project_type, language, architecture)

        if success:
            console.print(f"\n[bold green]✅ Projet {project_name} créé avec succès ![/bold green]")
            console.print(f"👉 cd {project_name}")
        else:
            console.print("\n[bold red]💥 La génération a échoué.[/bold red]")

    else:
        console.print("\n[red]❌ Annulation.[/red]")

if __name__ == "__main__":
    app()
