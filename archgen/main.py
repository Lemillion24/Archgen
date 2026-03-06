from pathlib import Path
import questionary
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from pyfiglet import Figlet
from archgen.generator import generate_project
from archgen.secure import encrypt_directory
from archgen.TUI.tui import ArchigenTUI 

# Initialisation
app = typer.Typer()
console = Console()

# --- 1. CONFIGURATION (Les choix possibles) ---
#  utilise des clés simples  pour le code
PROJECT_TYPES = ["web", "api", "cli", "mobile", "game", "platform"]
# ...
LANGUAGES = ["python", "javascript", "php", "java", "csharp", "go"]

# Associe chaque langage à ses frameworks populaires
# "none" signifie "Vanilla" ou "Pur" (sans framework)
FRAMEWORKS = {
    "python": ["django", "flask", "fastapi", "none"],
    "javascript": ["react", "vue", "angular", "express", "none"],
    "typescript": ["react", "angular", "nest", "none"],
    "php": ["laravel", "symfony", "none"],
    "java": ["spring", "jakarta", "none"],
    "csharp": ["dotnet-core", "none"],
    "go": ["gin", "fiber", "none"]
}

# ... (ARCHITECTURES reste pareil)# Liste des 10 architectures (exemple, tu pourras ajuster)
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
    "mern",
    "pern",
]
# Matrice de compatibilité : Quelles architectures pour quel type de projet ?
COMPATIBILITY = {
    "web": ["mvc", "clean", "n_tiers", "mern", "pern"],
    "api": ["clean", "hexagonal", "microservices"],
    "cli": ["monolith", "clean"],
    "mobile": ["mvvm", "clean"],
    "game": ["event_driven", "monolith"],
    "platform": ["microservices", "soa"]
}


# Dans main.py, avant d'appeler generate_project

def validate_selection(language, framework):
    allowed = FRAMEWORKS.get(language, ["none"])
    if framework not in allowed:
        console.print(f"[bold red]Erreur:[/bold red] Le framework '{framework}' n'est pas disponible pour le langage '{language}'.")
        raise typer.Exit()


def print_logo():
    """affichier
        le logo en un truc sympa
    """
    # genere  le texte ASCII
    f =  Figlet(font='slant')
    ascii_art =f.renderText('Archgen')
    console.print(ascii_art, style='bold magenta')

@app.callback()
def main():
    """
    Bienvenue
    """
    pass


