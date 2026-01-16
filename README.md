# Forensic Disk Populator

Een Python script dat realistische bestandssystemen genereert voor digitale forensische training en analyse.

## Overzicht

De Forensic Disk Populator is een geoptimaliseerd hulpmiddel dat duizenden realistische bestanden aanmaakt op een doelschijf. Dit is ideaal voor:

- Forensische training en oefeningen
- Testen van recovery tools
- Simuleren van bedrijfsomgevingen
- Educatieve doeleinden

## Kenmerken

### Bestandsgeneratie

Het script genereert de volgende typen bestanden:

| Categorie | Beschrijving | Aantal |
|-----------|--------------|--------|
| Documenten | TXT, DOCX, PDF, XLSX bestanden | 3.000+ |
| Afbeeldingen | JPG foto's gedownload van internet | 150+ |
| Systeembestanden | LOG, TMP, DAT bestanden | 300+ |
| Archieven | ZIP backup bestanden | 10-20 |
| Verwijderde bestanden | Gesimuleerde verwijderde data | 24 |

### Mappenstructuur

De gegenereerde structuur simuleert een Windows-omgeving:

```
Doelschijf/
    Users/
        [21 gebruikersprofielen]/
            Desktop/
            Documents/
                Work/
                Personal/
                Projects/
            Downloads/
            Pictures/
                Vacation/
                Family/
            AppData/
    Program Files/
        Microsoft Office/
        Adobe/
        Google/
        [Bedrijfsapplicaties]/
    Shared/
        [8 afdelingen]/
            Projects/
            Reports/
            Meetings/
    Windows/
        Logs/
        Temp/
    Projects/
    Archive/
    Temp/
```

### Parallelle Verwerking

Het script maakt gebruik van multithreading voor maximale snelheid:

- Automatische detectie van optimaal aantal threads
- Parallelle documentgeneratie per gebruiker
- Gelijktijdige afbeelding downloads met connection pooling
- Batch verwerking voor systeembestanden

## Vereisten

### Systeem

- Python 3.8 of hoger
- Minimaal 2 GB vrije schijfruimte
- Schrijfrechten op de doelschijf
- Internetverbinding (voor afbeelding downloads)

### Python Packages

```
requests
```

Installatie:

```bash
pip install requests
```

## Gebruik

### Basissyntax

```bash
python mega_disk_populator.py <doelschijf>
```

### Voorbeelden

Windows:

```bash
python mega_disk_populator.py D:\
python mega_disk_populator.py E:\ForensicDisk
```

Linux/Mac:

```bash
python mega_disk_populator.py /mnt/usb
python mega_disk_populator.py /media/forensic_disk
```

### Workflow

1. Start het script met het doelpad als argument
2. Bekijk de geschatte schijfruimte in de output
3. Bevestig met 'y' om door te gaan
4. Wacht tot alle stappen zijn voltooid (1-5 minuten)

## Gegenereerde Inhoud

### Gebruikersprofielen

Het script maakt 21 realistische gebruikersprofielen aan:

- John_Doe, Sarah_Smith, Mike_Johnson, etc.
- Admin en Guest accounts
- Elk profiel bevat 150-230 bestanden

### Afdelingen

Acht bedrijfsafdelingen worden gesimuleerd:

- IT, HR, Finance, Marketing
- Sales, Legal, Operations, R&D
- Elk met rapporten, vergadernotities en projectdocumenten

### Documenttemplates

Realistische inhoud wordt gegenereerd voor:

- Vergadernotities met agenda's en actiepunten
- Kwartaal- en maandrapporten met financiele gegevens
- E-mailberichten tussen medewerkers
- Contracten en serviceovereenkomsten

### Systeemartefacten

Voor forensische analyse worden aangemaakt:

- Windows systeemlogbestanden (security, application, network)
- Tijdelijke bestanden met willekeurige namen
- Cache bestanden van applicaties
- Gesimuleerde verwijderde bestanden

## Verwerkingsstappen

Het script doorloopt zeven stappen:

1. **Mappenstructuur** - Aanmaken van alle directories
2. **Documentcollectie** - Genereren van gebruikersdocumenten (parallel)
3. **Afbeeldingen** - Downloaden van foto's (parallel)
4. **Afdelingsbestanden** - Genereren van bedrijfsdocumenten (parallel)
5. **Systeembestanden** - Aanmaken van logs en temp bestanden (parallel)
6. **Archieven** - Creeren van ZIP backups (parallel)
7. **Verwijderde bestanden** - Simuleren van gewiste data

## Prestaties

### Geschatte Verwerkingstijd

| Stap | Duur |
|------|------|
| Mappenstructuur | < 5 seconden |
| Documentcollectie | 30-60 seconden |
| Afbeeldingen | 20-60 seconden |
| Afdelingsbestanden | 5-10 seconden |
| Systeembestanden | 10-20 seconden |
| Archieven | < 5 seconden |
| Verwijderde bestanden | < 1 seconde |
| **Totaal** | **1-5 minuten** |

### Optimalisaties

Het script bevat de volgende optimalisaties:

- ThreadPoolExecutor voor parallelle verwerking
- Connection pooling voor HTTP requests
- Grote write buffers (64KB) voor bestandsoperaties
- Batch verwerking van bestandstaken
- Pre-computed random waarden voor log generatie

## Aanbevolen Forensische Tools

Na het vullen van de schijf kunnen de volgende tools worden gebruikt voor analyse:

| Tool | Beschrijving |
|------|--------------|
| Autopsy | Open source forensisch platform |
| FTK Imager | Forensische imaging tool |
| Sleuth Kit | Command-line forensische tools |
| Volatility | Memory forensics framework |
| Recuva | Bestandsherstel tool |

## Schijfruimte

### Geschat Gebruik

- Documenten: circa 1-2 MB
- Afbeeldingen: circa 30-40 MB
- Systeembestanden: circa 10-15 MB
- Archieven: circa 1-2 MB
- **Totaal: circa 50-100 MB**

Het script geeft een gedetailleerde schatting voordat de verwerking begint.

## Foutafhandeling

Het script bevat robuuste foutafhandeling:

- Validatie van doelschijf voor start
- Controle van schrijfrechten
- Graceful handling van download fouten
- Gedetailleerde foutmeldingen in de log output

## Licentie

MIT License

## Versie

3.0 - Geoptimaliseerde Parallelle Editie
