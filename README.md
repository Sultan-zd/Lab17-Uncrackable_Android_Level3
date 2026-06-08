# 🔓 Lab 17 — Cracking : OWASP UnCrackable Android Level 3

> **Outils** : Android Studio · Ghidra · Jadx-GUI · apktool | **Cadre** : OWASP MASVS | **Niveau** : Avancé

---

## 📋 Table des matières

- [Avertissement légal](#-avertissement-légal)
- [Description](#-description)
- [Objectifs pédagogiques](#-objectifs-pédagogiques)
- [Prérequis](#-prérequis)
- [Architecture du lab](#-architecture-du-lab)
- [Méthodologie](#-méthodologie)
- [Déroulement des étapes](#-déroulement-des-étapes)
- [Questions de réflexion](#-questions-de-réflexion)
- [Livrables](#-livrables)
- [Résultats clés](#-résultats-clés)
- [Glossaire](#-glossaire)
- [Auteur](#-auteur)

---

## ⚠️ Avertissement légal

> **N'appliquez ce lab que dans un cadre légal (applications vulnérables d'entraînement).**
>
> Les techniques de cracking (décompilation, modification de smali, patching binaire) présentées ici sont à usage **strictement pédagogique** sur l'application open-source "UnCrackable-Level3" d'OWASP. L'application de ces techniques sur des applications de production sans autorisation est illégale.

---

## 📖 Description

Ce lab constitue le troisième et dernier niveau du célèbre challenge Android de l'OWASP. Contrairement aux niveaux précédents, ce challenge combine des protections à la fois au niveau **Java (Dalvik/ART)** et au niveau **Natif (C/C++)**. L'objectif est de trouver le mot de passe secret de 24 caractères en contournant une série de protections défensives robustes.

| Aspect | Détail |
|--------|--------|
| **Cible** | UnCrackable-Level3.apk |
| **Protections Java** | Root detection, vérification d'intégrité (CRC), Anti-debug APK |
| **Protections Natives** | Anti-debug (ptrace), Anti-Frida (maps scan), Obfuscation O-LLVM |
| **Outils** | Jadx-GUI (Java), apktool (Smali), Ghidra (Natif) |
| **Référentiel** | OWASP MASVS v2.0 — MASVS-RESILIENCE |

---

## 🎯 Objectifs pédagogiques

- ✅ **Décompiler et patcher** une APK (code smali) pour supprimer les vérifications de root.
- ✅ **Comprendre l'interaction JNI** (Java Native Interface) entre le DEX et la librairie `.so`.
- ✅ **Analyser une librairie native** avec Ghidra et patcher l'assembleur (`RET` instruction).
- ✅ **Identifier l'obfuscation** de type LCG et contourner le "bruit" pour trouver la logique métier.
- ✅ **Comprendre la représentation mémoire** (Little-Endian) des données chiffrées.
- ✅ **Décoder un chiffrement XOR** via un script Python pour extraire le mot de passe final.

---

## ⚙️ Prérequis

### Environnement

| Composant | Requis |
|-----------|--------|
| 💻 PC | Windows / Linux / macOS |
| 📱 Émulateur | Android Studio AVD (ARM64 API 30+ recommandé) |
| 🔧 Outils CLI | ADB, Python 3 |
| 🛡️ Reversing | Ghidra 11+, Jadx-GUI 1.4+, apktool 2.9+ |

### Installation de l'APK

```bash
wget https://github.com/OWASP/owasp-mstg/raw/master/Crackmes/Android/Level_03/UnCrackable-Level3.apk
adb install UnCrackable-Level3.apk
```

---

## 📁 Architecture du lab

```
Lab17/
├── 📂 00-setup/                            # Configuration et périmètre
│   ├── scope.md                            # Périmètre d'analyse
│   └── environment_check.md                # Vérification de l'environnement
│
├── 📂 01-analyse-statique/                 # Étape 1 — Java
│   └── jadx_analysis.md                    # Analyse avec Jadx-GUI
│
├── 📂 02-decompilation/                    # Étape 2 — Extraction
│   └── apktool_guide.md                    # Décompilation avec apktool
│
├── 📂 03-patch-smali/                      # Étape 3 — Patch Java
│   ├── smali_patch_guide.md                # Guide de modification smali
│   └── patch_examples.smali                # Exemples de blocs avant/après
│
├── 📂 04-recompilation/                    # Étape 4 — Build & Sign
│   └── recompilation_guide.md              # apktool b + apksigner
│
├── 📂 05-patch-natif/                      # Étape 5 — Ghidra
│   └── ghidra_patch_guide.md               # Neutralisation anti-debug/Frida
│
├── 📂 06-analyse-logique/                  # Étape 6 — Reverse Native
│   └── logique_native_guide.md             # Analyse JNI et obfuscation
│
├── 📂 07-decodage/                         # Étape 7 — XOR
│   └── decodage_guide.md                   # Extraction et décodage
│
├── 📂 scripts/                             # Scripts d'automatisation
│   └── decode_key.py                       # Solveur XOR en Python
│
├── analyse_info.txt                        # Métadonnées de traçabilité
├── commands.log                            # Log chronologique des commandes
├── checklist_fin.md                        # Checklist de clôture signée
└── README.md                               # Ce fichier
```

---

## 🔬 Méthodologie

Ce challenge nécessite une approche en **deux phases distinctes** :

1. **Phase Java** : Désamorcer les défenses de l'application (anti-root, anti-tamper) pour l'empêcher de se fermer.
2. **Phase Native** : Désamorcer les défenses anti-debug de la librairie `.so`, puis analyser l'algorithme de chiffrement pour extraire la clé.

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Analyse    │──▶│ Patch Smali │──▶│ Patch Natif │──▶│ Reverse .so │──▶│  Décodage   │
│  Jadx-GUI   │   │  apktool    │   │   Ghidra    │   │  Ghidra     │   │   Python    │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

---

## 📝 Déroulement des étapes

### 1. Analyse Statique Java

Ouverture de l'APK dans **Jadx-GUI**. On constate que `MainActivity.onCreate` effectue des vérifications root et affiche un popup bloquant. La vraie vérification du secret est déléguée à la méthode native `check_code` de `libfoo.so`.
→ [Guide d'analyse](./01-analyse-statique/jadx_analysis.md)

### 2. Patch Smali (Anti-Root)

Décompilation via `apktool d`. Modification du fichier `MainActivity.smali` pour court-circuiter l'appel à `showDialog("Rooting or tampering detected.")` en insérant une instruction `return-void` (ou `goto`).
→ [Guide de patch smali](./03-patch-smali/smali_patch_guide.md)

### 3. Recompilation et Signature

Reconstruction de l'APK patchée via `apktool b`. Signature obligatoire via `apksigner` avec un keystore de debug avant réinstallation via `adb install`.
→ [Guide de recompilation](./04-recompilation/recompilation_guide.md)

### 4. Patch Natif (Anti-Frida / Anti-Debug)

Importation de `libfoo.so` dans **Ghidra**. Identification de la fonction `sub_73D0` (lancée via `.init_array`) qui scanne `/proc/self/maps` (Frida) et utilise `ptrace` (GDB). Neutralisation de la fonction en modifiant sa première instruction par un `RET`.
→ [Guide de patch natif](./05-patch-natif/ghidra_patch_guide.md)

### 5. Extraction du secret

Analyse de la fonction JNI `Java_sg_vantagepoint_uncrackable3_CodeCheck_check_code` (qui pointe vers `FUN_001012c0`). Contournement visuel de l'obfuscation (LCG, mallocs de liste chaînée) pour repérer les 3 variables `undefined8` finales (24 octets). Prise en compte du Little-Endian.
→ [Guide d'analyse logique](./06-analyse-logique/logique_native_guide.md)

### 6. Décodage Python

Écriture d'un script pour appliquer un XOR byte par byte entre les 24 octets encodés (`1d081113...`) et la clé connue (`pizzapizzapizzapizzapizzapizza`).
→ [Script de décodage](./scripts/decode_key.py)

---

## 🧠 Questions de réflexion

**1. Le rôle de `check.check_code()`**
C'est la méthode Java (déclarée native) appelée lors du clic sur le bouton "VERIFY". Elle sert de passerelle JNI pour transmettre l'entrée utilisateur à la librairie native.

**2. Le rôle de `FUN_001012c0`**
C'est la fonction native réelle de vérification. Elle calcule (et obfusque) la clé secrète attendue et la compare octet par octet avec l'entrée utilisateur via une opération XOR.

**3. Les indices d'obfuscation observés**
La fonction contient près d'une centaine de blocs répétitifs effectuant un calcul mathématique (LCG: `x * 0x41c64e6d + 0x3039`) et l'allocation (`malloc`) de structures en liste chaînée qui ne servent à rien dans la logique finale. C'est typique d'outils comme O-LLVM.

**4. Pourquoi le buffer final est la clé du challenge**
Toute la logique parasite d'obfuscation n'affecte pas le flux de données réel. À la fin de la fonction, 24 octets statiques (la clé XOR encodée) sont écrits en mémoire (`param_1`) juste avant la comparaison avec l'entrée utilisateur. Suivre l'écriture mémoire est plus efficace que lire le code.

**5. Avantage de sécurité d'une vérification native**
Le bytecode Java (DEX) se décompile presque parfaitement (Jadx). Le code natif (C/C++ vers ARM) nécessite l'analyse d'assembleur, ce qui relève grandement la complexité du reverse engineering et permet des techniques d'obfuscation puissantes.

**6. Comment améliorer la sécurité ?**
Un développeur défensif pourrait chiffrer la librairie elle-même, obfusquer les chaînes de caractères (ex: "frida"), utiliser un packer commercial (DexGuard/Promon), ou générer la clé XOR dynamiquement via le réseau au lieu de la stocker statiquement.

---

## 📦 Livrables

| # | Fichier | Description | Statut |
|---|---------|-------------|--------|
| 1 | `00-setup/scope.md` | Périmètre d'analyse | ✅ |
| 2 | `01-analyse-statique/jadx_analysis.md` | Analyse Java | ✅ |
| 3 | `03-patch-smali/smali_patch_guide.md` | Modification bytecode smali | ✅ |
| 4 | `04-recompilation/recompilation_guide.md` | Build et signature | ✅ |
| 5 | `05-patch-natif/ghidra_patch_guide.md` | Neutralisation anti-debug natif | ✅ |
| 6 | `06-analyse-logique/logique_native_guide.md` | Reverse obfuscation JNI | ✅ |
| 7 | `scripts/decode_key.py` | Résolveur Python XOR | ✅ |
| 8 | `checklist_fin.md` | Validation de fin de lab | ✅ |
| 9 | `commands.log` | Historique des commandes | ✅ |
| 10 | `README.md` | Ce document | ✅ |

---

## 📊 Résultats clés

- **Mot de passe secret final** : `making owasp great again`
- **Architecture de la cible** : Hybride (Dalvik + ARM Native)
- **Points de patching** : 2 (Smali + Assembly `RET`)
- **Type d'obfuscation** : LCG (Linear Congruential Generator) + Dead Code Insertion

---

## 📖 Glossaire

| Terme | Définition |
|-------|------------|
| **Smali** | Langage d'assemblage lisible par l'homme pour le bytecode Dalvik/ART. |
| **JNI** | Java Native Interface — pont entre le code Java et le code C/C++. |
| **`.init_array`** | Section ELF contenant des pointeurs vers des fonctions exécutées au chargement de la librairie. |
| **Little-Endian** | Format de stockage mémoire où l'octet de poids faible est placé en premier. |
| **LCG** | Algorithme pseudo-aléatoire utilisé ici comme technique d'obfuscation (bruit). |
| **ptrace** | Appel système Linux utilisé par les débogueurs. Une app peut s'attacher à elle-même pour empêcher un débogueur de le faire (anti-debug). |

---

## 👤 Auteur

| | |
|---|---|
| **Analyste** | Étudiant Sécurité |
| **Cours** | Sécurité Mobile — Lab 17 |
| **Date** | 2026-06-08 |
| **Durée** | 4h00 |

---

<div align="center">
<b>⚡ Lab réalisé dans un cadre strictement pédagogique et défensif ⚡</b><br>
<i>OWASP UnCrackable Android Level 3</i>
</div>
