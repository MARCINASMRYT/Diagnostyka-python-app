\# Diagnostyka Systemu - narzędzie diagnostyczne w Python



!\[Diagnostyka Systemu](screenshot.png)



\## Opis



`diagnostyka.py` to zaawansowane narzędzie diagnostyczne napisane w Pythonie, służące do analizy stanu systemu Windows. Skrypt wykonuje szereg poleceń systemowych, takich jak `sfc /scannow` oraz `pnputil /enum-drivers`, aby zidentyfikować potencjalne problemy, błędy oraz niezgodności w sterownikach i systemie operacyjnym.



\### Kluczowe funkcje:



\- Skanowanie i raportowanie informacji o systemie oraz sterownikach

\- Automatyczne wykrywanie i wyświetlanie wyników polecenia `sfc /scannow`

\- Obsługa wersji Premium z dodatkowymi opcjami konfiguracyjnymi

\- Bezpieczne odblokowanie wersji Premium za pomocą podpisanego klucza RSA

\- Zapis wyników skanowania do pliku tekstowego (opcjonalnie)



\## Wymagania



\- Python 3.7 lub nowszy

\- System Windows (wymagane uprawnienia administratora)

\- Biblioteka `cryptography` do weryfikacji podpisów RSA



\### Instalacja biblioteki



```bash

pip install cryptography

