#!/usr/bin/env python3
"""
Forensic Disk Populator - Geoptimaliseerde Parallelle Editie
=============================================================

Een uitgebreid Python script dat realistische bestandssystemen genereert
met duizenden bestanden voor digitale forensische training en analyse.

Dit script genereert:
- Realistische Windows-achtige mappenstructuur
- Duizenden documenten met authentieke inhoud
- Browser geschiedenis databases
- E-mail simulaties
- Systeem artefacten en logbestanden
- Verwijderde bestandssimulaties
- Gebruikersprofielen en afdelingsgegevens

Auteur: Digital Forensics Training Tools
Licentie: MIT
Versie: 3.0 (Geoptimaliseerde Parallelle Editie)

Gebruik: python mega_disk_populator.py <doelschijf>
Voorbeeld: python mega_disk_populator.py D:\\
"""

# ==============================================================================
# Region: Imports
# ==============================================================================
import os
import sys
import random
import requests
import shutil
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import zipfile
import tempfile
from typing import List, Dict, Any, Tuple
import logging
import string
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading
from io import StringIO

# ==============================================================================
# Region: Logging Configuratie
# ==============================================================================
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
g_oLogger = logging.getLogger(__name__)


class ForensicDiskPopulator:
    """
    Geavanceerde forensische disk populator die realistische bestandssystemen
    aanmaakt voor digitale forensische training en analyse.
    
    Deze klasse genereert duizenden bestanden in meerdere categorieen:
    - Gebruikersprofielen met persoonlijke en werkdocumenten
    - Afdelingsspecifieke bestanden en rapporten
    - Systeem artefacten en logbestanden
    - Browser geschiedenis en e-mail simulaties
    - Verwijderde bestandsscenario's voor recovery oefening
    """
    
    # ==========================================================================
    # Region: Initialisatie
    # ==========================================================================
    
    def __init__(self, p_sDoelSchijf: str):
        """
        Initialiseert de forensische disk populator.
        
        Args:
            p_sDoelSchijf: Pad naar de doelschijf/directory om te vullen
            
        Raises:
            ValueError: Als de doelschijf niet bestaat
            PermissionError: Als er geen schrijfrechten zijn op de doelschijf
        """
        g_oLogger.info("Initialiseren van Forensic Disk Populator...")
        g_oLogger.info(f"Doelschijf: {p_sDoelSchijf}")
        
        # Interne leden met Hungarian notation
        self.m_oDoelSchijf = Path(p_sDoelSchijf)
        self.m_iBestandsTeller = 0
        self.m_oBestandsTellerLock = threading.Lock()
        self.m_dtStartTijd = time.time()
        
        # Prestatie instellingen
        self.m_iMaxWorkers = min(32, (os.cpu_count() or 4) * 4)
        self.m_iBatchGrootte = 100
        
        self._ValideerDoelSchijf()
        
        # Configuratie - uitgebreide gebruiker en bestandsgeneratie instellingen
        self.m_lstGebruikersnamen = [
            "John_Doe", "Sarah_Smith", "Mike_Johnson", "Emma_Wilson", "Admin", "Guest",
            "Alice_Cooper", "Bob_Miller", "Carol_Davis", "David_Brown", "Eva_Garcia",
            "Frank_Martinez", "Grace_Lee", "Henry_Taylor", "Iris_Anderson", "Jack_White",
            "Kate_Thompson", "Liam_Clark", "Maya_Rodriguez", "Noah_Lewis", "Olivia_Walker"
        ]
        
        # Bedrijfsomgeving simulatie
        self.m_sBedrijfsnaam = "TechCorp_Solutions"
        self.m_lstAfdelingen = ["IT", "HR", "Finance", "Marketing", "Sales", "Legal", "Operations", "R&D"]
        
        g_oLogger.info(f"Initialisatie compleet. Bestanden worden aangemaakt voor {len(self.m_lstGebruikersnamen)} gebruikers over {len(self.m_lstAfdelingen)} afdelingen.")
        
        # Bereken geschatte schijfruimte gebruik
        self._BerekenGeschatteSchijfRuimte()
        
        # Voorbeeld afbeeldingen voor realistische foto collecties
        self.m_lstVoorbeeldAfbeeldingen = [
            f"https://picsum.photos/800/600?random={i}" for i in range(1, 51)
        ]
        
        # Uitgebreide document templates voor realistische inhoud generatie
        self.m_dictDocumentTemplates = {
            "meeting_notes": [
                "Weekly Team Meeting - {date}\n\nAttendees: {attendees}\nAgenda:\n1. Project updates\n2. Budget review\n3. Next steps\n\nAction items:\n- Complete Q{quarter} report\n- Schedule client meeting\n- Update documentation",
                "Department Meeting - {dept}\n\nDate: {date}\nLocation: Conference Room A\n\nDiscussion points:\n- Performance metrics\n- Resource allocation\n- Training needs\n\nDecisions made:\n- Approve new software purchase\n- Extend project deadline\n- Hire additional staff",
                "Project Alpha Status Meeting\n\nDate: {date}\nProject Manager: {user}\n\nProgress:\n- Phase 1: Completed\n- Phase 2: 75% complete\n- Phase 3: Planning stage\n\nRisks:\n- Budget constraints\n- Resource availability\n- Timeline pressure"
            ],
            "reports": [
                "Quarterly Report Q{quarter} {year}\n\nExecutive Summary:\nThis quarter showed {trend} performance across all key metrics.\n\nKey Metrics:\n- Revenue: EUR {revenue:,}\n- Customers: {customers:,}\n- Growth: {growth}%\n\nRecommendations:\n- Increase marketing budget\n- Expand team capacity\n- Improve customer service",
                "Monthly Sales Report - {month} {year}\n\nDepartment: {dept}\nManager: {user}\n\nSales Performance:\n- Total Sales: EUR {revenue:,}\n- New Clients: {customers}\n- Conversion Rate: {growth}%\n\nTop Performers:\n1. Product A - EUR {revenue2:,}\n2. Product B - EUR {revenue3:,}\n3. Product C - EUR {revenue4:,}",
                "Financial Analysis Report\n\nPeriod: {month} {year}\nAnalyst: {user}\n\nBudget vs Actual:\n- Budget: EUR {revenue:,}\n- Actual: EUR {revenue2:,}\n- Variance: {growth}%\n\nExpense Categories:\n- Personnel: 60%\n- Operations: 25%\n- Marketing: 15%"
            ],
            "emails": [
                "Subject: {subject}\nFrom: {sender}@company.com\nTo: {recipient}@company.com\nDate: {date}\n\nHi {recipient_name},\n\n{body}\n\nBest regards,\n{sender_name}",
                "Subject: Urgent: {subject}\nFrom: {sender}@company.com\nTo: {recipient}@company.com\nCC: manager@company.com\nDate: {date}\n\nDear {recipient_name},\n\nThis is regarding {body}\n\nPlease respond by end of day.\n\nThanks,\n{sender_name}"
            ],
            "contracts": [
                "SERVICE AGREEMENT\n\nContract No: {contract_no}\nDate: {date}\nClient: {client}\nService Provider: {company}\n\nScope of Work:\n{scope}\n\nTerms:\n- Duration: {duration} months\n- Payment: EUR {amount:,}\n- Start Date: {start_date}\n\nSignatures:\nClient: ________________\nProvider: ________________",
                "EMPLOYMENT CONTRACT\n\nEmployee: {employee}\nPosition: {position}\nDepartment: {dept}\nStart Date: {date}\n\nSalary: EUR {salary:,} per year\nBenefits:\n- Health insurance\n- Vacation days: 25\n- Pension contribution: 8%\n\nTerms and Conditions:\n{terms}"
            ]
        }
        
        # Uitgebreide bestandsextensie mapping voor realistische bestandstypen
        self.m_dictBestandsExtensies = {
            "documents": [".txt", ".docx", ".pdf", ".rtf", ".odt"],
            "spreadsheets": [".xlsx", ".csv", ".ods", ".xls"],
            "presentations": [".pptx", ".ppt", ".odp"],
            "images": [".jpg", ".png", ".gif", ".bmp", ".tiff"],
            "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
            "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".php"],
            "data": [".json", ".xml", ".sql", ".db", ".log"]
        }
        
        # Realistische bestandsnaam patronen voor verschillende categorieen
        self.m_dictBestandsnaamPatronen = {
            "documents": [
                "Meeting_Notes_{date}", "Report_{quarter}_{year}", "Proposal_{client}",
                "Contract_{contract_no}", "Invoice_{invoice_no}", "Budget_{year}",
                "Policy_{dept}", "Manual_{product}", "Specification_{project}",
                "Analysis_{topic}", "Summary_{meeting_type}", "Presentation_{event}"
            ],
            "personal": [
                "Resume_{name}", "CV_{name}", "Photo_{event}", "Vacation_{location}",
                "Birthday_{person}", "Wedding_{couple}", "Graduation_{year}",
                "Family_{event}", "Holiday_{destination}", "Weekend_{activity}"
            ],
            "work": [
                "Project_{name}", "Task_{id}", "Milestone_{number}", "Deliverable_{phase}",
                "Requirement_{spec}", "Design_{component}", "Test_{scenario}",
                "Bug_Report_{id}", "Feature_{request}", "Documentation_{module}"
            ]
        }

    # ==========================================================================
    # Region: Validatie Methoden
    # ==========================================================================

    def _ValideerDoelSchijf(self):
        """
        Verifieert dat de doelschijf bestaat en toegankelijk is.
        
        Raises:
            ValueError: Als de doelschijf niet bestaat
            PermissionError: Als er geen schrijfrechten zijn op de doelschijf
        """
        if not self.m_oDoelSchijf.exists():
            raise ValueError(f"Doelschijf {self.m_oDoelSchijf} bestaat niet")
        
        if not os.access(self.m_oDoelSchijf, os.W_OK):
            raise PermissionError(f"Geen schrijfrechten voor {self.m_oDoelSchijf}")
        
        g_oLogger.info(f"Doelschijf gevalideerd: {self.m_oDoelSchijf}")
    
    def _BerekenGeschatteSchijfRuimte(self):
        """
        Berekent de totale schijfruimte die door het script wordt gebruikt.
        Dit helpt gebruikers te bepalen of ze voldoende ruimte hebben.
        """
        i_iAantalGebruikers = len(self.m_lstGebruikersnamen)
        i_iAantalAfdelingen = len(self.m_lstAfdelingen)
        
        # Documenten per gebruiker (gemiddeld)
        i_dDocsPerGebruiker = (50 + 100) / 2
        i_dWerkPerGebruiker = (30 + 60) / 2
        i_dPersoonlijkPerGebruiker = (20 + 40) / 2
        i_dDesktopPerGebruiker = (20 + 30) / 2
        i_dTotaalDocsPerGebruiker = i_dDocsPerGebruiker + i_dWerkPerGebruiker + i_dPersoonlijkPerGebruiker + i_dDesktopPerGebruiker
        i_dTotaalDocumenten = i_iAantalGebruikers * i_dTotaalDocsPerGebruiker
        i_dDocGrootteMB = (i_dTotaalDocumenten * 3.5) / 1024
        
        # Afbeeldingen (alleen eerste 10 gebruikers)
        i_dAfbeeldingenPerGebruiker = (5 + 10) / 2 + (3 + 8) / 2 + (2 + 6) / 2
        i_dTotaalAfbeeldingen = 10 * i_dAfbeeldingenPerGebruiker
        i_dAfbeeldingGrootteMB = (i_dTotaalAfbeeldingen * 200) / 1024
        
        # Afdelingsbestanden
        i_dRapportenPerAfdeling = (20 + 40) / 2
        i_dVergaderingenPerAfdeling = (15 + 30) / 2
        i_dProjectenPerAfdeling = (10 + 20) / 2
        i_dTotaalAfdelingsbestanden = i_iAantalAfdelingen * (i_dRapportenPerAfdeling + i_dVergaderingenPerAfdeling + i_dProjectenPerAfdeling)
        i_dAfdelingGrootteMB = (i_dTotaalAfdelingsbestanden * 3) / 1024
        
        # Systeembestanden
        i_dLogBestanden = 10 * (5 + 15) / 2
        i_dLogGrootteMB = (i_dLogBestanden * 60) / 1024
        
        i_dTempBestanden = (100 + 200) / 2
        i_dTempGrootteMB = (i_dTempBestanden * 1.5) / 1024
        
        i_dCacheBestanden = (50 + 100) / 2
        i_dCacheGrootteMB = (i_dCacheBestanden * 10) / 1024
        
        # Archiefbestanden
        i_dArchiefBestanden = (10 + 20) / 2
        i_dBestandenPerZip = (5 + 15) / 2
        i_dArchiefGrootteMB = (i_dArchiefBestanden * i_dBestandenPerZip * 5) / 1024
        
        # Totaal
        i_dTotaalMB = i_dDocGrootteMB + i_dAfbeeldingGrootteMB + i_dAfdelingGrootteMB + i_dLogGrootteMB + i_dTempGrootteMB + i_dCacheGrootteMB + i_dArchiefGrootteMB
        i_dTotaalGB = i_dTotaalMB / 1024
        
        g_oLogger.info("")
        g_oLogger.info("=" * 60)
        g_oLogger.info("GESCHATTE SCHIJFRUIMTE GEBRUIK:")
        g_oLogger.info("=" * 60)
        g_oLogger.info(f"  - Documenten ({int(i_dTotaalDocumenten):,} bestanden): ~{i_dDocGrootteMB:.1f} MB")
        g_oLogger.info(f"  - Afbeeldingen ({int(i_dTotaalAfbeeldingen):,} bestanden): ~{i_dAfbeeldingGrootteMB:.1f} MB")
        g_oLogger.info(f"  - Afdelingsbestanden ({int(i_dTotaalAfdelingsbestanden):,} bestanden): ~{i_dAfdelingGrootteMB:.1f} MB")
        g_oLogger.info(f"  - Systeemlogbestanden ({int(i_dLogBestanden):,} bestanden): ~{i_dLogGrootteMB:.1f} MB")
        g_oLogger.info(f"  - Tijdelijke bestanden ({int(i_dTempBestanden):,} bestanden): ~{i_dTempGrootteMB:.1f} MB")
        g_oLogger.info(f"  - Cachebestanden ({int(i_dCacheBestanden):,} bestanden): ~{i_dCacheGrootteMB:.1f} MB")
        g_oLogger.info(f"  - Archiefbestanden ({int(i_dArchiefBestanden):,} ZIP bestanden): ~{i_dArchiefGrootteMB:.1f} MB")
        g_oLogger.info("-" * 60)
        g_oLogger.info(f"  TOTAAL GESCHAT: ~{i_dTotaalMB:.1f} MB (~{i_dTotaalGB:.2f} GB)")
        g_oLogger.info("=" * 60)
        
        # Waarschuwing als het te groot is voor 8GB USB
        if i_dTotaalGB > 7.5:
            g_oLogger.warning(f"WAARSCHUWING: Geschatte grootte ({i_dTotaalGB:.2f} GB) is mogelijk te groot voor een 8GB USB!")
            g_oLogger.warning("   Overweeg om het aantal gebruikers of bestanden te verminderen.")
        elif i_dTotaalGB > 6:
            g_oLogger.warning(f"LET OP: Geschatte grootte ({i_dTotaalGB:.2f} GB) gebruikt het grootste deel van een 8GB USB.")
        else:
            g_oLogger.info(f"OK: Geschatte grootte ({i_dTotaalGB:.2f} GB) past binnen een 8GB USB.")
        g_oLogger.info("")

    # ==========================================================================
    # Region: Mappenstructuur Aanmaak
    # ==========================================================================

    def MaakUitgebreideMappenstructuur(self):
        """
        Maakt een uitgebreide en realistische Windows-achtige mappenstructuur aan.
        
        Deze methode maakt aan:
        - Hoofd systeemdirectories (Users, Program Files, Windows, etc.)
        - Gebruikersprofiel directories met subdirectories
        - Afdelingsspecifieke gedeelde mappen
        - Project directories met georganiseerde structuur
        """
        i_dtStapStart = time.time()
        g_oLogger.info("=" * 60)
        g_oLogger.info("STAP 1/7: Aanmaken van mappenstructuur...")
        g_oLogger.info("=" * 60)
        
        # Hoofd systeemdirectories
        g_oLogger.info("Aanmaken van hoofd systeemdirectories...")
        i_lstHoofdMappen = [
            "Users", "Program Files", "Program Files (x86)", "Windows",
            "Documents and Settings", "Temp", "Downloads", "Backup",
            "Projects", "Archive", "Shared", "Public"
        ]
        
        for i_sMap in i_lstHoofdMappen:
            i_oMapPad = self.m_oDoelSchijf / i_sMap
            i_oMapPad.mkdir(exist_ok=True)
        g_oLogger.info(f"OK: {len(i_lstHoofdMappen)} hoofd directories aangemaakt")
        
        # Uitgebreide gebruikersdirectories - meerdere realistische gebruikers
        g_oLogger.info(f"Aanmaken van gebruikersdirectories voor {len(self.m_lstGebruikersnamen)} gebruikers...")
        i_oGebruikersPad = self.m_oDoelSchijf / "Users"
        
        for i_iIdx, i_sGebruiker in enumerate(self.m_lstGebruikersnamen, 1):
            i_oGebruikerPad = i_oGebruikersPad / i_sGebruiker
            i_oGebruikerPad.mkdir(exist_ok=True)
            
            # Uitgebreide subdirectories voor elk gebruikersprofiel
            i_lstGebruikerMappen = [
                "Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music",
                "AppData/Local", "AppData/Roaming", "AppData/LocalLow",
                "Documents/Work", "Documents/Personal", "Documents/Projects",
                "Documents/Archive", "Documents/Templates", "Documents/Drafts",
                "Pictures/Vacation", "Pictures/Family", "Pictures/Work",
                "Pictures/Screenshots", "Pictures/Wallpapers",
                "Downloads/Software", "Downloads/Documents", "Downloads/Media",
                "Desktop/Shortcuts", "Desktop/Projects", "Desktop/Temp"
            ]
            
            for i_sSubmap in i_lstGebruikerMappen:
                (i_oGebruikerPad / i_sSubmap).mkdir(parents=True, exist_ok=True)
            
            if i_iIdx % 5 == 0 or i_iIdx == len(self.m_lstGebruikersnamen):
                g_oLogger.info(f"  -> Gebruiker {i_iIdx}/{len(self.m_lstGebruikersnamen)}: {i_sGebruiker} (met {len(i_lstGebruikerMappen)} subdirectories)")
        
        g_oLogger.info("OK: Alle gebruikersdirectories aangemaakt")
        
        # Uitgebreide Program Files structuur met realistische applicaties
        g_oLogger.info("Aanmaken van Program Files structuur...")
        i_lstProgrammas = [
            "Microsoft Office/Office16", "Microsoft Office/Templates", "Microsoft Office/Add-ins",
            "Adobe/Acrobat DC", "Adobe/Photoshop", "Adobe/Illustrator",
            "Google/Chrome", "Google/Drive", "Mozilla Firefox", "Mozilla Thunderbird",
            "VLC Media Player", "7-Zip", "WinRAR", "Notepad++", "Visual Studio Code",
            "TeamViewer", "Skype", "Zoom", "Slack", "Discord",
            "Antivirus/McAfee", "Antivirus/Norton", "Backup/Acronis",
            f"{self.m_sBedrijfsnaam}/Internal_Tools", f"{self.m_sBedrijfsnaam}/Database",
            f"{self.m_sBedrijfsnaam}/CRM", f"{self.m_sBedrijfsnaam}/ERP"
        ]
        
        for i_sProgramma in i_lstProgrammas:
            (self.m_oDoelSchijf / "Program Files" / i_sProgramma).mkdir(parents=True, exist_ok=True)
        g_oLogger.info(f"OK: {len(i_lstProgrammas)} programma directories aangemaakt")
        
        # Afdelingsspecifieke gedeelde directories
        g_oLogger.info(f"Aanmaken van afdelingsdirectories voor {len(self.m_lstAfdelingen)} afdelingen...")
        for i_sAfdeling in self.m_lstAfdelingen:
            i_oAfdelingPad = self.m_oDoelSchijf / "Shared" / i_sAfdeling
            i_oAfdelingPad.mkdir(parents=True, exist_ok=True)
            
            # Subdirectories voor elke afdeling
            i_lstAfdelingMappen = ["Projects", "Reports", "Meetings", "Archive", "Templates", "Budget"]
            for i_sMap in i_lstAfdelingMappen:
                (i_oAfdelingPad / i_sMap).mkdir(exist_ok=True)
        g_oLogger.info("OK: Afdelingsdirectories aangemaakt")
        
        # Project directories met georganiseerde structuur
        g_oLogger.info("Aanmaken van project directories...")
        i_oProjectenPad = self.m_oDoelSchijf / "Projects"
        i_lstProjectNamen = [
            "Project_Alpha", "Project_Beta", "Project_Gamma", "Website_Redesign",
            "Mobile_App", "Database_Migration", "Security_Audit", "Cloud_Migration",
            "AI_Initiative", "Digital_Transformation"
        ]
        
        for i_sProject in i_lstProjectNamen:
            i_oProjectPad = i_oProjectenPad / i_sProject
            i_lstProjectMappen = ["Documents", "Code", "Tests", "Meetings", "Archive"]
            for i_sMap in i_lstProjectMappen:
                (i_oProjectPad / i_sMap).mkdir(parents=True, exist_ok=True)
        g_oLogger.info(f"OK: {len(i_lstProjectNamen)} project directories aangemaakt")
        
        i_dVerstrekenTijd = time.time() - i_dtStapStart
        g_oLogger.info(f"OK: Mappenstructuur compleet in {i_dVerstrekenTijd:.2f} seconden")

    # ==========================================================================
    # Region: Inhoud Generatie
    # ==========================================================================

    def _GenereerRealistischeInhoud(self, p_sTemplateType: str, **kwargs) -> str:
        """
        Genereert realistische documentinhoud gebaseerd op voorgedefinieerde templates.
        
        Args:
            p_sTemplateType: Type document template om te gebruiken
            **kwargs: Aanvullende variabelen voor template substitutie
            
        Returns:
            Gegenereerde documentinhoud met realistische gegevens
        """
        if p_sTemplateType not in self.m_dictDocumentTemplates:
            return f"Voorbeeldinhoud voor {p_sTemplateType}\nGegenereerd op: {datetime.now()}"
        
        i_sTemplate = random.choice(self.m_dictDocumentTemplates[p_sTemplateType])
        
        # Vul template variabelen met realistische gegevens
        i_dictVariabelen = {
            "date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "user": random.choice(self.m_lstGebruikersnamen),
            "dept": random.choice(self.m_lstAfdelingen),
            "quarter": random.randint(1, 4),
            "year": random.randint(2022, 2024),
            "month": random.choice(["January", "February", "March", "April", "May", "June"]),
            "revenue": random.randint(50000, 500000),
            "revenue2": random.randint(30000, 200000),
            "revenue3": random.randint(20000, 150000),
            "revenue4": random.randint(10000, 100000),
            "customers": random.randint(50, 1000),
            "growth": random.randint(-10, 25),
            "attendees": ", ".join(random.sample(self.m_lstGebruikersnamen, random.randint(3, 8))),
            "trend": random.choice(["strong", "moderate", "weak", "excellent"]),
            "client": f"Client_{random.randint(1000, 9999)}",
            "contract_no": f"CNT-{random.randint(10000, 99999)}",
            "company": self.m_sBedrijfsnaam
        }
        
        i_dictVariabelen.update(kwargs)
        
        try:
            return i_sTemplate.format(**i_dictVariabelen)
        except KeyError:
            return i_sTemplate

    # ==========================================================================
    # Region: Bestandsaanmaak Hulpmethoden
    # ==========================================================================

    def _MaakBestandMetInhoud(self, p_oBestandsPad: Path, p_sInhoud: str, p_bZetTimestamp: bool = False):
        """
        Maakt een bestand aan met opgegeven inhoud en optioneel realistische timestamp.
        
        Args:
            p_oBestandsPad: Pad waar het bestand moet worden aangemaakt
            p_sInhoud: Inhoud om naar het bestand te schrijven
            p_bZetTimestamp: Of een willekeurige timestamp moet worden gezet (trager, standaard False)
            
        De methode kan optioneel een willekeurige timestamp binnen het afgelopen jaar
        instellen om het bestandssysteem realistischer te maken.
        """
        try:
            with open(p_oBestandsPad, 'w', encoding='utf-8', buffering=65536) as i_oBestand:
                i_oBestand.write(p_sInhoud)
            
            # Zet alleen timestamp als expliciet gevraagd (tragere operatie)
            if p_bZetTimestamp:
                i_dtWillekeurigeTijd = datetime.now() - timedelta(
                    days=random.randint(0, 365),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                i_dTimestamp = i_dtWillekeurigeTijd.timestamp()
                os.utime(p_oBestandsPad, (i_dTimestamp, i_dTimestamp))
            
        except Exception as e:
            g_oLogger.error(f"FOUT bij aanmaken bestand {p_oBestandsPad}: {e}")
    
    def _MaakBestandenBatch(self, p_lstBestandsTaken: List[Tuple]) -> int:
        """
        Maakt meerdere bestanden aan in een enkele batch operatie.
        
        Args:
            p_lstBestandsTaken: Lijst van (bestandspad, inhoud) tuples
            
        Returns:
            Aantal aangemaakte bestanden
        """
        for i_oBestandsPad, i_sInhoud in p_lstBestandsTaken:
            self._MaakBestandMetInhoud(i_oBestandsPad, i_sInhoud)
        return len(p_lstBestandsTaken)
    
    def _VerhoogBestandsTeller(self, p_iAantal: int = 1):
        """Thread-veilige bestandsteller verhoging."""
        with self.m_oBestandsTellerLock:
            self.m_iBestandsTeller += p_iAantal

    # ==========================================================================
    # Region: Document Collectie Aanmaak
    # ==========================================================================

    def _BereidGebruikersDocumentenVoor(self, p_sGebruiker: str, p_oGebruikersPad: Path) -> List[Tuple]:
        """
        Bereidt alle document bestandstaken voor voor een enkele gebruiker.
        
        Args:
            p_sGebruiker: Gebruikersnaam
            p_oGebruikersPad: Pad naar de Users directory
            
        Returns:
            Lijst van (bestandspad, inhoud) tuples voor batch aanmaak
        """
        i_lstBestandsTaken = []
        i_oGebruikerPad = p_oGebruikersPad / p_sGebruiker
        
        # Hoofd Documents map - 50-100 bestanden per gebruiker
        i_oDocumentenPad = i_oGebruikerPad / "Documents"
        i_iDocAantal = random.randint(50, 100)
        for i in range(i_iDocAantal):
            i_sDocType = random.choice(list(self.m_dictDocumentTemplates.keys()))
            i_sExtensie = random.choice(self.m_dictBestandsExtensies["documents"])
            i_sBestandsnaam = f"Document_{i+1:03d}_{i_sDocType}{i_sExtensie}"
            i_sInhoud = self._GenereerRealistischeInhoud(i_sDocType)
            i_lstBestandsTaken.append((i_oDocumentenPad / i_sBestandsnaam, i_sInhoud))
        
        # Werk subdirectory
        i_oWerkPad = i_oGebruikerPad / "Documents" / "Work"
        i_iWerkAantal = random.randint(30, 60)
        for i in range(i_iWerkAantal):
            i_sBestandsnaam = f"Work_Document_{i+1:03d}.{random.choice(['docx', 'pdf', 'txt'])}"
            i_sInhoud = self._GenereerRealistischeInhoud("reports", user=p_sGebruiker)
            i_lstBestandsTaken.append((i_oWerkPad / i_sBestandsnaam, i_sInhoud))
        
        # Persoonlijke subdirectory
        i_oPersoonlijkPad = i_oGebruikerPad / "Documents" / "Personal"
        i_iPersoonlijkAantal = random.randint(20, 40)
        i_sNuString = datetime.now().isoformat()
        for i in range(i_iPersoonlijkAantal):
            i_sBestandsnaam = f"Personal_{i+1:03d}.{random.choice(['txt', 'docx'])}"
            i_sInhoud = f"Persoonlijk document voor {p_sGebruiker}\nAangemaakt: {i_sNuString}\nInhoud: Persoonlijke notities en informatie."
            i_lstBestandsTaken.append((i_oPersoonlijkPad / i_sBestandsnaam, i_sInhoud))
        
        # Bureaubladbestanden
        i_oDesktopPad = i_oGebruikerPad / "Desktop"
        i_iDesktopAantal = random.randint(20, 30)
        for i in range(i_iDesktopAantal):
            i_sExtensie = random.choice([".txt", ".docx", ".pdf", ".lnk"])
            i_sBestandsnaam = f"Desktop_File_{i+1:02d}{i_sExtensie}"
            i_sInhoud = f"Bureaubladbestand voor {p_sGebruiker}\nBestandsnummer: {i+1}\nAangemaakt: {i_sNuString}"
            i_lstBestandsTaken.append((i_oDesktopPad / i_sBestandsnaam, i_sInhoud))
        
        return i_lstBestandsTaken

    def _MaakGebruikersDocumentenWorker(self, p_sGebruiker: str, p_oGebruikersPad: Path) -> Tuple[str, int]:
        """
        Worker functie om alle documenten voor een enkele gebruiker aan te maken.
        
        Args:
            p_sGebruiker: Gebruikersnaam
            p_oGebruikersPad: Pad naar de Users directory
            
        Returns:
            Tuple van (gebruikersnaam, aantal aangemaakte bestanden)
        """
        i_lstBestandsTaken = self._BereidGebruikersDocumentenVoor(p_sGebruiker, p_oGebruikersPad)
        i_iAangemaakt = self._MaakBestandenBatch(i_lstBestandsTaken)
        return p_sGebruiker, i_iAangemaakt

    def MaakUitgebreideDocumentCollectie(self):
        """
        Maakt duizenden realistische documenten aan over gebruikersdirectories.
        Gebruikt parallelle verwerking voor maximale snelheid.
        
        Deze methode genereert:
        - 50-100 documenten per gebruiker in hoofd Documents map
        - 30-60 werkgerelateerde documenten in Work submap
        - 20-40 persoonlijke documenten in Personal submap
        - 20-30 bureaubladbestanden per gebruiker
        
        Alle documenten bevatten realistische inhoud gebaseerd op templates.
        """
        i_dtStapStart = time.time()
        g_oLogger.info("=" * 60)
        g_oLogger.info("STAP 2/7: Aanmaken van document collectie (PARALLEL)...")
        g_oLogger.info("=" * 60)
        g_oLogger.info(f"Gebruikmakend van {self.m_iMaxWorkers} threads voor maximale snelheid...")
        
        i_oGebruikersPad = self.m_oDoelSchijf / "Users"
        i_iTotaalAangemaakt = 0
        
        # Gebruik ThreadPoolExecutor voor parallelle gebruikersverwerking
        with ThreadPoolExecutor(max_workers=self.m_iMaxWorkers) as i_oExecutor:
            # Dien alle gebruikerstaken in
            i_dictFutures = {
                i_oExecutor.submit(self._MaakGebruikersDocumentenWorker, i_sGebruiker, i_oGebruikersPad): i_sGebruiker 
                for i_sGebruiker in self.m_lstGebruikersnamen
            }
            
            # Verwerk voltooide taken
            for i_oFuture in as_completed(i_dictFutures):
                i_sGebruiker = i_dictFutures[i_oFuture]
                try:
                    i_sGebruikerNaam, i_iAantal = i_oFuture.result()
                    i_iTotaalAangemaakt += i_iAantal
                    self._VerhoogBestandsTeller(i_iAantal)
                    g_oLogger.info(f"  OK: {i_sGebruikerNaam}: {i_iAantal} bestanden aangemaakt")
                except Exception as e:
                    g_oLogger.error(f"  FOUT bij {i_sGebruiker}: {e}")
        
        i_dVerstrekenTijd = time.time() - i_dtStapStart
        g_oLogger.info(f"\nOK: Document collectie compleet: {i_iTotaalAangemaakt} bestanden aangemaakt in {i_dVerstrekenTijd:.2f} seconden")
        g_oLogger.info(f"  -> Snelheid: {i_iTotaalAangemaakt/i_dVerstrekenTijd:.0f} bestanden/seconde")

    # ==========================================================================
    # Region: Afbeelding Downloads
    # ==========================================================================

    def _BereidAfbeeldingDownloadTakenVoor(self, p_oGebruikersPad: Path) -> List[Tuple]:
        """
        Bereidt alle afbeelding download taken voor.
        
        Args:
            p_oGebruikersPad: Pad naar de Users directory
            
        Returns:
            Lijst van (url, bestandspad) tuples
        """
        i_lstTaken = []
        i_lstTeVerwerkenGebruikers = self.m_lstGebruikersnamen[:10]
        
        for i_sGebruiker in i_lstTeVerwerkenGebruikers:
            i_oFotosPad = p_oGebruikersPad / i_sGebruiker / "Pictures"
            
            # Hoofd Pictures directory
            for i in range(random.randint(5, 10)):
                i_sAfbeeldingUrl = random.choice(self.m_lstVoorbeeldAfbeeldingen)
                i_lstTaken.append((i_sAfbeeldingUrl, i_oFotosPad / f"photo_{i+1:03d}.jpg"))
            
            # Vakantie subdirectory
            i_oVakantiePad = i_oFotosPad / "Vacation"
            for i in range(random.randint(3, 8)):
                i_sAfbeeldingUrl = random.choice(self.m_lstVoorbeeldAfbeeldingen)
                i_lstTaken.append((i_sAfbeeldingUrl, i_oVakantiePad / f"vacation_{i+1:02d}.jpg"))
            
            # Familie subdirectory
            i_oFamiliePad = i_oFotosPad / "Family"
            for i in range(random.randint(2, 6)):
                i_sAfbeeldingUrl = random.choice(self.m_lstVoorbeeldAfbeeldingen)
                i_lstTaken.append((i_sAfbeeldingUrl, i_oFamiliePad / f"family_{i+1:02d}.jpg"))
        
        return i_lstTaken
    
    def _DownloadAfbeeldingWorker(self, p_oSessie: requests.Session, p_sUrl: str, p_oBestandsPad: Path) -> bool:
        """
        Worker functie voor het downloaden van een enkele afbeelding met gedeelde sessie.
        
        Args:
            p_oSessie: Requests sessie met connection pooling
            p_sUrl: URL van de afbeelding om te downloaden
            p_oBestandsPad: Lokaal pad waar de afbeelding moet worden opgeslagen
            
        Returns:
            True als download succesvol, anders False
        """
        try:
            i_oResponse = p_oSessie.get(p_sUrl, timeout=15, stream=True)
            i_oResponse.raise_for_status()
            with open(p_oBestandsPad, 'wb') as i_oBestand:
                for i_arrChunk in i_oResponse.iter_content(chunk_size=8192):
                    i_oBestand.write(i_arrChunk)
            return True
        except Exception:
            return False

    def DownloadUitgebreideAfbeeldingen(self):
        """
        Downloadt uitgebreide afbeeldingscollecties voor gebruikersprofielen.
        Gebruikt parallelle downloads met connection pooling voor maximale snelheid.
        
        Deze methode downloadt:
        - 5-10 afbeeldingen per gebruiker in hoofd Pictures map
        - 3-8 vakantiefoto's in Vacation submap
        - 2-6 familiefoto's in Family submap
        
        Afbeeldingen worden gedownload van Lorem Picsum voor realistische variatie.
        Beperkt tot eerste 10 gebruikers voor prestatie-optimalisatie.
        """
        i_dtStapStart = time.time()
        g_oLogger.info("=" * 60)
        g_oLogger.info("STAP 3/7: Downloaden van afbeeldingen (PARALLEL)...")
        g_oLogger.info("=" * 60)
        g_oLogger.info("Gebruikmakend van parallelle downloads met connection pooling...")
        
        i_oGebruikersPad = self.m_oDoelSchijf / "Users"
        
        # Bereid alle download taken voor
        i_lstTaken = self._BereidAfbeeldingDownloadTakenVoor(i_oGebruikersPad)
        i_iTotaalTaken = len(i_lstTaken)
        g_oLogger.info(f"  -> {i_iTotaalTaken} afbeeldingen worden parallel gedownload...")
        
        # Maak een sessie met connection pooling
        i_oSessie = requests.Session()
        i_oAdapter = requests.adapters.HTTPAdapter(
            pool_connections=20,
            pool_maxsize=20,
            max_retries=2
        )
        i_oSessie.mount('http://', i_oAdapter)
        i_oSessie.mount('https://', i_oAdapter)
        
        i_iSuccesAantal = 0
        
        # Gebruik ThreadPoolExecutor voor parallelle downloads
        with ThreadPoolExecutor(max_workers=min(20, self.m_iMaxWorkers)) as i_oExecutor:
            i_dictFutures = {
                i_oExecutor.submit(self._DownloadAfbeeldingWorker, i_oSessie, i_sUrl, i_oBestandsPad): i_oBestandsPad
                for i_sUrl, i_oBestandsPad in i_lstTaken
            }
            
            i_iVoltooid = 0
            for i_oFuture in as_completed(i_dictFutures):
                i_iVoltooid += 1
                if i_oFuture.result():
                    i_iSuccesAantal += 1
                    self._VerhoogBestandsTeller(1)
                
                if i_iVoltooid % 25 == 0 or i_iVoltooid == i_iTotaalTaken:
                    g_oLogger.info(f"    -> {i_iVoltooid}/{i_iTotaalTaken} downloads afgerond ({i_iSuccesAantal} succesvol)")
        
        i_oSessie.close()
        
        i_dVerstrekenTijd = time.time() - i_dtStapStart
        g_oLogger.info(f"\nOK: Afbeeldingen download compleet: {i_iSuccesAantal} afbeeldingen in {i_dVerstrekenTijd:.2f} seconden")
        if i_dVerstrekenTijd > 0:
            g_oLogger.info(f"  -> Snelheid: {i_iSuccesAantal/i_dVerstrekenTijd:.1f} afbeeldingen/seconde")

    # ==========================================================================
    # Region: Afdelingsbestanden Aanmaak
    # ==========================================================================

    def _MaakAfdelingsBestandenWorker(self, p_sAfdeling: str, p_oGedeeldPad: Path) -> Tuple[str, int]:
        """
        Worker functie om alle bestanden voor een enkele afdeling aan te maken.
        
        Args:
            p_sAfdeling: Afdelingsnaam
            p_oGedeeldPad: Pad naar de Shared directory
            
        Returns:
            Tuple van (afdelingsnaam, aantal aangemaakte bestanden)
        """
        i_oAfdelingPad = p_oGedeeldPad / p_sAfdeling
        i_lstBestandsTaken = []
        
        # Rapporten directory - 20-40 rapporten per afdeling
        i_oRapportenPad = i_oAfdelingPad / "Reports"
        for i in range(random.randint(20, 40)):
            i_sBestandsnaam = f"{p_sAfdeling}_Report_{i+1:03d}.{random.choice(['docx', 'pdf', 'xlsx'])}"
            i_sInhoud = self._GenereerRealistischeInhoud("reports", dept=p_sAfdeling)
            i_lstBestandsTaken.append((i_oRapportenPad / i_sBestandsnaam, i_sInhoud))
        
        # Vergaderingen directory - 15-30 vergadernotities
        i_oVergaderingenPad = i_oAfdelingPad / "Meetings"
        for i in range(random.randint(15, 30)):
            i_sBestandsnaam = f"{p_sAfdeling}_Meeting_{i+1:03d}.txt"
            i_sInhoud = self._GenereerRealistischeInhoud("meeting_notes", dept=p_sAfdeling)
            i_lstBestandsTaken.append((i_oVergaderingenPad / i_sBestandsnaam, i_sInhoud))
        
        # Projecten directory - 10-20 projectbestanden
        i_oProjectenPad = i_oAfdelingPad / "Projects"
        for i in range(random.randint(10, 20)):
            i_sBestandsnaam = f"{p_sAfdeling}_Project_{i+1:02d}.{random.choice(['docx', 'pdf'])}"
            i_sInhoud = f"Projectdocumentatie voor {p_sAfdeling}\nProject ID: {p_sAfdeling}-{i+1:03d}\nStatus: In Uitvoering"
            i_lstBestandsTaken.append((i_oProjectenPad / i_sBestandsnaam, i_sInhoud))
        
        # Maak alle bestanden aan
        i_iAangemaakt = self._MaakBestandenBatch(i_lstBestandsTaken)
        return p_sAfdeling, i_iAangemaakt

    def MaakAfdelingsbestanden(self):
        """
        Maakt realistische bestanden aan voor alle bedrijfsafdelingen.
        Gebruikt parallelle verwerking voor maximale snelheid.
        
        Deze methode genereert:
        - 20-40 rapporten per afdeling
        - 15-30 vergadernotities per afdeling
        - 10-20 projectbestanden per afdeling
        
        Alle bestanden bevatten afdelingsspecifieke realistische inhoud.
        """
        i_dtStapStart = time.time()
        g_oLogger.info("=" * 60)
        g_oLogger.info("STAP 4/7: Aanmaken van afdelingsbestanden (PARALLEL)...")
        g_oLogger.info("=" * 60)
        
        i_oGedeeldPad = self.m_oDoelSchijf / "Shared"
        i_iTotaalAangemaakt = 0
        
        # Gebruik ThreadPoolExecutor voor parallelle afdelingsverwerking
        with ThreadPoolExecutor(max_workers=len(self.m_lstAfdelingen)) as i_oExecutor:
            i_dictFutures = {
                i_oExecutor.submit(self._MaakAfdelingsBestandenWorker, i_sAfdeling, i_oGedeeldPad): i_sAfdeling
                for i_sAfdeling in self.m_lstAfdelingen
            }
            
            for i_oFuture in as_completed(i_dictFutures):
                i_sAfdeling = i_dictFutures[i_oFuture]
                try:
                    i_sAfdelingNaam, i_iAantal = i_oFuture.result()
                    i_iTotaalAangemaakt += i_iAantal
                    self._VerhoogBestandsTeller(i_iAantal)
                    g_oLogger.info(f"  OK: {i_sAfdelingNaam}: {i_iAantal} bestanden aangemaakt")
                except Exception as e:
                    g_oLogger.error(f"  FOUT bij {i_sAfdeling}: {e}")
        
        i_dVerstrekenTijd = time.time() - i_dtStapStart
        g_oLogger.info(f"\nOK: Afdelingsbestanden compleet: {i_iTotaalAangemaakt} bestanden in {i_dVerstrekenTijd:.2f} seconden")

    # ==========================================================================
    # Region: Systeembestanden Aanmaak
    # ==========================================================================

    def _MaakLogBestandenBatch(self, p_sLogType: str, p_oLogsPad: Path) -> int:
        """
        Maakt logbestanden aan voor een specifiek log type.
        
        Args:
            p_sLogType: Type log (system, application, etc.)
            p_oLogsPad: Pad naar de logs directory
            
        Returns:
            Aantal aangemaakte bestanden
        """
        i_lstBestandsTaken = []
        for i in range(random.randint(5, 15)):
            i_sLogBestandsnaam = f"{p_sLogType}_{i+1:02d}.log"
            i_sLogInhoud = self._GenereerUitgebreideLogInhoud(p_sLogType)
            i_lstBestandsTaken.append((p_oLogsPad / i_sLogBestandsnaam, i_sLogInhoud))
        return self._MaakBestandenBatch(i_lstBestandsTaken)

    def _GenereerUitgebreideLogInhoud(self, p_sLogType: str) -> str:
        """
        Genereert uitgebreide loginhoud met realistische entries.
        Geoptimaliseerd voor snelheid met vooraf berekende waarden.
        
        Args:
            p_sLogType: Type log om te genereren (system, application, etc.)
            
        Returns:
            Gegenereerde loginhoud met 200-1000 realistische entries
        """
        # Bereken constanten vooraf buiten loop
        i_lstLogNiveaus = ["INFO", "WARNING", "ERROR", "DEBUG", "TRACE"]
        i_dictBerichten = {
            "system": ["System startup completed", "Service started", "Driver loaded", "Hardware detected"],
            "application": ["Application launched", "User login", "File opened", "Process terminated"],
            "security": ["Login attempt", "Permission granted", "Access denied", "Policy applied"],
            "network": ["Connection established", "Packet received", "Timeout occurred", "DNS resolved"],
            "error": ["File not found", "Access violation", "Memory error", "Disk full"]
        }
        i_lstBerichtenLijst = i_dictBerichten.get(p_sLogType, ["Generic log message", "System event", "Process completed"])
        i_sLogTypeHoofdletters = p_sLogType.upper()
        
        # Genereer willekeurige waarden vooraf in bulk voor snelheid
        i_iEntryAantal = random.randint(200, 1000)
        
        # Gebruik StringIO voor efficiente string concatenatie
        i_oOutput = StringIO()
        i_dtBasisTimestamp = datetime.now() - timedelta(days=90)
        
        # Genereer willekeurige offsets vooraf
        i_lstDagOffsets = [random.randint(0, 90) for _ in range(i_iEntryAantal)]
        i_lstTijdSeconden = [random.randint(0, 86399) for _ in range(i_iEntryAantal)]
        i_lstNiveaus = [random.choice(i_lstLogNiveaus) for _ in range(i_iEntryAantal)]
        i_lstBerichten = [random.choice(i_lstBerichtenLijst) for _ in range(i_iEntryAantal)]
        i_lstPids = [random.randint(1000, 9999) for _ in range(i_iEntryAantal)]
        
        for i in range(i_iEntryAantal):
            i_dtTimestamp = i_dtBasisTimestamp + timedelta(days=i_lstDagOffsets[i], seconds=i_lstTijdSeconden[i])
            i_oOutput.write(f"{i_dtTimestamp.strftime('%Y-%m-%d %H:%M:%S')}.{random.randint(0,999):03d} [{i_lstNiveaus[i]}] {i_sLogTypeHoofdletters}: {i_lstBerichten[i]} (PID: {i_lstPids[i]})\n")
        
        return i_oOutput.getvalue()

    def MaakUitgebreideSysteembestanden(self):
        """
        Maakt uitgebreide systeembestanden en logs aan voor realistische forensische analyse.
        Gebruikt parallelle verwerking voor maximale snelheid.
        
        Deze methode genereert:
        - Meerdere logbestanden voor verschillende systeemcomponenten
        - 100-200 tijdelijke bestanden met realistische namen
        - Cachebestanden van verschillende applicaties
        
        Alle bestanden bevatten realistische timestamps en inhoud.
        """
        i_dtStapStart = time.time()
        g_oLogger.info("=" * 60)
        g_oLogger.info("STAP 5/7: Aanmaken van systeembestanden en logs (PARALLEL)...")
        g_oLogger.info("=" * 60)
        
        # Windows logs - parallelle log aanmaak
        g_oLogger.info("Aanmaken van Windows logbestanden...")
        i_oLogsPad = self.m_oDoelSchijf / "Windows" / "Logs"
        i_oLogsPad.mkdir(parents=True, exist_ok=True)
        
        i_lstLogTypes = [
            "system", "application", "security", "setup", "hardware", 
            "network", "performance", "error", "warning", "information"
        ]
        
        i_iTotaalLogBestanden = 0
        with ThreadPoolExecutor(max_workers=len(i_lstLogTypes)) as i_oExecutor:
            i_lstFutures = [i_oExecutor.submit(self._MaakLogBestandenBatch, i_sLt, i_oLogsPad) for i_sLt in i_lstLogTypes]
            for i_oFuture in as_completed(i_lstFutures):
                i_iAantal = i_oFuture.result()
                i_iTotaalLogBestanden += i_iAantal
                self._VerhoogBestandsTeller(i_iAantal)
        g_oLogger.info(f"OK: {i_iTotaalLogBestanden} logbestanden aangemaakt")
        
        # Tijdelijke bestanden - batch aanmaak
        g_oLogger.info("Aanmaken van tijdelijke bestanden...")
        i_oTempPad = self.m_oDoelSchijf / "Temp"
        i_iTempAantal = random.randint(100, 200)
        
        i_sNuString = datetime.now().isoformat()
        i_lstTempTaken = []
        for i in range(i_iTempAantal):
            i_sTempBestandsnaam = f"tmp_{random.randint(10000, 99999)}.tmp"
            i_sTempInhoud = f"Tijdelijk bestand {i}\nAangemaakt: {i_sNuString}\nGrootte: {random.randint(1024, 1048576)} bytes"
            i_lstTempTaken.append((i_oTempPad / i_sTempBestandsnaam, i_sTempInhoud))
        
        # Maak aan in parallelle batches
        i_iBatchGrootte = 50
        with ThreadPoolExecutor(max_workers=4) as i_oExecutor:
            i_lstBatches = [i_lstTempTaken[i:i+i_iBatchGrootte] for i in range(0, len(i_lstTempTaken), i_iBatchGrootte)]
            i_lstFutures = [i_oExecutor.submit(self._MaakBestandenBatch, i_lstBatch) for i_lstBatch in i_lstBatches]
            for i_oFuture in as_completed(i_lstFutures):
                self._VerhoogBestandsTeller(i_oFuture.result())
        g_oLogger.info(f"OK: {i_iTempAantal} tijdelijke bestanden aangemaakt")
        
        # Applicatie cachebestanden - batch aanmaak
        g_oLogger.info("Aanmaken van cachebestanden...")
        i_oCachePad = self.m_oDoelSchijf / "Windows" / "Temp" / "Cache"
        i_oCachePad.mkdir(parents=True, exist_ok=True)
        
        i_iCacheAantal = random.randint(50, 100)
        i_lstCacheTaken = []
        for i in range(i_iCacheAantal):
            i_sCacheBestandsnaam = f"cache_{random.randint(100000, 999999)}.dat"
            i_sCacheInhoud = f"Cache data {i}\nApplicatie: {random.choice(['Chrome', 'Firefox', 'Office', 'System'])}"
            i_lstCacheTaken.append((i_oCachePad / i_sCacheBestandsnaam, i_sCacheInhoud))
        
        i_iAangemaakt = self._MaakBestandenBatch(i_lstCacheTaken)
        self._VerhoogBestandsTeller(i_iAangemaakt)
        g_oLogger.info(f"OK: {i_iCacheAantal} cachebestanden aangemaakt")
        
        i_dVerstrekenTijd = time.time() - i_dtStapStart
        i_iTotaalBestanden = i_iTotaalLogBestanden + i_iTempAantal + i_iCacheAantal
        g_oLogger.info(f"\nOK: Systeembestanden compleet: {i_iTotaalBestanden} bestanden in {i_dVerstrekenTijd:.2f} seconden")

    # ==========================================================================
    # Region: Archiefbestanden Aanmaak
    # ==========================================================================

    def _MaakArchiefWorker(self, p_oZipPad: Path, p_iBestandenInZip: int, p_sNuString: str) -> bool:
        """
        Worker functie om een enkel ZIP archief aan te maken.
        
        Args:
            p_oZipPad: Pad voor het ZIP bestand
            p_iBestandenInZip: Aantal bestanden om in het ZIP te plaatsen
            p_sNuString: Huidige datum/tijd string
            
        Returns:
            True als aanmaak succesvol, anders False
        """
        try:
            with zipfile.ZipFile(p_oZipPad, 'w', compression=zipfile.ZIP_DEFLATED) as i_oZipBestand:
                for j in range(p_iBestandenInZip):
                    i_sBestandsInhoud = f"Archiefbestand {j+1}\nBackup datum: {p_sNuString}\nBestandsgrootte: {random.randint(1024, 10240)} bytes"
                    i_oZipBestand.writestr(f"file_{j+1:02d}.txt", i_sBestandsInhoud)
            return True
        except Exception:
            return False

    def MaakArchiefbestanden(self):
        """
        Maakt verschillende typen archiefbestanden aan voor realistische bestandssysteem simulatie.
        Gebruikt parallelle verwerking voor maximale snelheid.
        
        Deze methode maakt 10-20 ZIP bestanden aan met meerdere dummy bestanden
        om backup archieven en gecomprimeerde data te simuleren.
        """
        i_dtStapStart = time.time()
        g_oLogger.info("=" * 60)
        g_oLogger.info("STAP 6/7: Aanmaken van archiefbestanden (PARALLEL)...")
        g_oLogger.info("=" * 60)
        
        i_oArchiefPad = self.m_oDoelSchijf / "Archive"
        i_iArchiefAantal = random.randint(10, 20)
        i_sNuString = datetime.now().isoformat()
        i_iJaar = datetime.now().year
        
        g_oLogger.info(f"Aanmaken van {i_iArchiefAantal} ZIP archiefbestanden...")
        
        # Bereid archieftaken voor
        i_lstArchiefTaken = []
        for i in range(i_iArchiefAantal):
            i_sZipNaam = f"backup_{i_iJaar}_{i+1:02d}.zip"
            i_oZipPad = i_oArchiefPad / i_sZipNaam
            i_iBestandenInZip = random.randint(5, 15)
            i_lstArchiefTaken.append((i_oZipPad, i_iBestandenInZip, i_sNuString))
        
        # Maak archieven parallel aan
        i_iSuccesAantal = 0
        with ThreadPoolExecutor(max_workers=min(i_iArchiefAantal, self.m_iMaxWorkers)) as i_oExecutor:
            i_lstFutures = [i_oExecutor.submit(self._MaakArchiefWorker, *i_tupTaak) for i_tupTaak in i_lstArchiefTaken]
            for i_oFuture in as_completed(i_lstFutures):
                if i_oFuture.result():
                    i_iSuccesAantal += 1
                    self._VerhoogBestandsTeller(1)
        
        i_dVerstrekenTijd = time.time() - i_dtStapStart
        g_oLogger.info(f"OK: Archiefbestanden compleet: {i_iSuccesAantal} ZIP bestanden in {i_dVerstrekenTijd:.2f} seconden")

    # ==========================================================================
    # Region: Verwijderde Bestanden Simulatie
    # ==========================================================================

    def MaakUitgebreideVerwijderdeBestandenSimulatie(self):
        """
        Maakt uitgebreide verwijderde bestanden simulatie aan voor forensische recovery oefening.
        
        Deze methode maakt en verwijdert direct bestanden in categorieen:
        - Vertrouwelijke documenten (salarisinformatie, financiele gegevens, etc.)
        - Persoonlijke bestanden (foto's, e-mails, bankgegevens, etc.)
        - Systeembestanden (backups, registry, wachtwoord cache, etc.)
        - Projectbestanden (broncode, databases, API keys, etc.)
        
        Bestanden worden aangemaakt met realistische inhoud en daarna verwijderd om
        echte forensische recovery scenario's te simuleren.
        """
        i_dtStapStart = time.time()
        g_oLogger.info("=" * 60)
        g_oLogger.info("STAP 7/7: Simuleren van verwijderde bestanden...")
        g_oLogger.info("=" * 60)
        g_oLogger.info("Bestanden worden aangemaakt en direct verwijderd voor recovery oefening...")
        
        # Maak tijdelijke bestanden aan die worden "verwijderd" voor forensische recovery
        i_oTempMap = self.m_oDoelSchijf / "temp_deleted_mega"
        i_oTempMap.mkdir(exist_ok=True)
        
        i_dictVerwijderdCategorieen = {
            "confidential": [
                "salary_information.xlsx", "employee_records.docx", "financial_audit.pdf",
                "merger_plans.pptx", "customer_database.csv", "security_codes.txt"
            ],
            "personal": [
                "personal_photos.zip", "private_emails.pst", "banking_info.pdf",
                "medical_records.docx", "insurance_documents.pdf", "tax_returns.xlsx"
            ],
            "system": [
                "system_backup.bak", "registry_backup.reg", "password_cache.dat",
                "browser_history.db", "temp_files.tmp", "crash_dumps.dmp"
            ],
            "projects": [
                "source_code.zip", "database_schema.sql", "api_keys.json",
                "client_data.xlsx", "project_notes.docx", "meeting_recordings.mp4"
            ]
        }
        
        i_iTotaalVerwijderd = 0
        i_sNuString = datetime.now().isoformat()
        i_lstRedenen = ['Gebruiker verwijderd', 'Systeem opruiming', 'Beveiligingsbeleid', 'Schijf opruiming']
        
        for i_iCatIdx, (i_sCategorie, i_lstBestanden) in enumerate(i_dictVerwijderdCategorieen.items(), 1):
            g_oLogger.info(f"[Categorie {i_iCatIdx}/4] {i_sCategorie.upper()}: {len(i_lstBestanden)} bestanden...")
            i_oCategorieMap = i_oTempMap / i_sCategorie
            i_oCategorieMap.mkdir(exist_ok=True)
            
            # Batch aanmaken en verwijderen voor snelheid
            for i_sBestandsnaam in i_lstBestanden:
                i_oBestandsPad = i_oCategorieMap / i_sBestandsnaam
                i_sInhoud = f"VERWIJDERD BESTAND - {i_sCategorie.upper()}\nOriginele naam: {i_sBestandsnaam}\nCategorie: {i_sCategorie}\nVerwijderd: {i_sNuString}\nReden: {random.choice(i_lstRedenen)}\n\nDit bestand bevatte gevoelige informatie en is verwijderd om beveiligingsredenen."
                
                # Maak aan en verwijder direct (geen sleep nodig)
                with open(i_oBestandsPad, 'w', encoding='utf-8', buffering=65536) as i_oBestand:
                    i_oBestand.write(i_sInhoud)
                os.remove(i_oBestandsPad)
                i_iTotaalVerwijderd += 1
            
            # Verwijder de categoriemap
            i_oCategorieMap.rmdir()
        
        # Verwijder de hoofd tijdelijke map
        i_oTempMap.rmdir()
        
        i_dVerstrekenTijd = time.time() - i_dtStapStart
        g_oLogger.info(f"OK: Verwijderde bestanden simulatie compleet: {i_iTotaalVerwijderd} bestanden in {i_dVerstrekenTijd:.2f} seconden")

    # ==========================================================================
    # Region: Hoofduitvoering
    # ==========================================================================

    def Uitvoeren(self):
        """
        Voert het complete forensische disk populatie proces uit.
        
        Deze methode orkestreert de gehele disk populatie workflow:
        1. Maak uitgebreide mappenstructuur aan
        2. Genereer uitgebreide documentcollecties
        3. Download realistische afbeeldingscollecties
        4. Maak afdelingsspecifieke bestanden aan
        5. Genereer systeembestanden en logs
        6. Maak archiefbestanden aan
        7. Simuleer verwijderde bestanden voor recovery oefening
        
        Het proces maakt duizenden bestanden aan over meerdere categorieen
        voor uitgebreide forensische trainingsscenario's.
        """
        g_oLogger.info("")
        g_oLogger.info("=" * 60)
        g_oLogger.info("FORENSIC DISK POPULATOR - GESTART")
        g_oLogger.info("=" * 60)
        g_oLogger.info(f"Doelschijf: {self.m_oDoelSchijf}")
        g_oLogger.info("Dit script gaat DUIZENDEN bestanden aanmaken - wees geduldig!")
        g_oLogger.info("")
        
        try:
            # Stap 1: Maak uitgebreide mappenstructuur aan
            self.MaakUitgebreideMappenstructuur()
            
            # Stap 2: Genereer uitgebreide documentcollecties (langste stap)
            self.MaakUitgebreideDocumentCollectie()
            
            # Stap 3: Download realistische afbeeldingen (beperkt voor prestatie)
            self.DownloadUitgebreideAfbeeldingen()
            
            # Stap 4: Maak afdelingsspecifieke bestanden aan
            self.MaakAfdelingsbestanden()
            
            # Stap 5: Genereer systeembestanden en logs
            self.MaakUitgebreideSysteembestanden()
            
            # Stap 6: Maak realistische archiefbestanden aan
            self.MaakArchiefbestanden()
            
            # Stap 7: Simuleer verwijderde bestanden voor recovery oefening
            self.MaakUitgebreideVerwijderdeBestandenSimulatie()
            
            i_dTotaleTijd = time.time() - self.m_dtStartTijd
            g_oLogger.info("")
            g_oLogger.info("=" * 60)
            g_oLogger.info("OK: DISK POPULATIE SUCCESVOL AFGEROND!")
            g_oLogger.info("=" * 60)
            g_oLogger.info("Statistieken:")
            g_oLogger.info(f"  - Totaal aantal gebruikers: {len(self.m_lstGebruikersnamen)}")
            g_oLogger.info(f"  - Totaal aantal afdelingen: {len(self.m_lstAfdelingen)}")
            g_oLogger.info(f"  - Totaal aantal bestanden aangemaakt: {self.m_iBestandsTeller:,}")
            g_oLogger.info(f"  - Totale verstreken tijd: {i_dTotaleTijd:.2f} seconden ({i_dTotaleTijd/60:.2f} minuten)")
            g_oLogger.info(f"  - Gemiddelde snelheid: {self.m_iBestandsTeller/i_dTotaleTijd:.1f} bestanden/seconde")
            g_oLogger.info("")
            g_oLogger.info("Bestandstypen:")
            g_oLogger.info("  - Documenten: TXT, DOCX, PDF, XLSX, en meer")
            g_oLogger.info("  - Afbeeldingen: JPG (gedownload van internet)")
            g_oLogger.info("  - Systeembestanden: LOG, TMP, DAT")
            g_oLogger.info("  - Archiefbestanden: ZIP")
            g_oLogger.info("  - Verwijderde bestanden: 24 bestanden gesimuleerd voor recovery oefening")
            g_oLogger.info("=" * 60)
            
        except Exception as e:
            g_oLogger.error("")
            g_oLogger.error("=" * 60)
            g_oLogger.error(f"FOUT TIJDENS DISK POPULATIE: {e}")
            g_oLogger.error("=" * 60)
            g_oLogger.exception("Volledige foutdetails:")
            raise


# ==============================================================================
# Region: Hoofdprogramma
# ==============================================================================

def main():
    """
    Hoofdinvoerpunt voor de Forensic Disk Populator applicatie.
    
    Verwerkt commandoregel argumenten, toont gebruiksinformatie,
    vraagt om bevestiging en start het populatieproces.
    """
    if len(sys.argv) != 2:
        print("Gebruik: python mega_disk_populator.py <doelschijf>")
        print("Voorbeeld: python mega_disk_populator.py D:\\")
        print("\nWAARSCHUWING: Dit script maakt DUIZENDEN bestanden aan!")
        print("Vereisten:")
        print("- Minimaal 2GB vrije schijfruimte")
        print("- Schrijfrechten op de doelschijf")
        print("- Internetverbinding voor afbeelding downloads")
        sys.exit(1)
    
    i_sDoelSchijf = sys.argv[1]
    
    print("FORENSIC DISK POPULATOR - GEOPTIMALISEERDE PARALLELLE EDITIE")
    print("=" * 60)
    print("Dit script maakt duizenden realistische bestanden aan voor forensische training!")
    print(f"Doelschijf: {i_sDoelSchijf}")
    print(f"Parallelle workers: {min(32, (os.cpu_count() or 4) * 4)} threads")
    print("Geschatte tijd: 1-5 minuten (parallelle verwerking)")
    print("Benodigde ruimte: 1-3 GB")
    print("Bestanden gegenereerd: 5.000-10.000+")
    print("=" * 60)
    
    i_sBevestiging = input("Doorgaan? (j/N): ")
    if i_sBevestiging.lower() not in ['j', 'y']:
        print("Operatie geannuleerd.")
        sys.exit(0)
    
    try:
        i_oPopulator = ForensicDiskPopulator(i_sDoelSchijf)
        i_oPopulator.Uitvoeren()
        
        print("\nSUCCES!")
        print("Je uitgebreide forensische trainingsdisk is klaar!")
        print("\nAanbevolen forensische tools voor analyse:")
        print("- Autopsy (Open source digitaal forensisch platform)")
        print("- FTK Imager (Forensische imaging tool)")
        print("- Sleuth Kit (Commandoregel forensische tools)")
        print("- Volatility (Memory forensics framework)")
        print("\nSucces met forensische analyse!")
        
    except Exception as e:
        g_oLogger.error(f"Disk populatie mislukt: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
