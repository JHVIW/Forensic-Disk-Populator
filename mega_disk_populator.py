#!/usr/bin/env python3
"""
Forensic Disk Populator - Advanced Edition
==========================================

A comprehensive Python script that creates realistic file systems with thousands of files
for digital forensics training and analysis purposes.

This script generates:
- Realistic Windows-like directory structure
- Thousands of documents with authentic content
- Browser history databases
- Email simulations
- System artifacts and logs
- Deleted file simulations
- User profiles and departmental data

Author: Digital Forensics Training Tools
License: MIT
Version: 2.0

Usage: python mega_disk_populator.py <target_drive>
Example: python mega_disk_populator.py D:\
"""

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
from typing import List, Dict, Any
import logging
import string
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ForensicDiskPopulator:
    """
    Advanced forensic disk populator that creates realistic file systems
    for digital forensics training and analysis.
    
    This class generates thousands of files across multiple categories:
    - User profiles with personal and work documents
    - Department-specific files and reports
    - System artifacts and logs
    - Browser history and email simulations
    - Deleted file scenarios for recovery practice
    """
    def __init__(self, target_drive: str):
        """
        Initialize the forensic disk populator.
        
        Args:
            target_drive (str): Path to the target drive/directory to populate
            
        Raises:
            ValueError: If target drive doesn't exist
            PermissionError: If no write permission to target drive
        """
        self.target_drive = Path(target_drive)
        self.ensure_target_exists()
        
        # Configuration - extensive user and file generation settings
        # Realistic user profiles for file generation
        self.user_names = [
            "John_Doe", "Sarah_Smith", "Mike_Johnson", "Emma_Wilson", "Admin", "Guest",
            "Alice_Cooper", "Bob_Miller", "Carol_Davis", "David_Brown", "Eva_Garcia",
            "Frank_Martinez", "Grace_Lee", "Henry_Taylor", "Iris_Anderson", "Jack_White",
            "Kate_Thompson", "Liam_Clark", "Maya_Rodriguez", "Noah_Lewis", "Olivia_Walker"
        ]
        
        # Corporate environment simulation
        self.company_name = "TechCorp_Solutions"
        self.departments = ["IT", "HR", "Finance", "Marketing", "Sales", "Legal", "Operations", "R&D"]
        
        # Sample images for realistic photo collections
        self.sample_images = [
            f"https://picsum.photos/800/600?random={i}" for i in range(1, 51)  # 50 different images
        ]
        
        # Comprehensive document templates for realistic content generation
        self.document_templates = {
            "meeting_notes": [
                "Weekly Team Meeting - {date}\n\nAttendees: {attendees}\nAgenda:\n1. Project updates\n2. Budget review\n3. Next steps\n\nAction items:\n- Complete Q{quarter} report\n- Schedule client meeting\n- Update documentation",
                "Department Meeting - {dept}\n\nDate: {date}\nLocation: Conference Room A\n\nDiscussion points:\n- Performance metrics\n- Resource allocation\n- Training needs\n\nDecisions made:\n- Approve new software purchase\n- Extend project deadline\n- Hire additional staff",
                "Project Alpha Status Meeting\n\nDate: {date}\nProject Manager: {user}\n\nProgress:\n- Phase 1: Completed\n- Phase 2: 75% complete\n- Phase 3: Planning stage\n\nRisks:\n- Budget constraints\n- Resource availability\n- Timeline pressure"
            ],
            "reports": [
                "Quarterly Report Q{quarter} {year}\n\nExecutive Summary:\nThis quarter showed {trend} performance across all key metrics.\n\nKey Metrics:\n- Revenue: €{revenue:,}\n- Customers: {customers:,}\n- Growth: {growth}%\n\nRecommendations:\n- Increase marketing budget\n- Expand team capacity\n- Improve customer service",
                "Monthly Sales Report - {month} {year}\n\nDepartment: {dept}\nManager: {user}\n\nSales Performance:\n- Total Sales: €{revenue:,}\n- New Clients: {customers}\n- Conversion Rate: {growth}%\n\nTop Performers:\n1. Product A - €{revenue2:,}\n2. Product B - €{revenue3:,}\n3. Product C - €{revenue4:,}",
                "Financial Analysis Report\n\nPeriod: {month} {year}\nAnalyst: {user}\n\nBudget vs Actual:\n- Budget: €{revenue:,}\n- Actual: €{revenue2:,}\n- Variance: {growth}%\n\nExpense Categories:\n- Personnel: 60%\n- Operations: 25%\n- Marketing: 15%"
            ],
            "emails": [
                "Subject: {subject}\nFrom: {sender}@company.com\nTo: {recipient}@company.com\nDate: {date}\n\nHi {recipient_name},\n\n{body}\n\nBest regards,\n{sender_name}",
                "Subject: Urgent: {subject}\nFrom: {sender}@company.com\nTo: {recipient}@company.com\nCC: manager@company.com\nDate: {date}\n\nDear {recipient_name},\n\nThis is regarding {body}\n\nPlease respond by end of day.\n\nThanks,\n{sender_name}"
            ],
            "contracts": [
                "SERVICE AGREEMENT\n\nContract No: {contract_no}\nDate: {date}\nClient: {client}\nService Provider: {company}\n\nScope of Work:\n{scope}\n\nTerms:\n- Duration: {duration} months\n- Payment: €{amount:,}\n- Start Date: {start_date}\n\nSignatures:\nClient: ________________\nProvider: ________________",
                "EMPLOYMENT CONTRACT\n\nEmployee: {employee}\nPosition: {position}\nDepartment: {dept}\nStart Date: {date}\n\nSalary: €{salary:,} per year\nBenefits:\n- Health insurance\n- Vacation days: 25\n- Pension contribution: 8%\n\nTerms and Conditions:\n{terms}"
            ]
        }
        
        # Comprehensive file extension mapping for realistic file types
        self.file_extensions = {
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
        
        # Realistic filename patterns for different categories
        self.filename_patterns = {
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

    def ensure_target_exists(self):
        """
        Verify that the target drive exists and is accessible.
        
        Raises:
            ValueError: If target drive doesn't exist
            PermissionError: If no write permission to target drive
        """
        if not self.target_drive.exists():
            raise ValueError(f"Target drive {self.target_drive} does not exist")
        
        if not os.access(self.target_drive, os.W_OK):
            raise PermissionError(f"No write permission for {self.target_drive}")
        
        logger.info(f"Target drive validated: {self.target_drive}")

    def create_comprehensive_folder_structure(self):
        """
        Create a comprehensive and realistic Windows-like folder structure.
        
        This method creates:
        - Main system directories (Users, Program Files, Windows, etc.)
        - User profile directories with subdirectories
        - Department-specific shared folders
        - Project directories with organized structure
        """
        logger.info("Creating comprehensive folder structure...")
        
        # Main system directories
        main_folders = [
            "Users", "Program Files", "Program Files (x86)", "Windows",
            "Documents and Settings", "Temp", "Downloads", "Backup",
            "Projects", "Archive", "Shared", "Public"
        ]
        
        for folder in main_folders:
            folder_path = self.target_drive / folder
            folder_path.mkdir(exist_ok=True)
        
        # Comprehensive user directories - multiple realistic users
        users_path = self.target_drive / "Users"
        for user in self.user_names:
            user_path = users_path / user
            user_path.mkdir(exist_ok=True)
            
            # Comprehensive subdirectories for each user profile
            user_folders = [
                "Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music",
                "AppData/Local", "AppData/Roaming", "AppData/LocalLow",
                "Documents/Work", "Documents/Personal", "Documents/Projects",
                "Documents/Archive", "Documents/Templates", "Documents/Drafts",
                "Pictures/Vacation", "Pictures/Family", "Pictures/Work",
                "Pictures/Screenshots", "Pictures/Wallpapers",
                "Downloads/Software", "Downloads/Documents", "Downloads/Media",
                "Desktop/Shortcuts", "Desktop/Projects", "Desktop/Temp"
            ]
            
            for subfolder in user_folders:
                (user_path / subfolder).mkdir(parents=True, exist_ok=True)
        
        # Extensive Program Files structure with realistic applications
        programs = [
            "Microsoft Office/Office16", "Microsoft Office/Templates", "Microsoft Office/Add-ins",
            "Adobe/Acrobat DC", "Adobe/Photoshop", "Adobe/Illustrator",
            "Google/Chrome", "Google/Drive", "Mozilla Firefox", "Mozilla Thunderbird",
            "VLC Media Player", "7-Zip", "WinRAR", "Notepad++", "Visual Studio Code",
            "TeamViewer", "Skype", "Zoom", "Slack", "Discord",
            "Antivirus/McAfee", "Antivirus/Norton", "Backup/Acronis",
            f"{self.company_name}/Internal_Tools", f"{self.company_name}/Database",
            f"{self.company_name}/CRM", f"{self.company_name}/ERP"
        ]
        
        for program in programs:
            (self.target_drive / "Program Files" / program).mkdir(parents=True, exist_ok=True)
        
        # Department-specific shared directories
        for dept in self.departments:
            dept_path = self.target_drive / "Shared" / dept
            dept_path.mkdir(parents=True, exist_ok=True)
            
            # Subdirectories for each department
            dept_folders = ["Projects", "Reports", "Meetings", "Archive", "Templates", "Budget"]
            for folder in dept_folders:
                (dept_path / folder).mkdir(exist_ok=True)
        
        # Project directories with organized structure
        projects_path = self.target_drive / "Projects"
        project_names = [
            "Project_Alpha", "Project_Beta", "Project_Gamma", "Website_Redesign",
            "Mobile_App", "Database_Migration", "Security_Audit", "Cloud_Migration",
            "AI_Initiative", "Digital_Transformation"
        ]
        
        for project in project_names:
            project_path = projects_path / project
            project_folders = ["Documents", "Code", "Tests", "Meetings", "Archive"]
            for folder in project_folders:
                (project_path / folder).mkdir(parents=True, exist_ok=True)

    def generate_realistic_content(self, template_type: str, **kwargs) -> str:
        """
        Generate realistic document content based on predefined templates.
        
        Args:
            template_type (str): Type of document template to use
            **kwargs: Additional variables for template substitution
            
        Returns:
            str: Generated document content with realistic data
        """
        if template_type not in self.document_templates:
            return f"Sample content for {template_type}\nGenerated on: {datetime.now()}"
        
        template = random.choice(self.document_templates[template_type])
        
        # Fill template variables with realistic data
        variables = {
            "date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "user": random.choice(self.user_names),
            "dept": random.choice(self.departments),
            "quarter": random.randint(1, 4),
            "year": random.randint(2022, 2024),
            "month": random.choice(["January", "February", "March", "April", "May", "June"]),
            "revenue": random.randint(50000, 500000),
            "revenue2": random.randint(30000, 200000),
            "revenue3": random.randint(20000, 150000),
            "revenue4": random.randint(10000, 100000),
            "customers": random.randint(50, 1000),
            "growth": random.randint(-10, 25),
            "attendees": ", ".join(random.sample(self.user_names, random.randint(3, 8))),
            "trend": random.choice(["strong", "moderate", "weak", "excellent"]),
            "client": f"Client_{random.randint(1000, 9999)}",
            "contract_no": f"CNT-{random.randint(10000, 99999)}",
            "company": self.company_name
        }
        
        variables.update(kwargs)
        
        try:
            return template.format(**variables)
        except KeyError:
            return template

    def create_extensive_document_collection(self):
        """
        Create thousands of realistic documents across user directories.
        
        This method generates:
        - 50-100 documents per user in main Documents folder
        - 30-60 work-related documents in Work subfolder
        - 20-40 personal documents in Personal subfolder
        - 20-30 desktop files per user
        
        All documents contain realistic content based on templates.
        """
        logger.info("Creating extensive document collection...")
        
        users_path = self.target_drive / "Users"
        
        # Generate documents for each user profile
        for user_idx, user in enumerate(self.user_names):
            logger.info(f"Creating documents for user {user_idx + 1}/{len(self.user_names)}: {user}")
            
            user_path = users_path / user
            
            # Main Documents folder - 50-100 files per user
            documents_path = user_path / "Documents"
            for i in range(random.randint(50, 100)):
                doc_type = random.choice(list(self.document_templates.keys()))
                extension = random.choice(self.file_extensions["documents"])
                
                filename = f"Document_{i+1:03d}_{doc_type}{extension}"
                content = self.generate_realistic_content(doc_type)
                
                self.create_file_with_content(documents_path / filename, content)
            
            # Work subdirectory - additional work-related documents
            work_path = user_path / "Documents" / "Work"
            for i in range(random.randint(30, 60)):
                filename = f"Work_Document_{i+1:03d}.{random.choice(['docx', 'pdf', 'txt'])}"
                content = self.generate_realistic_content("reports", user=user)
                self.create_file_with_content(work_path / filename, content)
            
            # Personal subdirectory - personal documents
            personal_path = user_path / "Documents" / "Personal"
            for i in range(random.randint(20, 40)):
                filename = f"Personal_{i+1:03d}.{random.choice(['txt', 'docx'])}"
                content = f"Personal document for {user}\nCreated: {datetime.now()}\nContent: Personal notes and information."
                self.create_file_with_content(personal_path / filename, content)
            
            # Desktop files - 20-30 files per user
            desktop_path = user_path / "Desktop"
            for i in range(random.randint(20, 30)):
                extension = random.choice([".txt", ".docx", ".pdf", ".lnk"])
                filename = f"Desktop_File_{i+1:02d}{extension}"
                content = f"Desktop file for {user}\nFile number: {i+1}\nCreated: {datetime.now()}"
                self.create_file_with_content(desktop_path / filename, content)

    def create_file_with_content(self, filepath: Path, content: str):
        """
        Create a file with specified content and realistic timestamp.
        
        Args:
            filepath (Path): Path where the file should be created
            content (str): Content to write to the file
            
        The method also sets a random timestamp within the past year
        to make the file system appear more realistic.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Set realistic timestamp within the past year
            random_time = datetime.now() - timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            timestamp = random_time.timestamp()
            os.utime(filepath, (timestamp, timestamp))
            
        except Exception as e:
            logger.error(f"Failed to create file {filepath}: {e}")

    def download_extensive_images(self):
        """
        Download extensive image collections for user profiles.
        
        This method downloads:
        - 5-10 images per user in main Pictures folder
        - 3-8 vacation photos in Vacation subfolder
        - 2-6 family photos in Family subfolder
        
        Images are downloaded from Lorem Picsum for realistic variety.
        Limited to first 10 users for performance optimization.
        """
        logger.info("Downloading extensive image collection...")
        
        users_path = self.target_drive / "Users"
        
        for user_idx, user in enumerate(self.user_names[:10]):  # Limited to 10 users for performance
            logger.info(f"Downloading images for user {user_idx + 1}/10: {user}")
            
            pictures_path = users_path / user / "Pictures"
            
            # Main Pictures directory - 5-10 images
            for i in range(random.randint(5, 10)):
                img_url = random.choice(self.sample_images)
                img_filename = f"photo_{i+1:03d}.jpg"
                
                if self.download_image(img_url, pictures_path / img_filename):
                    time.sleep(0.5)  # Brief pause between downloads
            
            # Vacation subdirectory
            vacation_path = pictures_path / "Vacation"
            for i in range(random.randint(3, 8)):
                img_url = random.choice(self.sample_images)
                img_filename = f"vacation_{i+1:02d}.jpg"
                
                if self.download_image(img_url, vacation_path / img_filename):
                    time.sleep(0.5)  # Rate limiting for server courtesy
            
            # Family subdirectory
            family_path = pictures_path / "Family"
            for i in range(random.randint(2, 6)):
                img_url = random.choice(self.sample_images)
                img_filename = f"family_{i+1:02d}.jpg"
                
                if self.download_image(img_url, family_path / img_filename):
                    time.sleep(0.5)

    def download_image(self, url: str, filepath: Path) -> bool:
        """
        Download an image from a URL to the specified filepath.
        
        Args:
            url (str): URL of the image to download
            filepath (Path): Local path where image should be saved
            
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            return False

    def create_department_files(self):
        """
        Create realistic files for all corporate departments.
        
        This method generates:
        - 20-40 reports per department
        - 15-30 meeting notes per department
        - 10-20 project files per department
        
        All files contain department-specific realistic content.
        """
        logger.info("Creating department-specific files...")
        
        shared_path = self.target_drive / "Shared"
        
        for dept in self.departments:
            logger.info(f"Creating files for department: {dept}")
            dept_path = shared_path / dept
            
            # Reports directory - 20-40 reports per department
            reports_path = dept_path / "Reports"
            for i in range(random.randint(20, 40)):
                filename = f"{dept}_Report_{i+1:03d}.{random.choice(['docx', 'pdf', 'xlsx'])}"
                content = self.generate_realistic_content("reports", dept=dept)
                self.create_file_with_content(reports_path / filename, content)
            
            # Meetings directory - 15-30 meeting notes
            meetings_path = dept_path / "Meetings"
            for i in range(random.randint(15, 30)):
                filename = f"{dept}_Meeting_{i+1:03d}.txt"
                content = self.generate_realistic_content("meeting_notes", dept=dept)
                self.create_file_with_content(meetings_path / filename, content)
            
            # Projects directory - 10-20 project files
            projects_path = dept_path / "Projects"
            for i in range(random.randint(10, 20)):
                filename = f"{dept}_Project_{i+1:02d}.{random.choice(['docx', 'pdf'])}"
                content = f"Project documentation for {dept}\nProject ID: {dept}-{i+1:03d}\nStatus: In Progress"
                self.create_file_with_content(projects_path / filename, content)

    def create_extensive_system_files(self):
        """
        Create extensive system files and logs for realistic forensic analysis.
        
        This method generates:
        - Multiple log files for different system components
        - 100-200 temporary files with realistic names
        - Cache files from various applications
        
        All files include realistic timestamps and content.
        """
        logger.info("Creating extensive system files and logs...")
        
        # Windows logs - comprehensive log collection
        logs_path = self.target_drive / "Windows" / "Logs"
        logs_path.mkdir(parents=True, exist_ok=True)
        
        log_types = [
            "system", "application", "security", "setup", "hardware", 
            "network", "performance", "error", "warning", "information"
        ]
        
        for log_type in log_types:
            for i in range(random.randint(5, 15)):
                log_filename = f"{log_type}_{i+1:02d}.log"
                log_content = self.generate_massive_log_content(log_type)
                self.create_file_with_content(logs_path / log_filename, log_content)
        
        # Temporary files - extensive temp file collection
        temp_path = self.target_drive / "Temp"
        for i in range(random.randint(100, 200)):
            temp_filename = f"tmp_{random.randint(10000, 99999)}.tmp"
            temp_content = f"Temporary file {i}\nCreated: {datetime.now()}\nSize: {random.randint(1024, 1048576)} bytes"
            self.create_file_with_content(temp_path / temp_filename, temp_content)
        
        # Application cache files
        cache_path = self.target_drive / "Windows" / "Temp" / "Cache"
        cache_path.mkdir(parents=True, exist_ok=True)
        
        for i in range(random.randint(50, 100)):
            cache_filename = f"cache_{random.randint(100000, 999999)}.dat"
            cache_content = f"Cache data {i}\nApplication: {random.choice(['Chrome', 'Firefox', 'Office', 'System'])}"
            self.create_file_with_content(cache_path / cache_filename, cache_content)

    def generate_extensive_log_content(self, log_type: str) -> str:
        """
        Generate extensive log content with realistic entries.
        
        Args:
            log_type (str): Type of log to generate (system, application, etc.)
            
        Returns:
            str: Generated log content with 200-1000 realistic entries
        """
        log_entries = []
        start_date = datetime.now() - timedelta(days=90)
        
        for i in range(random.randint(200, 1000)):
            timestamp = start_date + timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            
            log_levels = ["INFO", "WARNING", "ERROR", "DEBUG", "TRACE"]
            log_level = random.choice(log_levels)
            
            messages = {
                "system": ["System startup completed", "Service started", "Driver loaded", "Hardware detected"],
                "application": ["Application launched", "User login", "File opened", "Process terminated"],
                "security": ["Login attempt", "Permission granted", "Access denied", "Policy applied"],
                "network": ["Connection established", "Packet received", "Timeout occurred", "DNS resolved"],
                "error": ["File not found", "Access violation", "Memory error", "Disk full"]
            }
            
            message_list = messages.get(log_type, ["Generic log message", "System event", "Process completed"])
            message = random.choice(message_list)
            
            log_entry = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} [{log_level}] {log_type.upper()}: {message} (PID: {random.randint(1000, 9999)})"
            log_entries.append(log_entry)
        
        return "\n".join(log_entries)

    def create_extensive_deleted_files_simulation(self):
        """
        Create extensive deleted files simulation for forensic recovery practice.
        
        This method creates and immediately deletes files in categories:
        - Confidential documents (salary info, financial data, etc.)
        - Personal files (photos, emails, banking info, etc.)
        - System files (backups, registry, password cache, etc.)
        - Project files (source code, databases, API keys, etc.)
        
        Files are created with realistic content then deleted to simulate
        real-world forensic recovery scenarios.
        """
        logger.info("Creating extensive deleted files simulation...")
        
        # Create temporary files that will be "deleted" for forensic recovery
        temp_folder = self.target_drive / "temp_deleted_mega"
        temp_folder.mkdir(exist_ok=True)
        
        deleted_categories = {
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
        
        for category, files in deleted_categories.items():
            category_folder = temp_folder / category
            category_folder.mkdir(exist_ok=True)
            
            for filename in files:
                filepath = category_folder / filename
                content = f"DELETED FILE - {category.upper()}\nOriginal name: {filename}\nCategory: {category}\nDeleted: {datetime.now()}\nReason: {random.choice(['User deleted', 'System cleanup', 'Security policy', 'Disk cleanup'])}\n\nThis file contained sensitive information and was deleted for security reasons."
                
                # Create the file with realistic content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Brief wait then delete for forensic simulation
                time.sleep(0.1)
                os.remove(filepath)
            
            # Remove the category directory
            category_folder.rmdir()
        
        # Remove the main temporary directory
        temp_folder.rmdir()
        
        logger.info("Deleted files simulation completed - files created and removed for forensic recovery practice")

    def create_archive_files(self):
        """
        Create various types of archive files for realistic file system simulation.
        
        This method creates 10-20 ZIP files containing multiple dummy files
        to simulate backup archives and compressed data.
        """
        logger.info("Creating realistic archive files...")
        
        archive_path = self.target_drive / "Archive"
        
        # Create various ZIP archive files
        for i in range(random.randint(10, 20)):
            zip_name = f"backup_{datetime.now().year}_{i+1:02d}.zip"
            zip_path = archive_path / zip_name
            
            # Create ZIP file with realistic dummy content
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for j in range(random.randint(5, 15)):
                    file_content = f"Archive file {j+1}\nBackup date: {datetime.now()}\nFile size: {random.randint(1024, 10240)} bytes"
                    zipf.writestr(f"file_{j+1:02d}.txt", file_content)

    def run(self):
        """
        Execute the complete forensic disk population process.
        
        This method orchestrates the entire disk population workflow:
        1. Create comprehensive folder structure
        2. Generate extensive document collections
        3. Download realistic image collections
        4. Create department-specific files
        5. Generate system files and logs
        6. Create archive files
        7. Simulate deleted files for recovery practice
        
        The process creates thousands of files across multiple categories
        for comprehensive forensic training scenarios.
        """
        logger.info(f"Starting comprehensive disk population on {self.target_drive}")
        logger.info("This will create THOUSANDS of files - please be patient!")
        
        try:
            # Step 1: Create comprehensive folder structure
            self.create_comprehensive_folder_structure()
            
            # Step 2: Generate extensive document collections (longest step)
            self.create_extensive_document_collection()
            
            # Step 3: Download realistic images (limited for performance)
            self.download_extensive_images()
            
            # Step 4: Create department-specific files
            self.create_department_files()
            
            # Step 5: Generate system files and logs
            self.create_extensive_system_files()
            
            # Step 6: Create realistic archive files
            self.create_archive_files()
            
            # Step 7: Simulate deleted files for recovery practice
            self.create_extensive_deleted_files_simulation()
            
            logger.info("Comprehensive disk population completed successfully!")
            logger.info("Statistics:")
            logger.info(f"- Users created: {len(self.user_names)}")
            logger.info(f"- Departments: {len(self.departments)}")
            logger.info("- Estimated files created: 5,000-10,000+")
            logger.info("- Document types: TXT, DOCX, PDF, XLSX, and more")
            logger.info("- Images downloaded: 100-200")
            logger.info("- System files: 500-1000")
            logger.info("- Archive files: 10-20")
            logger.info("- Deleted files simulated: 24")
            
        except Exception as e:
            logger.error(f"Error during comprehensive disk population: {e}")
            raise


def main():
    if len(sys.argv) != 2:
        print("Usage: python mega_disk_populator.py <target_drive>")
        print("Example: python mega_disk_populator.py D:\\")
        print("\nWARNING: This script will create THOUSANDS of files!")
        print("Requirements:")
        print("- Minimum 2GB free disk space")
        print("- Write permissions to target drive")
        print("- Internet connection for image downloads")
        sys.exit(1)
    
    target_drive = sys.argv[1]
    
    print("🚀 FORENSIC DISK POPULATOR - ADVANCED EDITION")
    print("=" * 60)
    print("This script creates thousands of realistic files for forensic training!")
    print(f"Target drive: {target_drive}")
    print("Estimated time: 5-15 minutes")
    print("Estimated space needed: 1-3 GB")
    print("Files generated: 5,000-10,000+")
    print("=" * 60)
    
    confirm = input("Continue? (y/N): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    try:
        populator = ForensicDiskPopulator(target_drive)
        populator.run()
        
        print("\n🎉 SUCCESS!")
        print("Your comprehensive forensic training disk is ready!")
        print("\nRecommended forensic tools for analysis:")
        print("- Autopsy (Open source digital forensics platform)")
        print("- FTK Imager (Forensic imaging tool)")
        print("- Sleuth Kit (Command-line forensic tools)")
        print("- Volatility (Memory forensics framework)")
        print("\nHappy forensic analysis! 🔍")
        
    except Exception as e:
        logger.error(f"Failed to populate disk: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
