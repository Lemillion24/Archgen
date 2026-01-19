#!/usr/bin/env python3
"""
Tests unitaires pour vérifier les corrections apportées.
"""

import sys
from pathlib import Path
from unittest.mock import patch

# Ajouter le répertoire au path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Vérifier que les imports fonctionnent."""
    try:
        from archgen.main import create, create_react, FRAMEWORKS, ARCHITECTURES
        from archgen.generator import generate_project
        print("✅ Imports OK")
        return True
    except Exception as e:
        print(f"❌ Erreur imports: {e}")
        return False

def test_no_syntax_errors():
    """Vérifier qu'il n'y a pas d'erreurs de syntaxe."""
    import py_compile
    files = [
        "archgen/main.py",
        "archgen/generator.py"
    ]
    
    for file in files:
        try:
            py_compile.compile(file, doraise=True)
            print(f"✅ {file} - Pas d'erreur de syntaxe")
        except py_compile.PyCompileError as e:
            print(f"❌ {file} - Erreur: {e}")
            return False
    return True

def test_framework_logic():
    """Tester la logique du framework."""
    from archgen.main import FRAMEWORKS
    
    # Vérifier que react est dans javascript
    if "react" in FRAMEWORKS.get("javascript", []):
        print("✅ React est correctement dans JavaScript")
    else:
        print("❌ React manque dans JavaScript")
        return False
    
    # Vérifier que django est dans python
    if "django" in FRAMEWORKS.get("python", []):
        print("✅ Django est correctement dans Python")
    else:
        print("❌ Django manque dans Python")
        return False
    
    return True

def test_architecture_compatibility():
    """Tester la matrice de compatibilité."""
    from archgen.main import COMPATIBILITY
    
    # Vérifier que mern est pour web
    if "mern" in COMPATIBILITY.get("web", []):
        print("✅ MERN est compatible avec 'web'")
    else:
        print("❌ MERN manque pour 'web'")
        return False
    
    # Vérifier que mvc est disponible
    if "mvc" in [arch for archs in COMPATIBILITY.values() for arch in archs]:
        print("✅ MVC est disponible")
    else:
        print("❌ MVC manque")
        return False
    
    return True

def main():
    """Exécuter tous les tests."""
    print("=" * 50)
    print("🧪 TESTS DE VÉRIFICATION")
    print("=" * 50)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Syntaxe", test_no_syntax_errors),
        ("Framework Logic", test_framework_logic),
        ("Architecture Compatibility", test_architecture_compatibility),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📝 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Score: {passed}/{total} ({100*passed//total}%)")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS PASSENT!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
