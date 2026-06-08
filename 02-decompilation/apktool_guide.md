# 📦 Étape 2 — Décompilation avec apktool

> **Objectif** : Obtenir le code smali modifiable et les librairies natives.

---

## 2.1 Commande de décompilation

```bash
apktool d UnCrackable-Level3.apk -o uncrackable3
```

### Résultat attendu

```
I: Using Apktool 2.9.x
I: Loading resource table...
I: Decoding AndroidManifest.xml...
I: Loading resource table from file...
I: Regular manifest package...
I: Decoding file-resources...
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...
```

---

## 2.2 Structure du dossier décompilé

```
uncrackable3/
├── AndroidManifest.xml              # Manifest de l'application
├── apktool.yml                      # Métadonnées apktool
├── lib/
│   ├── arm64-v8a/
│   │   └── libfoo.so               # Librairie native ARM64
│   ├── armeabi-v7a/
│   │   └── libfoo.so               # Librairie native ARM32
│   ├── x86/
│   │   └── libfoo.so               # Librairie native x86
│   └── x86_64/
│       └── libfoo.so               # Librairie native x86_64
├── original/
├── res/                             # Ressources (layouts, strings, etc.)
├── smali/
│   └── sg/
│       └── vantagepoint/
│           ├── uncrackable3/
│           │   ├── MainActivity.smali        # ← FICHIER CLÉ
│           │   ├── MainActivity$1.smali
│           │   ├── MainActivity$2.smali
│           │   └── CodeCheck.smali
│           └── util/
│               ├── RootDetection.smali
│               └── IntegrityCheck.smali
└── unknown/
```

---

## 2.3 Fichiers importants

| Fichier | Rôle | Action requise |
|---------|------|----------------|
| `smali/.../MainActivity.smali` | Code principal | **Patch** : supprimer root check |
| `lib/x86_64/libfoo.so` | Librairie native | **Patch** : désactiver anti-debug |
| `lib/arm64-v8a/libfoo.so` | Librairie native ARM64 | **Patch** (si émulateur ARM) |
| `AndroidManifest.xml` | Configuration app | Lecture seule |

---

## 2.4 Choix de la librairie native

```bash
# Identifier l'architecture de l'émulateur
adb shell getprop ro.product.cpu.abi
```

| Architecture émulateur | Fichier à patcher |
|------------------------|-------------------|
| `x86_64` | `lib/x86_64/libfoo.so` |
| `arm64-v8a` | `lib/arm64-v8a/libfoo.so` |
| `x86` | `lib/x86/libfoo.so` |
| `armeabi-v7a` | `lib/armeabi-v7a/libfoo.so` |

> **Important** : Patcher la librairie correspondant à l'architecture de votre émulateur.

---

## 2.5 Vérification

- [x] Le dossier `uncrackable3/` est créé avec tous les sous-dossiers
- [x] `MainActivity.smali` est accessible dans `smali/sg/vantagepoint/uncrackable3/`
- [x] La librairie `libfoo.so` correspondant à l'architecture est présente dans `lib/`
- [x] Le fichier `apktool.yml` est présent (métadonnées de recompilation)

> ✅ **Validation** : Le dossier décompilé est prêt. On peut maintenant modifier le code smali.
