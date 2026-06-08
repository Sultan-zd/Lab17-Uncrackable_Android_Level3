# ✅ Checklist de clôture — Lab 17

> **Lab** : Cracker OWASP UnCrackable Android Level 3
> **Date** : 2026-06-08
> **Analyste** : Étudiant Sécurité

---

## Phase 1 — Préparation

- [x] APK `UnCrackable-Level3.apk` téléchargée depuis le dépôt OWASP officiel
- [x] APK installée sur l'émulateur (`adb install`)
- [x] Émulateur ARM64 / x86_64 API 30+ configuré dans Android Studio
- [x] Outils installés : Ghidra, Jadx-GUI, apktool, Python 3, ADB

## Phase 2 — Analyse statique (Jadx-GUI)

- [x] Code Java décompilé lu dans Jadx-GUI
- [x] `MainActivity.onCreate()` analysé — root check + tampered check identifiés
- [x] `verifyLibs()` identifié — vérification CRC via fonction native `baz`
- [x] `System.loadLibrary("foo")` localisé — librairie native `libfoo.so`
- [x] `CodeCheck.check_code()` identifié — délégation native

## Phase 3 — Patch smali (anti-root / anti-tampering)

- [x] APK décompilée avec `apktool d`
- [x] `MainActivity.smali` ouvert et analysé
- [x] Bloc `showDialog("Rooting or tampering detected.")` localisé
- [x] Patch appliqué : `return-void` remplace l'appel `showDialog`
- [x] (Optionnel) Méthode `showDialog` neutralisée complètement
- [x] APK recompilée avec `apktool b`
- [x] APK signée avec `apksigner`
- [x] APK installée et testée — pas de popup root/tampering

## Phase 4 — Patch natif (anti-debug / anti-Frida)

- [x] `libfoo.so` importée dans Ghidra
- [x] Fonction `sub_73D0` localisée dans `.init_array`
- [x] Anti-Frida identifié (`/proc/self/maps` → "frida"/"exposed")
- [x] Anti-debug identifié (`ptrace`)
- [x] Patch appliqué : première instruction → `RET`
- [x] Librairie exportée et replacée dans le dossier `lib/`
- [x] APK reconstruite, signée, installée

## Phase 5 — Analyse logique native (Ghidra)

- [x] `Java_sg_vantagepoint_uncrackable3_Check_check_code` localisé
- [x] `FUN_001012c0` analysée — obfuscation identifiée
- [x] Code parasite identifié : LCG (0x41c64e6d + 0x3039), malloc, liste chaînée
- [x] 3 qwords finaux relevés (clé encodée, 24 octets)
- [x] Byte Viewer confirmé : little-endian
- [x] Buffer `param_1` suivi via Find References

## Phase 6 — Décodage et validation

- [x] Script Python `decode_key.py` exécuté
- [x] Clé XOR : `pizzapizzapizzapizzapizza` (24 octets)
- [x] Secret décodé : `making owasp great again`
- [x] Phrase saisie dans l'application → **Success!** ✅

## Phase 7 — Documentation

- [x] Tous les fichiers de documentation créés
- [x] `commands.log` complété
- [x] `analyse_info.txt` renseigné
- [x] `README.md` finalisé
- [x] Questions de réflexion répondues

---

## Signature de clôture

| | |
|---|---|
| **Analyste** | Étudiant Sécurité |
| **Date** | 2026-06-08 |
| **Statut** | ✅ Lab terminé et validé |
| **Secret** | `making owasp great again` |
