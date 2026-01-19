import typer
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from pyfiglet import Figlet
from archgen.generator import generate_project

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
        project_name = Prompt.ask(
            "Quel est le [bold green]nom de ton projet[/bold green] ?"
        )
    else:
        console.print(f"📂 Nom du projet : [bold green]{project_name}[/bold green]")

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
    
    valid_architectures = COMPATIBILITY.get(project_type, ARCHITECTURES)
    valid_frameworks = FRAMEWORKS.get(language, ["none"])
    
    # 4. Framework
    if framework:
        if framework == "react":
            language = "javascript"
        elif framework not in FRAMEWORKS.get(language, ['none']):
           console.print(f"[yellow]⚠️ Attention: {framework} n'est pas standard pour {language}, mais on continue.[/yellow]")
        console.print(f"⚡ Framework : [bold green]{framework}[/bold green]")
    else:
        framework = Prompt.ask(
            f"Quel [blod green]framework[/blod green] utiliser ?",
            choices=valid_frameworks,
            default="none"
            )
    # 5. Architecture
    architecture = Prompt.ask(
        "Quelle [bold green]architecture[/bold green] souhaites-tu implémenter ?",
        choices=valid_architectures,
        default=valid_architectures[0],
    )

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
    # ... (le début du fichier reste identique)

    if Confirm.ask("Ces informations sont-elles correctes ?"):
        console.print(f"\n[bold green]🚀 C'est parti ! Génération de {project_name} en cours...[/bold green]")

        # 👇 APPEL DU GÉNÉRATEUR 👇
        success = generate_project(project_name, project_type, language, framework, architecture)

        if success:
            console.print(f"\n[bold green]✅ Projet {project_name} créé avec succès ![/bold green]")
            console.print(f"👉 cd {project_name}")
        else:
            console.print("\n[bold red]💥 La génération a échoué.[/bold red]")

    else:
        console.print("\n[red]❌ Annulation.[/red]")


@app.command()
def create_react():
    """
    lance un projet react sans les dependance pour l'instant
    """
    print_logo()
    
    #valid_frameworks = FRAMEWORKS.get(language, ["none"])
    
    project_name = Prompt.ask(
        f"Quel est le [blod green] nom du  projet react [/blod green]?"
    )
    project_type = Prompt.ask(
        "Quel [bold green]type de projet[/bold green] veux-tu créer ?",
        choices=PROJECT_TYPES,
        default="api",  # Valeur par défaut si on appuie sur Entrée
    )
    valid_architectures = COMPATIBILITY.get(project_type, ARCHITECTURES)
    language = "javascript"
    framework = "react"
    architecture = Prompt.ask(
        f"Quelle [bold green]architecture[/bold green] souhaites-tu implémenter ?",
        choices=valid_architectures,
        default=valid_architectures[0],
    )

    console.print("\n[bold yellow]📋 Vérification de la configuration :[/bold yellow]")

    # On crée un joli tableau pour récapituler (ça fait très pro)
    table = Table(show_header=False, box=None)
    table.add_row("Nom du projet", f"[bold white]{project_name}[/bold white]")
    table.add_row("Type", f"[cyan]{project_type}[/cyan]")
    table.add_row("Langage", f"[magenta]{language}[/magenta]")
    table.add_row("Framework", f"[yellow]{framework}[/yellow]")
    table.add_row("Architecture", f"[green]{architecture}[/green]")
    console.print(table)

    console.print("")  
    
    #success = generate_project(project_name,project_type,language, framework, architecture)
    if Confirm.ask("Ces informations sont-elles correctes ?"):
        console.print(f"\n[bold green]🚀 C'est parti ! Génération de {project_name} en cours...[/bold green]")

        # 👇 APPEL DU GÉNÉRATEUR 👇
        success = generate_project(project_name, project_type, language, framework, architecture)

        if success:
            console.print(f"\n[bold green]✅ Projet {project_name} créé avec succès ![/bold green]")
            console.print(f"👉 cd {project_name}")
        else:
            console.print("\n[bold red]💥 La génération a échoué.[/bold red]")

    else:
        console.print("\n[red]❌ Annulation.[/red]")


"""@app.Option()
def op():
    print_logo()
    """

if __name__ == "__main__":
    app()
