import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import sys

def generate_project(project_name: str, project_type: str, language: str, framework: str, architecture: str):
    """
    Fonction principale qui orchestre la création du projet.
    
    Args:
        project_name: Nom du projet
        project_type: Type de projet (web, api, cli, etc.)
        language: Langage de programmation
        framework: Framework à utiliser
        architecture: Architecture du projet
        
    Returns:
        bool: True si succès, False sinon
    """
    try:
        # 1. Définir les chemins
        base_dir = Path(__file__).parent

        # Si le template est "none", utiliser "vanilla"
        framework_dir = "vanilla" if framework == "none" else framework
        
        # Chemin vers les templates
        template_dir = base_dir / "templates" / language / framework_dir / architecture
        
        # Fichier de structure
        structure_file = template_dir / "structure.yaml"

        # 2. Vérification de sécurité
        if not structure_file.exists():
            print(f"❌ Erreur : Le template '{language}/{framework_dir}/{architecture}' n'existe pas.")
            print(f"📁 Chemin recherché : {structure_file}")
            return False

        # 3. Chargement de la structure YAML
        try:
            with open(structure_file, "r", encoding="utf-8") as f:
                structure = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ Erreur YAML dans {structure_file}: {e}")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la lecture de {structure_file}: {e}")
            return False

        if not structure or "root" not in structure:
            print(f"❌ Erreur : Le fichier {structure_file} n'a pas de clé 'root'.")
            return False

        # 4. Configuration de Jinja2
        try:
            jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        except Exception as e:
            print(f"❌ Erreur lors de la configuration de Jinja2: {e}")
            return False
        
        # Variables de contexte pour les templates
        context = {
            "project_name": project_name,
            "project_type": project_type,
            "language": language,
            "framework": framework,
            "architecture": architecture,
            "author": "Your Name"  # À améliorer later
        }

        # 5. Création du dossier racine du projet
        root_path = Path.cwd() / project_name
        if root_path.exists():
            print(f"❌ Erreur : Le dossier '{project_name}' existe déjà ici.")
            return False
        
        try:
            root_path.mkdir()
            print(f"📁 Création du dossier racine : {project_name}")
        except Exception as e:
            print(f"❌ Erreur lors de la création du dossier: {e}")
            return False

        # 6. Lancement de la récursion
        try:
            _create_recursive(root_path, structure["root"], jinja_env, context, template_dir)
        except Exception as e:
            print(f"❌ Erreur lors de la génération des fichiers: {e}")
            # Nettoyer le dossier créé en cas d'erreur
            import shutil
            try:
                shutil.rmtree(root_path)
                print(f"🧹 Dossier {project_name} supprimé en raison de l'erreur.")
            except:
                pass
            return False

        return True

    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False


def _create_recursive(current_path: Path, structure_content, jinja_env, context, template_dir):
    """
    Fonction récursive qui crée l'arbre de fichiers et dossiers.
    
    Args:
        current_path: Chemin courant
        structure_content: Contenu de la structure (dict ou string)
        jinja_env: Environnement Jinja2
        context: Contexte de rendu
        template_dir: Répertoire des templates
    """
    # Si c'est un dictionnaire, on traite chaque clé-valeur
    if isinstance(structure_content, dict):
        for name, content in structure_content.items():
            new_path = current_path / name
            
            # Si contenu est None ou dict, c'est un dossier
            if content is None or isinstance(content, dict):
                try:
                    new_path.mkdir(exist_ok=True)
                    print(f"📁 Créé dossier: {new_path.relative_to(Path.cwd())}")
                except Exception as e:
                    print(f"❌ Erreur lors de la création du dossier {new_path}: {e}")
                    raise
                
                # Récursion dans le sous-dossier
                if content is not None:
                    _create_recursive(new_path, content, jinja_env, context, template_dir)
            
            # Si contenu est une chaîne, c'est un fichier template
            elif isinstance(content, str):
                try:
                    _render_file(new_path, content, jinja_env, context, template_dir)
                except Exception as e:
                    print(f"❌ Erreur lors du rendu du fichier {new_path}: {e}")
                    raise

    # Si c'est une chaîne directement (cas rare)
    elif isinstance(structure_content, str):
        try:
            _render_file(current_path, structure_content, jinja_env, context, template_dir)
        except Exception as e:
            print(f"❌ Erreur lors du rendu: {e}")
            raise


def _render_file(file_path: Path, template_name: str, jinja_env, context, template_dir):
    """
    Génère un fichier à partir d'un template Jinja2.
    
    Args:
        file_path: Chemin du fichier à créer
        template_name: Nom du template (relatif à template_dir)
        jinja_env: Environnement Jinja2
        context: Contexte de rendu
        template_dir: Répertoire des templates
    """
    try:
        # Charger et rendre le template
        template = jinja_env.get_template(template_name)
        content = template.render(context)
        
        # Créer le fichier
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"📄 Créé fichier: {file_path.relative_to(Path.cwd())}")
        
    except TemplateNotFound:
        print(f"❌ Erreur : Template '{template_name}' introuvable dans {template_dir}")
        raise
    except Exception as e:
        print(f"❌ Erreur lors du rendu de {template_name}: {e}")
        raise