@app.command()
def create(
    # 1. ARGUMENT : Le nom du projet (positionnel, optionnel)
    project_name: str = typer.Argument(None, help="Le nom du dossier à créer"),
    # 2. OPTION : Le framework (ex: --framework react ou -f react)
    framework: str = typer.Option(None, "--framework", "-f", help="Framework (react, django, laravel...)"),
    # 3.OPTION : verouillage (ex: --secure ou -s)
    secure: bool = typer.Option(False, "--secure", "-s", help="Chiffrer le projet après génération avec un mot de passe")
):
    """
    Lance l'assistant pour configurer un nouveau projet.
    """
    print_logo()
    
    console.print(
        "[bold blue]🛠  Bienvenue dans Archigen 🛠 [/bold blue] - Créateur d'Architectures\n"
    )

    # --- 2. QUESTIONNAIRE INTERACTIF ---

    # 1. Nom du projet
    # Prompt.ask pose une question et attend une réponse
    if not project_name:
        project_name = questionary.text(
            "Quel est le nom de ton projet ?",
            validate=lambda text:True if len(text)>0 else "Entre un nom Valide"
        ).ask()

        if project_name is None:
            console.print("[red]Annulation[/red]")
            raise typer.Exit()
    else:
        console.print(f"📂 Nom du projet : [bold green]{project_name}[/bold green]")

    # 2. Type de projet
    # L'argument 'choices' force l'utilisateur à choisir dans la liste.
    # faire une selection
    project_type = questionary.select(
        "Quel [bold green]type de projet[/bold green] veux-tu créer ?",
        choices=PROJECT_TYPES,
        default="api",  # Valeur par défaut si on appuie sur Entrée
    ).ask()
    if not project_type: raise typer.Exit()

    # 3. Langage
    language = questionary.select(
        f"Quel [bold green]langage[/bold green] utiliser pour ce projet {project_type} ?",
        choices=LANGUAGES,
        default="python",
    ).ask()
    if not language: raise typer.Exit()
    
    #valid_architectures = COMPATIBILITY.get(project_type, ARCHITECTURES)
    valid_frameworks = FRAMEWORKS.get(language, ["none"])
    # Utilisation dans la commande create :
    
    # 4. Framework
    if framework:
        if framework not in FRAMEWORKS.get(language, ["none"]):
             console.print(f"[yellow]⚠️ Attention: {framework} n'est pas standard pour {language}.[/yellow]")
        console.print(f"⚡ Framework : [bold green]{framework}[/bold green]")
    else:
        available_frameworks = FRAMEWORKS.get(language, ["none"])
        framework = questionary.select(
            "Quel framework veux-tu utiliser ?",
            choices=available_frameworks,
            default="none"
        ).ask()
        if not framework: raise typer.Exit()


    # 5. Architecture
    valid_architectures = COMPATIBILITY.get(project_type, ARCHITECTURES)
    architecture = questionary.select(
        "Quelle architecture appliquer ?",
        choices=valid_architectures,
        default="clean"
    ).ask()
    if not architecture: raise typer.Exit()

    install_deps = questionary.confirm(
        "Veux-tu installer les dépendances automatiquement ?",
        default=True
    ).ask()
    if install_deps is None: raise typer.Exit()

    init_git_repo = questionary.confirm(
        "Veux-tu initialiser un dépôt Git ?",
        default=True
    ).ask()
    if init_git_repo is None: raise typer.Exit()

    validate_selection(language, framework)
    # --- 3. RÉSUMÉ ET CONFIRMATION ---
    console.print("\n[bold yellow]📋 Vérification de la configuration :[/bold yellow]")

    # On crée un joli tableau pour récapituler (ça fait très pro)
    table = Table(show_header=False, box=None)
    table.add_row("Nom du projet", f"[bold white]{project_name}[/bold white]")
    table.add_row("Type", f"[cyan]{project_type}[/cyan]")
    table.add_row("Langage", f"[magenta]{language}[/magenta]")
    table.add_row("Framework", f"[yellow]{framework}[/yellow]")
    table.add_row("Architecture", f"[green]{architecture}[/green]")
    console.print(table)

    console.print("")  # Saut de ligne

    # Confirm.ask renvoie True (Oui) ou False (Non)
    if Confirm.ask("Ces informations sont-elles correctes ?"):
        console.print(f"\n[bold green]🚀 C'est parti ! Génération de {project_name} en cours...[/bold green]")

        # 👇 APPEL DU GÉNÉRATEUR 👇
        success = generate_project(project_name, project_type, language, framework, architecture)

        if success:
            root_path = Path.cwd() / project_name

            # secure option
            if secure:
                password = Prompt.ask( "entre un mot de passe pour chiffre le projet(ne pas le perdre ou le divulguer!)", password=True,)
                if not password:
                    console.print("[red] Mots depasse requit pour --secure[/red].")
                    return
                console.print("[yellow] [-]chiffrement en cours ...[/yellow]"
                )

                try:
                    encrypt_directory(root_path, password)
                    console.print(f"\n[blod green] Project {project_name} cree et securiser avec succes! [/bold green]")
                    console.print(f"cd {project_name} puis arcgen unlock {project_name} pour le dechiffrer")
                except Exception:
                    console.print(f"[red] Echec de chiffremment project: {project_name} genere mais pas chiffrer")
            else:
                console.print(f"\n[bold green]✅ Projet {project_name} créé avec succès ![/bold green]")
                console.print(f"👉 cd {project_name}")
        else:
            console.print("\n[bold red]💥 La génération a échoué.[/bold red]")

    else:
        console.print("\n[red]❌ Annulation.[/red]")


@app.command()
def create_react():
    """
    Raccourci pour créer rapidement un projet React.
    Utilise la fonction 'create' avec framework=react pré-sélectionné.
    """
    create(project_name=None, framework="react")


@app.command()
def unlock(
    project_path: str = typer.Argument(..., help="Chemin vers le dossier à déverrouiller"),
):
    """
    Déverrouille (déchiffre) un projet précédemment chiffré avec --secure.
    """
    from archgen.secure import decrypt_directory

    path = Path(project_path).resolve()
    if not path.exists():
        console.print(f"[red]❌ Le chemin '{path}' n'existe pas.[/red]")
        raise typer.Exit(1)

    password = Prompt.ask("Mot de passe du projet", password=True)
    if not password:
        console.print("[red]❌ Mot de passe requis.[/red]")
        raise typer.Exit(1)

    console.print("[yellow]🔓 Déchiffrement du dossier en cours...[/yellow]")
    try:
        decrypt_directory(path, password)
        console.print(f"\n[bold green]✅ Dossier {path} déchiffré avec succès ![/bold green]")
    except Exception as e:
        console.print(f"[red]❌ Échec du déchiffrement : {e}[/red]")
        raise typer.Exit(1)
    
@app.command()
def ui():
    """
    Lance l'interface graphique (TUI) d'Archigen.
    """
    app_tui = ArchigenTUI()
    app_tui.run()


if __name__ == "__main__":
    app()
# N'oublie pas d'importer ton nouveau fichier !
 # Ajuste l'import selon l'emplacement exact de ton fichier

