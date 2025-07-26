# 💀 ChromeNuke

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Security](https://img.shields.io/badge/Security-DoD%205220.22--M-red.svg)]()

![ChromeNukeLogo](https://github.com/LMLK-seal/ChromeNuke/blob/main/ChromeNukeLogo.png?raw=true)

**Military-Grade Chrome Browser Data Destruction Tool**

*Professional-grade secure deletion with DoD 5220.22-M compliance*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-features) • [🛡️ Security](#-security-compliance) • [💻 Screenshots](#-screenshots)

</div>

---

## 🎯 Overview

ChromeNuke is a professional-grade secure deletion tool designed for complete Chrome browser data destruction. Built with military-standard security protocols, it ensures forensic-level data elimination that prevents any possibility of recovery.

### ⚡ Key Highlights

- 🔒 **Military-Grade Security**: DoD 5220.22-M standard compliance
- 🎯 **Complete Destruction**: 3-35 configurable overwrite passes
- 🖥️ **Professional GUI**: Modern CustomTkinter interface
- 🌐 **Cross-Platform**: Windows, macOS, and Linux support
- 📊 **Detailed Analytics**: Comprehensive deletion statistics
- 🔍 **Smart Detection**: Automatic Chrome profile and cache discovery

---

## 🛡️ Security Compliance

<table>
<tr>
<td width="50%">

### 🏛️ Military Standards
- **DoD 5220.22-M** compliant
- **NIST SP 800-88** guidelines
- **NSA/CSS Policy 9-12** standards
- Forensic-level data destruction

</td>
<td width="50%">

### 🔐 Deletion Methods
- **Zero-fill passes** (0x00)
- **One-fill passes** (0xFF)
- **Cryptographic random data**
- **File system synchronization**
- **Directory structure elimination**

</td>
</tr>
</table>

---

## ✨ Features

### 🎛️ Core Functionality
| Feature | Description |
|---------|-------------|
| 🗂️ **Multi-Profile Support** | Detects and manages all Chrome profiles |
| 💾 **Cache Management** | Comprehensive cache directory handling |
| ⚙️ **Process Control** | Safe Chrome process termination |
| 📈 **Real-time Progress** | Live deletion progress with statistics |
| 🎚️ **Configurable Passes** | 3-35 overwrite passes (default: 7) |
| 📝 **Audit Logging** | Detailed operation logs for compliance |

### 🔍 Data Detection
- **Browser History** - Complete browsing records
- **Cookies & Sessions** - Authentication tokens
- **Downloaded Files** - Download history database
- **Cache Files** - Temporary internet files
- **Bookmarks** - Saved bookmark collections
- **Extensions** - Installed browser extensions
- **Stored Passwords** - Saved credential databases
- **Autofill Data** - Form completion data

### 🖥️ User Interface
- **Modern Dark Theme** - Professional appearance
- **Intuitive Controls** - Easy-to-use interface
- **Progress Tracking** - Real-time operation status
- **Error Handling** - Comprehensive error reporting
- **Keyboard Shortcuts** - Power user efficiency
- **Responsive Design** - Scales with window size

---

## 🚀 Quick Start

### 📋 Prerequisites

```bash
# Python 3.8 or higher required
python --version

# Required packages
pip install customtkinter psutil
```

### 💻 Installation

```bash
# Clone the repository
git clone https://github.com/LMLK-seal/ChromeNuke.git
cd ChromeNuke

# Install dependencies
pip install customtkinter psutil

# Run ChromeNuke
python chromenuke.py
```

### ⚡ Quick Usage

1. **🔍 Scan** - Click "Scan Chrome Data" to detect all Chrome installations
2. **⚙️ Configure** - Set deletion passes (3-35, default 7 for DoD compliance)
3. **✅ Select** - Choose specific profiles/caches to destroy
4. **⚠️ Terminate** - Close Chrome processes if running
5. **💀 Execute** - Click "SECURE DELETE" for permanent destruction

---

## 📸 Screenshots

<details>
<summary>🖼️ View Application Screenshots</summary>

### Main Interface
![Main Interface](screenshots/main_interface.png)

</details>

---

## 🛠️ Technical Specifications

### 🏗️ Architecture
```
ChromeNuke/
├── 🔧 Core Engine
│   ├── SecureDeletion class    # DoD 5220.22-M implementation
│   ├── ChromeDataLocator class # Cross-platform data discovery
│   └── ProcessManager class    # Chrome process management
├── 🎨 GUI Framework
│   ├── ChromeDataDestroyer     # Main application window
│   ├── AboutDialog            # Information dialog
│   └── CustomTkinter UI       # Modern interface components
└── 📊 Analytics
    ├── DataAnalyzer class     # Statistics and reporting
    └── Logging system        # Audit trail generation
```

### 🔒 Security Implementation

| Pass Type | Pattern | Purpose |
|-----------|---------|---------|
| **Pass 1** | `0x00` | Zero-fill overwrite |
| **Pass 2** | `0xFF` | One-fill overwrite |
| **Pass 3** | Random | Cryptographically secure random data |
| **Pass N** | Rotating | Continues pattern for additional passes |

### 🌍 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Windows** | ✅ Full | Windows 10/11, all Chrome variants |
| **macOS** | ✅ Full | macOS 10.14+, Intel & Apple Silicon |
| **Linux** | ✅ Full | Ubuntu, Debian, Fedora, Arch |

---

## ⚠️ Important Warnings

<div align="center">

### 🚨 **CRITICAL SECURITY NOTICE** 🚨

**ChromeNuke performs IRREVERSIBLE data destruction. Deleted data cannot be recovered by any means, including professional data recovery services.**

</div>

### 🔴 Before Using ChromeNuke:
- ✅ **Backup Important Data** - Export bookmarks, passwords if needed
- ✅ **Close Chrome Completely** - Ensure all Chrome processes are terminated
- ✅ **Verify Selections** - Double-check which profiles/data to delete
- ✅ **Test Environment** - Try on non-critical data first
- ✅ **Legal Compliance** - Ensure deletion complies with local laws

---

## 📚 Documentation

### 🎯 Use Cases
- **Corporate Security** - Employee device cleanup
- **Privacy Protection** - Personal data elimination
- **Forensic Investigation** - Evidence secure disposal
- **System Maintenance** - Complete browser reset
- **Security Auditing** - Data destruction verification

### 🔧 Configuration Options

```python
# Deletion passes configuration
DELETION_PASSES = {
    'minimum': 3,      # Basic security
    'standard': 7,     # DoD 5220.22-M compliance
    'paranoid': 35     # Maximum security
}

# Supported Chrome variants
CHROME_VARIANTS = [
    'Google Chrome',
    'Chromium',
    'Chrome Beta',
    'Chrome Dev',
    'Chrome Canary'
]
```

### 📋 Command Line Arguments
```bash
python chromenuke.py --help
python chromenuke.py --scan-only          # Scan without GUI
python chromenuke.py --passes 35          # Set custom passes
python chromenuke.py --profile "Profile 1" # Target specific profile
```

---

### 🐛 Bug Reports
- Use the [Issue Tracker](https://github.com/LMLK-seal/ChromeNuke/issues)
- Include system information and logs
- Provide steps to reproduce

---

## 📄 Legal & Compliance

### 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### ⚖️ Disclaimer
- ChromeNuke is provided "as is" without warranty
- Users are responsible for legal compliance in their jurisdiction
- Not liable for data loss or misuse
- Intended for legitimate security and privacy purposes only

### 🏛️ Compliance Standards
- **GDPR** - Right to erasure implementation
- **CCPA** - Consumer data deletion rights
- **HIPAA** - Healthcare data destruction
- **SOX** - Financial record management
- **DoD 5220.22-M** - Classified information handling

---

## 📞 Support & Contact

<div align="center">

### 🆘 Need Help?

[![Issues](https://img.shields.io/badge/🐛-Issues-red)](https://github.com/LMLK-seal/ChromeNuke/issues)
[![Discussions](https://img.shields.io/badge/💬-Discussions-purple)](https://github.com/LMLK-seal/ChromeNuke/discussions)

---

## ⭐ Show Your Support

If ChromeNuke helps secure your data, please:

- ⭐ **Star this repository**
- 🐦 **Share on social media**
- 📝 **Write a review**
- 🤝 **Contribute to the project**

<div align="center">

**Made with for digital security**

</div>
