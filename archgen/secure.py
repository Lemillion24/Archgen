from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64  
import os

def derive_key(password: str, salt: bytes) -> bytes:
    """Dérive une clé à partir d'un mot de passe et d'un sel."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_directory(root_dir: Path, password: str):
    """Chiffre recursivement tous les fichiers d'un répertoire."""
    key = derive_key(password, b"archgen_salt_2026")
    f = Fernet(key)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = Path(dirpath) / filename
            try:
                with open(file_path, "rb") as f_in:
                    data = f_in.read()
                encrypted_data = f.encrypt(data)
                with open(file_path, "wb") as f_out:
                    f_out.write(encrypted_data)
                print(f"🔒 Chiffré: {file_path.relative_to(Path.cwd())}")
            except Exception as e:
                print(f"❌ Erreur lors du chiffrement de {file_path}: {e}")
                raise
            