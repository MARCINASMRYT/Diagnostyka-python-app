import os
import json
import subprocess
import sys
import traceback
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# === ŚCIEŻKI ===
PREMIUM_KEY_FILE = "premium.key"
PREMIUM_SIG_FILE = "premium.sig"
CONFIG_FILE = "config.json"
WYNIK_FILE = "diagnostyka_wynik.txt"

# === PUBLICZNY KLUCZ RSA (zaszyty w kodzie) ===
PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxNXyso5XPAhkKSBk4ny5
etp2/RowJ9KTFRbTefMcYgG4ikvz8EE1MGQhqjVjFAS7NaS2WWJYW5aJeVtQyKR3
1HCJDif5YpvN0XToR9MQKD8oZBfnwGpYhNQnAscjxpeC/anYx8/G0Y0XZ9iVZS9A
B6sv5H0ACKphCTbwrWEIRXNrkNCBPCISPQEQGMY6MIKeEhPJhwtEiG6DUaDV2yW+
u5tOCBb+mKr5fCxcodnvQkiZ5DPvBZT39nsdxr4F8sqAXlVGaYoAWbkirtdD5PzR
yj/kj1Tu1xS3wrq3945nwi42Q5OimntOLEenkpfhjV1DmJxK9PSsqwhBsP+uhkPD
xQIDAQAB
-----END PUBLIC KEY-----
"""

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()

def run_cmd(cmd, timeout=None):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate(timeout=timeout)
        return out.decode("utf-8", errors="replace") + err.decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        proc.kill()
        return f"[BŁĄD]: Polecenie '{cmd}' przekroczyło limit czasu"
    except Exception as e:
        return f"[BŁĄD]: {e}"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}  # Nie twórz domyślnego config.json

def save_config(config):
    if config.get("premium_unlocked"):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f)

def verify_signature(public_key_pem, message, signature):
    public_key = serialization.load_pem_public_key(public_key_pem)
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

def ask_for_premium_key():
    print("==== Odblokuj wersję Premium ====")
    kod = input("Wpisz kod premium: ").strip()

    if not os.path.exists(PREMIUM_SIG_FILE):
        print("Brak pliku z podpisem (premium.sig).")
        input("Naciśnij Enter, aby kontynuować...")
        return False

    try:
        with open(PREMIUM_SIG_FILE, "rb") as f:
            signature = f.read()

        if verify_signature(PUBLIC_KEY_PEM, kod, signature):
            with open(PREMIUM_KEY_FILE, "w", encoding="utf-8") as f:
                f.write(kod)
            print("Klucz zaakceptowany! Wersja Premium odblokowana.")
            input("Naciśnij Enter, aby kontynuować...")
            return True
        else:
            print("Nieprawidłowy kod lub podpis.")
            input("Naciśnij Enter, aby kontynuować...")
            return False
    except Exception as e:
        print(f"Błąd weryfikacji: {e}")
        input("Naciśnij Enter, aby kontynuować...")
        return False

def scan_system(save_to_txt=True):
    try:
        print(">>> Rozpoczynam skanowanie systemu...")
        print(">>> Może to potrwać kilka minut, proszę czekać...\n")
        output = []

        output.append("[SYSTEM INFO]")
        output.append(run_cmd("ver", timeout=None))
        output.append(run_cmd("wmic os get caption", timeout=None))

        output.append("\n[STEROWNIKI - PNPUTIL]")
        output.append(run_cmd("pnputil /enum-drivers", timeout=None))

        output.append("\n[SFC SCAN - może potrwać kilka minut...]")
        output.append(run_cmd("sfc /scannow", timeout=None))

        result = "\n\n".join(output)

        print("\n=== SKANOWANIE ZAKOŃCZONE ===\n")
        if save_to_txt:
            with open(WYNIK_FILE, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"Wyniki zapisane do: {WYNIK_FILE}")
            print("\n----- ZAWARTOŚĆ WYNIKU -----\n")
            print(result)
        else:
            print(result)

        input("\nNaciśnij Enter, aby kontynuować...")
    except Exception:
        print("Wystąpił błąd podczas skanowania:")
        print(traceback.format_exc())
        input("\nNaciśnij Enter, aby kontynuować...")

def premium_settings(config):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("==== Ustawienia Premium ====")
        print(f"1. Zapis wyników do pliku TXT: {'Włączony' if config.get('save_txt', True) else 'Wyłączony'}")
        print("2. Powrót")
        choice = input("Wybierz opcję: ").strip()
        if choice == "1":
            if config.get("premium_unlocked", False):
                config["save_txt"] = not config.get("save_txt", True)
                save_config(config)
                print(f"Zapis do pliku TXT {'włączony' if config['save_txt'] else 'wyłączony'}.")
                input("Naciśnij Enter, aby kontynuować...")
            else:
                print("Opcja dostępna tylko w wersji Premium.")
                input("Naciśnij Enter, aby kontynuować...")
        elif choice == "2":
            break
        else:
            print("Niepoprawny wybór.")
            input("Naciśnij Enter, aby kontynuować...")

def start_screen():
    config = load_config()

    # Domyślne wartości robocze (RAM, nie do config.json)
    if "premium_unlocked" not in config:
        config["premium_unlocked"] = False
    if "save_txt" not in config:
        config["save_txt"] = True

    # Weryfikacja Premium na starcie
    if os.path.exists(PREMIUM_KEY_FILE) and os.path.exists(PREMIUM_SIG_FILE):
        try:
            with open(PREMIUM_KEY_FILE, "r", encoding="utf-8") as f:
                kod = f.read().strip()
            with open(PREMIUM_SIG_FILE, "rb") as f:
                sig = f.read()
            config["premium_unlocked"] = verify_signature(PUBLIC_KEY_PEM, kod, sig)
        except:
            config["premium_unlocked"] = False

    if config["premium_unlocked"]:
        save_config(config)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("==== Diagnostyka Systemu ====")
        print("1. Uruchom diagnostykę")
        if config.get("premium_unlocked", False):
            print("2. Ustawienia Premium")
        else:
            print("2. Odblokuj wersję Premium")
        print("3. Wyjście")

        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            scan_system(save_to_txt=config.get("save_txt", True))
        elif choice == "2":
            if config.get("premium_unlocked", False):
                premium_settings(config)
            else:
                if ask_for_premium_key():
                    config["premium_unlocked"] = True
                    save_config(config)
        elif choice == "3":
            print("Do widzenia!")
            break
        else:
            print("Niepoprawny wybór.")
            input("Naciśnij Enter, aby kontynuować...")

if __name__ == "__main__":
    if not is_admin():
        print("❗ Uruchom program jako administrator!")
        input("Naciśnij Enter, aby zakończyć...")
        sys.exit(1)

    try:
        start_screen()
    except Exception:
        print("Wystąpił nieoczekiwany błąd:")
        print(traceback.format_exc())
        input("\nNaciśnij Enter, aby zakończyć...")