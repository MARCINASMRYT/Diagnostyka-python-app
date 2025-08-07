# 🛠 Diagnostyka Systemu (Python)

![Zrzut ekranu działania aplikacji](screenshot.png)

> Zaawansowane narzędzie diagnostyczne dla systemu Windows z obsługą wersji Premium (RSA + podpis cyfrowy)

## 📦 Opis projektu

`diagnostyka.py` to interaktywny skrypt stworzony w Pythonie, który umożliwia użytkownikowi szybkie przeskanowanie systemu Windows, wykrycie problemów, oraz opcjonalne zapisanie wyników do pliku. Projekt zawiera także mechanizm weryfikacji Premium oparty na szyfrowaniu RSA i podpisach cyfrowych.

---

## 🔧 Funkcje

- ✅ Diagnostyka systemu operacyjnego (komendy `ver`, `wmic`, `sfc`)
- ✅ Skanowanie i analiza sterowników (`pnputil /enum-drivers`)
- ✅ Zapis wyników do pliku `.txt`
- ✅ Obsługa klucza Premium podpisanego RSA (funkcje Premium)
- ✅ Prosty interfejs tekstowy (CLI)

---

## 💡 Jak używać?

1. **Zainstaluj zależność:**
   ```bash
   pip install cryptography
   ```

2. **Uruchom jako administrator:**
   ```bash
   python diagnostyka.py
   ```

3. **Korzystaj z menu:**
   - `1` – Uruchamia diagnostykę
   - `2` – Odblokowuje Premium (jeśli masz podpisany klucz)
   - `3` – Zamyka aplikację

> **Uwaga:** funkcje Premium (np. zapisywanie wyników do pliku) są dostępne dopiero po poprawnej weryfikacji klucza podpisanego podpisem RSA.

---

## 🔐 Wersja Premium

Aby odblokować Premium:

1. Wygeneruj parę kluczy RSA (publiczny + prywatny)
2. W pliku `diagnostyka.py` umieść publiczny klucz RSA w zmiennej `PUBLIC_KEY_PEM`
3. Wygeneruj podpis `.sig` dla kodu użytkownika (np. w `generator.py`)
4. Dołącz do użytkownika:
   - `diagnostyka.py`
   - `premium.sig`

Po wpisaniu poprawnego kodu z podpisem — Premium zostanie aktywowane.

---

## 📂 Struktura projektu

```
📁 diagnostyka/
├── diagnostyka.py         # Główny skrypt
├── generator.py           # Skrypt do generowania podpisów
├── premium.sig            # Podpisany plik klucza
├── README.md              # Ten plik
├── screenshot.png         # Zrzut ekranu (jeśli chcesz)
```

---

## 🖼 Zrzut ekranu

Umieść obrazek `screenshot.png` w katalogu repozytorium, aby został wyświetlony powyżej.

---

## 🧪 Wymagania

- Python 3.7+
- System Windows
- Uprawnienia administratora
- Biblioteka `cryptography`

---

## 📃 Licencja

Projekt dostępny na licencji MIT – możesz używać, modyfikować i rozpowszechniać dowolnie, z zachowaniem informacji o autorze.

---

## 👤 Autor

Projekt stworzony przez **[Twoje Imię lub Nick z GitHuba]**

Chcesz pomóc? Zgłoś issue lub stwórz pull request 🙌