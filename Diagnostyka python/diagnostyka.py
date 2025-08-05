import subprocess
import sys
import os
import platform
import time
from datetime import datetime
import ctypes

log_file = "diagnostyka_wynik.txt"

def log(text):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def clear_log():
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"== RAPORT DIAGNOSTYKI SYSTEMU WINDOWS ==\n")
        f.write(f"Data wykonania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("="*60)
    print(title)
    print("="*60)
    log("="*60)
    log(title)
    log("="*60)

def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def system_info():
    print_header("Informacje o systemie")
    info = [
        f"Nazwa systemu: {platform.system()}",
        f"Wersja systemu: {platform.version()}",
        f"Platforma: {platform.platform()}",
        f"Architektura: {platform.architecture()[0]}",
        f"Nazwa hosta: {platform.node()}",
    ]
    for line in info:
        print(line)
        log(line)
    print()
    log("")

def check_missing_drivers():
    print_header("Sprawdzanie brakujących/uszkodzonych sterowników (pnputil)")
    try:
        result = subprocess.run(
            ['pnputil', '/enum-devices', '/problem'],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        if "Nie znaleziono urządzeń" in output or "No devices found" in output:
            msg = "✅ Wszystkie sterowniki działają prawidłowo."
            print(msg)
            log(msg)
        else:
            msg = "❌ Znaleziono urządzenia z problemami:\n"
            print(msg)
            log(msg)
            devices = output.split("\n\n")
            for device in devices:
                lines = device.strip().splitlines()
                name = ""
                problem = ""
                for line in lines:
                    if line.strip().startswith("Nazwa:") or line.strip().startswith("Name:"):
                        name = line.split(":", 1)[1].strip()
                    elif line.strip().startswith("Problem:") or line.strip().startswith("Problem Code:"):
                        problem = line.split(":", 1)[1].strip()
                if name:
                    print(f"🛑 Urządzenie: {name}")
                    print(f"    Problem: {problem}\n")
                    log(f"🛑 Urządzenie: {name}")
                    log(f"    Problem: {problem}\n")
    except Exception as e:
        print("Błąd podczas sprawdzania sterowników:", str(e))
        log(f"Błąd podczas sprawdzania sterowników: {str(e)}")
    print()
    log("")

def run_sfc_scan():
    print_header("Skanowanie integralności plików systemowych (sfc /scannow)")
    print("⏳ Trwa skanowanie SFC, proszę czekać, może to potrwać kilka minut...")
    log("Trwa skanowanie SFC, proszę czekać, może to potrwać kilka minut...")
    try:
        result = subprocess.run(['sfc', '/scannow'], capture_output=True, text=True)
        print(result.stdout)
        log(result.stdout)
    except Exception as e:
        msg = f"Błąd podczas uruchamiania SFC: {str(e)}"
        print(msg)
        log(msg)
    print()
    log("")

def open_log_file():
    try:
        os.startfile(log_file)
    except Exception as e:
        print(f"Nie udało się otworzyć pliku wynikowego: {e}")

def main():
    clear_console()

    if not check_admin():
        print("❌ Ten skrypt musi być uruchomiony jako administrator!")
        print("Kliknij prawym przyciskiem na plik i wybierz 'Uruchom jako administrator'.")
        input("Naciśnij Enter, aby zakończyć...")
        sys.exit(1)

    clear_log()
    print("🛠️  Aplikacja diagnostyczna systemu Windows\n")
    log("🛠️  Aplikacja diagnostyczna systemu Windows\n")
    time.sleep(1)

    system_info()
    time.sleep(1)

    check_missing_drivers()
    time.sleep(1)

    run_sfc_scan()
    time.sleep(1)

    msg = f"✅ Diagnostyka zakończona. Wyniki zapisano do pliku: {log_file}"
    print(msg)
    log(msg)

    open_log_file()

    input("Naciśnij Enter, aby zakończyć...")

if __name__ == "__main__":
    main()
