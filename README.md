# Project Setup Guide

## 🎯 Project Objective
The objective of this project is to create a Python application that fetches and processes weather data from various APIs, including SIAR, Meteogalicia, Euskalmet, and AEMET. The application will store the fetched data in a structured format for further analysis or use.

## 📁 Project Structure 

The project is organized as follows:
```
tfm_apis_input_data/
├── src/
│   ├── main.py
│   ├── clients/
│   │   ├── aemet_client.py
│   │   ├── base_client.py
│   │   ├── siar_client.py
│   │   ├── meteogalicia_client.py
│   │   └── euskalmet_client.py
│   └── utils/
│                
├── data/
│   └── raw/
│       ├── siar/
│       ├── meteogalicia/
│       └── euskalmet/
├── .env
├── requirements.txt
└── README.md
```
---

## 🔐 Environment Configuration

Before running the project, create a `.env` file in the root directory of your project. You can use the `.env.example` file as a template.

###  Required Environment Variables

Your `.env` file should include the necessary API keys and configuration variables. 
Variables to define include:
```plaintext
API_KEY_SIAR 
API_KEY_METEOGALICIA 
API_KEY_EUSKALMET 
API_KEY_AEMET 
```

Find an example in file .`.env.example`.

---

# ⚙️ Useful Commands
## 🧹 Removing `.idea` Files from Git

To prevent PyCharm’s `.idea` directory from being tracked by Git and pushed to the repository, follow these steps:

### 1. Remove `.idea` from Git Tracking

In the root of your Git repository, run the following commands:

```bash
git rm -r --cached .
git add .
git commit -m "Cleanup: remove ignored files from Git tracking"
```

This removes previously tracked files (including `.idea/`) from Git’s index without deleting them from your local file system.

### 2. Add `.idea` to `.gitignore`

Ensure your `.gitignore` file contains the following line to ignore the `.idea/` directory in the future:

```
.idea/
```

### 3. Commit `.gitignore` Changes

After updating your `.gitignore`, commit the change:

```bash
git add .gitignore
git commit -m "Add .idea to .gitignore"
```

---



