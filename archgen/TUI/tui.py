from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Input, Select, Button, Label
import sys

# On simule tes listes (tu pourras importer les vraies depuis ton main.py plus tard)
LANGUAGES = [("JavaScript", "javascript"), ("Python", "python"), ("PHP", "php"), ("Go", "go")]
FRAMEWORKS = [("Aucun (Vanilla)", "none"), ("React", "react"), ("MERN", "mern"), ("Laravel", "laravel"), ("Django", "django")]
ARCHITECTURES = [("Clean Architecture", "clean"), ("MVC", "mvc"), ("Fullstack", "fullstack")]
PROJECT_TYPES = [("Web / Frontend", "web"), ("API / Backend", "api"), ("CLI", "cli")]

class ArchigenTUI(App):
    # --- LE STYLE (CSS) ---
    CSS = """
    Screen {
        align: center middle;
        background: #1e1e2e; /* Fond sombre */
    }

    #form-container {
        width: 60;
        height: auto;
        border: solid #cba6f7; /* Bordure violette comme sur ta capture */
        padding: 1 2;
        background: #181825;
    }

    Label {
        margin-top: 1;
        color: #bac2de;
        text-style: bold;
    }

    Input, Select {
        margin-bottom: 1;
        width: 100%;
    }

    #btn-generate {
        margin-top: 2;
        width: 100%;
        background: #a6e3a1; /* Vert pastel */
        color: #11111b;
        text-style: bold;
    }
    """

    # --- RACCOURCIS CLAVIER ---
    BINDINGS = [
        ("q", "quit", "Quitter"),
        ("ctrl+g", "generate", "Générer")
    ]

    # --- CONSTRUCTION DE L'INTERFACE ---
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Vertical(id="form-container"):
            # Titre
            yield Label("CREATE PROJECT", id="title")
            
            # Formulaire
            yield Label("Project Name")
            yield Input(placeholder="> ex: mon_projet", id="input-name")

            yield Label("Project Type")
            yield Select(PROJECT_TYPES, id="select-type", value="api")

            yield Label("Language")
            yield Select(LANGUAGES, id="select-lang", value="javascript")

            yield Label("Framework")
            yield Select(FRAMEWORKS, id="select-framework", value="none")

            yield Label("Architecture")
            yield Select(ARCHITECTURES, id="select-archi", value="clean")

            # Bouton de validation
            yield Button("🚀 GÉNÉRER LE PROJET", id="btn-generate")
            
        yield Footer()

    # --- GESTION DES ACTIONS ---
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-generate":
            self.action_generate()

    def action_generate(self) -> None:
        """Récupère les valeurs et lance la génération"""
        # 1. On récupère les valeurs des champs
        name = self.query_one("#input-name", Input).value
        p_type = self.query_one("#select-type", Select).value
        lang = self.query_one("#select-lang", Select).value
        frame = self.query_one("#select-framework", Select).value
        archi = self.query_one("#select-archi", Select).value

        # 2. Vérification basique
        if not name:
            self.notify("⚠️ Le nom du projet est obligatoire !", severity="error")
            return

        # 3. Notification de succès (Pour l'instant, on affiche juste)
        self.notify(f"✅ Préparation de {name} ({lang}/{frame}/{archi})", severity="information")
        
        # TODO: Plus tard, on appellera ta fonction generate_project() ici !
        # generate_project(name, p_type, lang, frame, archi)