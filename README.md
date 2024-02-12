# Pracovne-instrukcie
Projekt o prezeraní pracovných inštrukcií\
Aplikácia je v `Python 3.10`

## Project setup
Nainštalovať všetky potrebné knižnice (cez terminál): 
```
pip install -r requirements.txt
```

V súbore `src/config.ini`:
1. nastaviť `recipient_email = ...` na email, kam sa majú posielať notifikácie ohľadom blížiaceho sa konca platnosti pracovných inštrukcií.
2. v sekcii `[Preferences]` si treba nastaviť správne rozlíšenie obrazovky
3. v sekcii `[Admin]` zmeniť heslo, na požadované heslo admina (rozlišné od zamestnaneckých kódov)

### Inštrukcie a ich pracovné listy

Inštrukcie sú uložené v `resources/pdf/`

Na nahranie inštrukcie sú dva spôsoby:
1. ručne cez aplikáciu (automaticky sa skopíruje do požadovaného priečinka) 
2. presunúť inštrukcie ručne do `resources/pdf/` a spustiť `src/initalize_database.py`, ktorý ich všetky indexuje do databázy a každej sa nastaví platnosť podľa premennej `valid_until` (prednastavené na `2024-09-01`)

### Prístupové kódy zamestnancov

Nachádzajú sa v súbore `resources/employees.csv` vo formáte `kód_zamestnanca,priezvisko,meno`
