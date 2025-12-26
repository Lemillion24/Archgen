import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def generate_project(project_name: str, project_type: str, language: str, architecture: str):
    """
    Fonction principale qui orchestre la création du projet.
    """
    # 1. Définir les chemins
    # Le dossier où se trouve ce script (archigen/)
    base_dir = Path(__file__).parent
    
    # Le chemin vers les templates (archigen/templates/python/clean/)
    template_dir = base_dir / "templates" / language / architecture
    
    # Le fichier de structure (archigen/templates/python/clean/structure.yaml)
    structure_file = template_dir / "structure.yaml"

    # 2. Vérification de sécurité
    if not structure_file.exists():
        print(f"❌ Erreur : L'architecture '{architecture}' pour '{language}' n'est pas encore implémentée.")
        return False

    # 3. Chargement de la structure YAML
    with open(structure_file, "r") as f:
        structure = yaml.safe_load(f)

    # 4. Configuration de Jinja2 (le moteur de template)
    jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    # Les variables qu'on va injecter dans les templates
    context = {
        "project_name": project_name,
        "project_type": project_type,
        "language": language,
        "architecture": architecture
    }

    # 5. Création du dossier racine du projet
    root_path = Path.cwd() / project_name
    if root_path.exists():
        print(f"❌ Erreur : Le dossier '{project_name}' existe déjà ici.")
        return False
    
    root_path.mkdir()
    print(f"📁 Création du dossier racine : {project_name}")

    # 6. Lancement de la récursion
    # On regarde la clé "root" du YAML et on lance la création
    _create_recursive(root_path, structure["root"], jinja_env, context)
    
    return True

def _create_recursive(current_path: Path, structure_content, jinja_env, context):
    """
    Fonction qui s'appelle elle-même pour créer l'arbre de fichiers.
    """
    # Si le contenu est un Dictionnaire, c'est un DOSSIER
    if isinstance(structure_content, dict):
        for name, content in structure_content.items():
            new_path = current_path / name
            
            # Si le contenu est null (vide) ou un dico, on crée le dossier
            if content is None or isinstance(content, dict):
                new_path.mkdir(exist_ok=True)
                # 🔄 APPEL RÉCURSIF : On plonge dans le sous-dossier
                if content is not None:
                    _create_recursive(new_path, content, jinja_env, context)
            
            # Si le contenu est une chaîne, c'est un FICHIER template (cas traité en dessous)
            elif isinstance(content, str):
                _render_file(new_path, content, jinja_env, context)

    # Si le contenu est une chaîne directement (cas rare mais possible), c'est un fichier
    elif isinstance(structure_content, str):
        _render_file(current_path, structure_content, jinja_env, context)

def _render_file(file_path: Path, template_name: str, jinja_env, context):
    """
    Génère un fichier à partir d'un template Jinja.
    """
    template = jinja_env.get_template(template_name)
    content = template.render(context)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)