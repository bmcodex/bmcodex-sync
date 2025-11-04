# bmcode-sync

## Narzędzie do synchronizacji plików logów

`bmcode-sync` to proste, ale efektywne narzędzie w Pythonie, zaprojektowane do synchronizacji plików logów (lub dowolnych innych plików) między dwoma katalogami: źródłowym (`--source`) a docelowym (`--destination`).

Kluczową cechą programu jest **porównywanie plików na podstawie sum kontrolnych (hash SHA256)**. Oznacza to, że plik jest kopiowany do katalogu docelowego tylko wtedy, gdy:
1. Nie istnieje w katalogu docelowym (operacja **SKOPIOWANO**).
2. Istnieje, ale jego zawartość uległa zmianie w katalogu źródłowym (operacja **ZAKTUALIZOWANO**).

Program wykorzystuje bibliotekę `rich` do wyświetlania kolorowych i czytelnych komunikatów w terminalu.

## Instalacja

1. **Klonowanie repozytorium:**
   ```bash
   git clone https://github.com/bmcodex/bmcodex-sync.git
   cd bmcodex-sync
   ```

2. **Instalacja zależności:**
   Program wymaga jedynie biblioteki `rich`.
   ```bash
   pip install -r requirements.txt
   ```

## Użycie

Uruchomienie programu odbywa się za pomocą skryptu `sync.py` z wymaganymi argumentami `--source` i `--destination`.

### Argumenty

| Argument | Opis | Wymagany |
| :--- | :--- | :--- |
| `--source` | Ścieżka do katalogu źródłowego. | Tak |
| `--destination` | Ścieżka do katalogu docelowego (archiwum). | Tak |
| `--dry-run` | Symuluje synchronizację. Żadne pliki nie zostaną skopiowane ani zmienione. | Nie |
| `--verbose` | Wyświetla szczegółowe informacje, w tym pliki, które zostały pominięte (`POMINIĘTO`). | Nie |

### Przykład użycia

Poniższy przykład uruchamia synchronizację z katalogu `./warsztat` do `./archiwum`, wyświetlając szczegółowe komunikaty:

```bash
python sync.py --source ./warsztat --destination ./archiwum --verbose
```

## Przykładowy wynik działania

Poniżej przedstawiono przykładowy wynik działania programu z kolorowym wyjściem:

```
INFO: Znaleziono 3 plików w źródle: warsztat
SKOPIOWANO: file1.txt
SKOPIOWANO: subdir/file2.log
POMINIĘTO: file3.dat
ZAKTUALIZOWANO: config/settings.ini
```

| Status | Kolor | Opis |
| :--- | :--- | :--- |
| **SKOPIOWANO** | Zielony | Plik nie istniał w miejscu docelowym i został skopiowany. |
| **ZAKTUALIZOWANO** | Żółty | Plik istniał, ale jego suma kontrolna była inna (został zmieniony) i został nadpisany. |
| **POMINIĘTO** | Niebieski | Plik istniał i jego suma kontrolna była identyczna. |
| **DRY-RUN** | Magenta | Wskazuje, że operacja jest symulowana (tylko w trybie `--dry-run`). |

---
*Autor: Manus AI*
