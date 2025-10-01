# 🔍 Forensic Disk Populator - Advanced Edition

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive Python tool that creates realistic file systems with thousands of files for digital forensics training and analysis purposes.

## 🎯 Purpose

This tool is designed for:
- **Digital forensics education** and training
- **Cybersecurity research** and testing
- **Forensic tool validation** and benchmarking
- **Academic coursework** in digital forensics
- **Professional training** scenarios

## ✨ Features

### 🏗️ Comprehensive File System Generation
- **Realistic Windows-like directory structure** (Users, Program Files, Windows, etc.)
- **20+ user profiles** with authentic personal and work directories
- **8 corporate departments** with department-specific files
- **Project directories** with organized development structures

### 📄 Extensive Document Creation
- **5,000-10,000+ files** across multiple categories
- **Realistic document templates** for meetings, reports, contracts, emails
- **Multiple file formats**: DOCX, PDF, TXT, XLSX, CSV, and more
- **Authentic timestamps** spanning the past year
- **Department-specific content** for each organizational unit

### 🖼️ Media and Binary Files
- **100-200 downloaded images** from Lorem Picsum
- **Organized photo collections** (vacation, family, work photos)
- **Archive files** (ZIP, RAR simulations)
- **System binaries** and application files

### 🔧 System Artifacts
- **Comprehensive log files** (system, application, security, network)
- **500-1000 system files** (temp files, cache, prefetch simulations)
- **Registry-like files** and configuration data
- **Browser history simulations** (Chrome, Firefox)
- **Email archives** (PST-like files)

### 🗑️ Forensic Recovery Scenarios
- **Deleted files simulation** across multiple categories:
  - Confidential documents (salary info, financial data)
  - Personal files (photos, emails, banking information)
  - System files (backups, registry, password cache)
  - Project files (source code, databases, API keys)

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection (for image downloads)
- 2-3 GB free disk space
- Write permissions to target drive

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/forensic-disk-populator.git
   cd forensic-disk-populator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script:**
   ```bash
   python mega_disk_populator.py <target_drive>
   ```

### Example Usage

```bash
# Populate D: drive (Windows)
python mega_disk_populator.py D:\

# Populate external drive (Windows)
python mega_disk_populator.py E:\

# Populate directory (Linux/Mac)
python mega_disk_populator.py /mnt/forensic-test/
```

## 📊 Generated Content Statistics

| Category | Count | Description |
|----------|-------|-------------|
| **User Profiles** | 20+ | Complete user directories with personal/work files |
| **Documents** | 3,000-5,000 | Realistic business documents, reports, emails |
| **Images** | 100-200 | Downloaded photos in organized collections |
| **System Files** | 500-1,000 | Logs, temp files, cache, system artifacts |
| **Department Files** | 1,000+ | Department-specific reports and documentation |
| **Archive Files** | 10-20 | ZIP archives with realistic content |
| **Deleted Files** | 24 | Simulated deleted files for recovery practice |

## 🔍 Forensic Analysis Opportunities

### File System Analysis
- **File recovery** from deleted file simulations
- **Timeline analysis** using realistic timestamps
- **File signature analysis** across multiple formats
- **Directory structure investigation**

### Content Analysis
- **Document forensics** with realistic business content
- **Email analysis** from simulated PST files
- **Image metadata** examination
- **Archive file investigation**

### System Forensics
- **Log file analysis** across multiple system components
- **Browser history** reconstruction
- **User activity** timeline creation
- **System artifact** correlation

### Advanced Scenarios
- **Corporate investigation** simulations
- **Data breach** response training
- **Insider threat** detection practice
- **Compliance audit** preparation

## 🛠️ Recommended Forensic Tools

### Open Source Tools
- **[Autopsy](https://www.autopsy.com/)** - Comprehensive digital forensics platform
- **[Sleuth Kit](https://www.sleuthkit.org/)** - Command-line forensic analysis tools
- **[Volatility](https://www.volatilityfoundation.org/)** - Memory forensics framework
- **[YARA](https://virustotal.github.io/yara/)** - Pattern matching engine

### Commercial Tools
- **FTK Imager** - Forensic imaging and analysis
- **EnCase** - Enterprise forensic investigation
- **X-Ways Forensics** - Integrated forensic environment
- **Cellebrite UFED** - Mobile forensics platform

### Analysis Techniques
- **Hash analysis** (MD5, SHA-1, SHA-256)
- **Keyword searching** across file contents
- **Regular expression** pattern matching
- **Metadata extraction** and analysis
- **Timeline correlation** across artifacts

## ⚙️ Configuration

### Customizing User Profiles
```python
# Edit the user_names list in the script
self.user_names = [
    "John_Doe", "Sarah_Smith", "Mike_Johnson", 
    # Add your custom users here
]
```

### Modifying Departments
```python
# Customize corporate departments
self.departments = [
    "IT", "HR", "Finance", "Marketing", 
    # Add your departments here
]
```

### Adjusting File Counts
```python
# Modify ranges in document generation methods
for i in range(random.randint(50, 100)):  # Adjust these numbers
```

## 📁 Directory Structure

```
forensic-disk-populator/
├── mega_disk_populator.py    # Main script
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── examples/                # Example configurations
    ├── corporate_config.py  # Corporate environment setup
    └── academic_config.py   # Academic lab setup
```

## 🔒 Security and Legal Considerations

### ⚠️ Important Disclaimers

**This tool is intended for:**
- Educational purposes only
- Authorized forensic training
- Controlled testing environments
- Academic research

**Do NOT use for:**
- Unauthorized system access
- Malicious activities
- Production system testing without permission
- Any illegal purposes

### Best Practices
- Always use on **isolated test systems**
- Obtain proper **authorization** before use
- Follow your organization's **security policies**
- Document all **training activities**
- Respect **privacy and data protection** laws

## 🐛 Troubleshooting

### Common Issues

**Permission Denied Errors:**
```bash
# Run as administrator (Windows)
# Use sudo if necessary (Linux/Mac)
```

**Module Import Errors:**
```bash
pip install --upgrade -r requirements.txt
```

**Insufficient Disk Space:**
- Ensure 2-3 GB free space
- Monitor disk usage during execution
- Consider reducing file generation counts

**Network Issues:**
- Check internet connection for image downloads
- Configure proxy settings if necessary
- Disable firewall temporarily if blocking downloads

### Performance Optimization

**For faster execution:**
- Reduce image download count
- Limit user profile generation
- Use SSD storage for better I/O performance
- Close unnecessary applications

**For larger datasets:**
- Increase file generation ranges
- Add more user profiles
- Extend department structures
- Include additional file types

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/forensic-disk-populator.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black mega_disk_populator.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Lorem Picsum** for providing sample images
- **Digital forensics community** for inspiration and feedback
- **Academic institutions** using this tool for education
- **Open source contributors** making this project better

## 📚 Educational Resources

### Learning Digital Forensics
- **[SANS Digital Forensics](https://www.sans.org/cyber-security-courses/digital-forensics/)** - Professional training
- **[Cybrary](https://www.cybrary.it/)** - Free cybersecurity courses
- **[Digital Forensics Association](https://www.digitalforensicsassociation.org/)** - Professional organization

### Academic Programs
- **Computer Science** with cybersecurity focus
- **Digital Forensics** specialized degrees
- **Cybersecurity** certification programs
- **Information Systems** security tracks

---

**⭐ If this tool helps your forensic training, please give it a star!**

Made with ❤️ for the digital forensics community
