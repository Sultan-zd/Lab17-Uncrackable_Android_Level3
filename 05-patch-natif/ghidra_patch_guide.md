# 🛡️ Étape 5 — Patch de la librairie native avec Ghidra

> **Objectif** : Désactiver les protections anti-debug et anti-Frida contenues dans `libfoo.so` avant d'analyser la logique de vérification.

---

## 5.1 Importer la librairie dans Ghidra

1. Dans le dossier `uncrackable3/lib/`, allez dans le sous-dossier correspondant à votre architecture (ex: `x86_64` ou `arm64-v8a`).
2. Ouvrez **Ghidra**.
3. `File → New Project → Non-Shared Project → "Uncrackable3"`.
4. `File → Import File...` → Sélectionnez `libfoo.so`.
5. Double-cliquez sur `libfoo.so` dans l'Active Project pour l'ouvrir dans l'outil **CodeBrowser**.
6. Acceptez l'analyse automatique initiale (`Yes` → `Analyze`).

---

## 5.2 Identifier la fonction d'initialisation

Les protections natives s'exécutent souvent avant le point d'entrée principal (JNI), lors du chargement de la librairie (déclenché par `System.loadLibrary("foo")` en Java).

1. Dans la fenêtre **Symbol Tree** (à gauche), développez `Functions`.
2. Cherchez une fonction se nommant `sub_73D0` (ou une fonction proche dans les premières adresses de la section `.text`, souvent référencée par `.init_array`).
3. Double-cliquez dessus.

### Observation du code (`sub_73D0`)

Vous verrez des éléments suspects dans la fenêtre **Decompile** :
- `fopen("/proc/self/maps", "r")`
- `strstr(..., "frida")` ou `strstr(..., "exposed")`
- `ptrace(PTRACE_TRACEME, ...)`
- Appels à `goodbye()` ou `exit()` si les vérifications échouent.

C'est clairement la fonction de protection.

---

## 5.3 Appliquer le patch "RET"

L'objectif est de neutraliser entièrement cette fonction pour qu'elle retourne immédiatement sans exécuter aucune vérification.

1. Dans la vue **Listing** (assembleur), cliquez sur la **première instruction** de la fonction `sub_73D0`.
   - Pour ARM64 : souvent un `STP X29, X30, [SP, ...]`
   - Pour x86_64 : souvent `PUSH RBP`
2. Clic droit → **Patch Instruction** (ou `Ctrl + Shift + G`).
3. Remplacez l'instruction par :
   - **`RET`**
4. Appuyez sur Entrée.

> **Ce que ça fait :** Dès que la fonction est appelée au démarrage de la librairie, elle exécute `RET` (Return) et revient à l'appelant sans faire les vérifications.

---

## 5.4 Exporter la librairie patchée

1. Dans Ghidra, allez dans `File → Export Program...`
2. **Format** : Choisissez **Binary** ou **Original File** (les deux peuvent fonctionner selon la version de Ghidra, privilégiez Binary pour s'assurer que le patch s'applique sur l'octet modifié).
3. Sauvegardez le fichier sous le nom `libfoo_patched.so` (pour ne pas écraser l'original tout de suite).
4. Renommez-le en `libfoo.so` et remplacez l'ancien fichier dans le dossier `uncrackable3/lib/votre_arch/`.

---

## 5.5 Reconstruire et réinstaller

Nous devons appliquer les mêmes commandes qu'à l'étape 4 :

```bash
# 1. Recompiler l'APK
apktool b uncrackable3 -o UnCrackable-Level3-patched.apk

# 2. Signer l'APK
apksigner sign --ks "%USERPROFILE%\.android\debug.keystore" UnCrackable-Level3-patched.apk
# ou sous Linux: apksigner sign --ks ~/.android/debug.keystore UnCrackable-Level3-patched.apk

# 3. Désinstaller et réinstaller
adb uninstall owasp.mstg.uncrackable3
adb install -r UnCrackable-Level3-patched.apk
```

---

## 5.6 Vérification

L'application doit toujours fonctionner normalement. La différence est qu'elle est maintenant vulnérable à l'injection Frida et au débogage gdb, car les mécanismes défensifs natifs ont été désactivés.

> ✅ **Validation** : La librairie native est "désarmée". Nous pouvons maintenant chercher la logique de vérification du secret en toute tranquillité.
