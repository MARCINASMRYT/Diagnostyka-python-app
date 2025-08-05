# 🛠️ Diagnostyka Systemu Windows (Python)

**Aplikacja konsolowa** do przeprowadzenia szybkiej diagnostyki systemu Windows — sprawdza:

- podstawowe informacje o systemie,
- brakujące lub uszkodzone sterowniki (za pomocą `pnputil`),
- integralność plików systemowych (`sfc /scannow`),
- zapisuje wynik do pliku tekstowego `diagnostyka_wynik.txt`.

---

## 📁 Zawartość projektu

- `diagnostyka.py` – główny skrypt diagnostyczny.
- `diagnostyka_wynik.txt` – plik tworzony automatycznie z wynikami po uruchomieniu.

---

## ⚙️ Wymagania

- Windows 10 / 11  
- Python 3.x zainstalowany w systemie  
- Uprawnienia administratora  

---

## 🚀 Instrukcja uruchomienia

### ✅ PowerShell

1. Kliknij Start → wpisz `PowerShell`  
2. Kliknij prawym → **Uruchom jako administrator**  
3. Przejdź do folderu aplikacji:
   ```powershell
   cd "C:\ścieżka\do\folderu"
   ```
4. Uruchom skrypt:
   ```powershell
   python .\diagnostyka.py
   ```

---

## 📄 Wynik

Po zakończeniu działania, program:

- otwiera automatycznie plik `diagnostyka_wynik.txt`  
- zawiera wszystkie informacje i znalezione błędy (jeśli są)

---

## 🛡️ Ważne

> ⚠️ Program **musi być uruchomiony jako administrator**, inaczej zakończy się komunikatem o błędzie.
