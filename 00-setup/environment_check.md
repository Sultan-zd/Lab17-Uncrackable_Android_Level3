# ⚙️ Vérification de l'environnement — Lab 17

> Vérifier que tous les outils sont installés et opérationnels avant de commencer.

---

## Checklist de l'environnement

### 1. Android Studio et émulateur

```powershell
# Vérifier l'installation d'Android Studio
adb version
# Attendu : Android Debug Bridge version 1.0.41

# Vérifier que l'émulateur est visible
adb devices
# Attendu : emulator-5554   device

# Vérifier l'architecture de l'émulateur
adb shell getprop ro.product.cpu.abi
# Attendu : x86_64 ou arm64-v8a
```

> **Recommandation** : Créer un émulateur **ARM64 API 30+** pour manipuler les registres X0/X9 dans GDB. Si x86_64, adapter les instructions Ghidra en conséquence.

### 2. Ghidra

```powershell
# Lancer Ghidra (pas de CLI — interface graphique)
# Windows : double-clic sur ghidraRun.bat
# Linux : ./ghidraRun
```

- Version minimale : **11.0**
- Vérifier que le plugin ARM/x86 est chargé (automatique)

### 3. Jadx-GUI

```powershell
# Lancer Jadx-GUI
# Windows : double-clic sur jadx-gui.bat
# Linux : ./jadx-gui
```

- Version minimale : **1.4.7**
- Tester en ouvrant un APK quelconque

### 4. apktool

```powershell
apktool --version
# Attendu : 2.9.x ou supérieur

# Test rapide de décompilation
apktool d test.apk -o test_output
```

### 5. Python 3

```powershell
python --version
# Attendu : Python 3.8+

python -c "print(bytes.fromhex('41').decode())"
# Attendu : A
```

### 6. Outils de signature APK

```powershell
# apksigner (dans le SDK Android)
apksigner --version

# Vérifier l'existence du keystore de debug
# Windows :
dir "%USERPROFILE%\.android\debug.keystore"
# Linux :
ls ~/.android/debug.keystore
```

> Si le keystore n'existe pas, Android Studio le crée automatiquement au premier build.

---

## Tableau récapitulatif

| Outil | Version minimale | Commande de vérification | Statut |
|-------|-----------------|--------------------------|--------|
| Android Studio | Latest | `adb version` | ✅ |
| Émulateur AVD | API 30+ | `adb devices` | ✅ |
| Ghidra | 11.0 | GUI → About | ✅ |
| Jadx-GUI | 1.4.7 | GUI → About | ✅ |
| apktool | 2.9.x | `apktool --version` | ✅ |
| Python | 3.8+ | `python --version` | ✅ |
| apksigner | SDK | `apksigner --version` | ✅ |
| ADB | 1.0.41 | `adb version` | ✅ |

---

## Téléchargement de l'APK cible

```bash
# Via wget (Linux / WSL)
wget https://github.com/OWASP/owasp-mstg/raw/master/Crackmes/Android/Level_03/UnCrackable-Level3.apk

# Via PowerShell (Windows)
Invoke-WebRequest -Uri "https://github.com/OWASP/owasp-mstg/raw/master/Crackmes/Android/Level_03/UnCrackable-Level3.apk" -OutFile "UnCrackable-Level3.apk"

# Installation sur l'émulateur
adb install UnCrackable-Level3.apk
```

> À l'ouverture, vous verrez un champ de 24 caractères. L'objectif est de trouver le code secret.
