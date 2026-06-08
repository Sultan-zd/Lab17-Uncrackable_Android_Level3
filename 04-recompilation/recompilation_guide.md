# 🏗️ Étape 4 — Recompilation, signature et installation

> **Objectif** : Reconstruire l'APK à partir des sources modifiées, la signer pour qu'Android l'accepte, et l'installer sur l'émulateur.

---

## 4.1 Reconstruire l'APK (apktool b)

Ouvrir un terminal dans le dossier contenant le répertoire `uncrackable3/` (pas à l'intérieur).

```bash
apktool b uncrackable3 -o UnCrackable-Level3-patched.apk
```

**Résultat attendu :**
```text
I: Using Apktool 2.9.x
I: Checking whether sources has changed...
I: Smaling smali folder into classes.dex...
I: Checking whether resources has changed...
I: Building resources...
I: Building apk file...
I: Copying unknown files/dir...
I: Built apk...
```
*(Si vous avez une erreur `brut.androlib.AndrolibException`, vérifiez vos modifications smali).*

---

## 4.2 Signer l'APK (apksigner)

Android refuse d'installer une application non signée. Nous utilisons la clé de debug standard.

### Sous Windows :

```cmd
apksigner sign --ks "%USERPROFILE%\.android\debug.keystore" UnCrackable-Level3-patched.apk
```

### Sous Linux / WSL / Mac :

```bash
apksigner sign --ks ~/.android/debug.keystore UnCrackable-Level3-patched.apk
```

> **Mot de passe** : Si un mot de passe est demandé, tapez `android`.
> **Note** : Si `apksigner` n'est pas reconnu, ajoutez le chemin des `build-tools` du SDK Android à votre variable d'environnement PATH.

---

## 4.3 Désinstaller l'ancienne version

```bash
# Vérifier la connexion à l'émulateur
adb devices

# Désinstaller l'APK originale
adb uninstall owasp.mstg.uncrackable3
```

**Pourquoi désinstaller ?** Les signatures de l'APK originale (signée par OWASP) et de l'APK patchée (signée par vous) sont différentes. Android empêche la mise à jour d'une application si la signature change.

---

## 4.4 Installer la version patchée

```bash
adb install -r UnCrackable-Level3-patched.apk
```

**Résultat attendu :**
```text
Performing Streamed Install
Success
```

---

## 4.5 Vérification de l'architecture (Important pour la suite)

```bash
adb shell getprop ro.product.cpu.abi
```

**Résultat :** `x86_64` ou `arm64-v8a`.
Mémorisez cette valeur. Elle indique quelle version de `libfoo.so` vous devez patcher à l'étape suivante.

---

## 4.6 Tester l'application

Ouvrez l'application sur l'émulateur.

**Résultat attendu :**
- L'application s'ouvre directement sur l'écran "Enter the secret code".
- Aucun message "Rooting or tampering detected." n'apparaît.
- Vous pouvez interagir avec le champ texte sans que l'application ne se ferme.

> ✅ **Validation** : Le patch Java (smali) fonctionne. Mais l'application possède encore des protections natives (anti-debug, anti-Frida) qui vont bloquer l'analyse avec Ghidra/GDB ou Frida. Prochaine étape : patcher la librairie native.
