# 🎯 Périmètre d'analyse — Lab 17

> **Challenge** : OWASP UnCrackable Level 3
> **Date** : 2026-06-08

---

## Application cible

| Attribut | Valeur |
|----------|--------|
| **Nom** | UnCrackable-Level3 |
| **Package** | `owasp.mstg.uncrackable3` |
| **Source** | [OWASP MSTG — Crackmes](https://github.com/OWASP/owasp-mstg/tree/master/Crackmes/Android/Level_03) |
| **Type** | Challenge de rétro-ingénierie Android (APK) |
| **Licence** | Open-source (Creative Commons) |

## Autorisations

- ✅ L'APK est publiée en open-source par OWASP à des fins éducatives
- ✅ Aucune donnée personnelle n'est traitée
- ✅ L'analyse est réalisée sur un émulateur local contrôlé
- ✅ Aucune infrastructure tierce n'est ciblée

## Objectif du périmètre

Identifier et contourner les protections suivantes :

1. **Détection de root** — `RootDetection.checkRoot1/2/3()`
2. **Vérification d'intégrité** — CRC sur `.so` et DEX via `verifyLibs()` + `baz()`
3. **Anti-debug** — `ptrace` dans `libfoo.so`
4. **Anti-Frida** — Scan de `/proc/self/maps` pour "frida" / "exposed"
5. **Obfuscation native** — LCG + malloc + liste chaînée dans `FUN_001012c0`
6. **Clé XOR encodée** — 24 octets dans la librairie native

## Hors périmètre

- Analyse réseau / interception de trafic
- Fuzzing de l'APK
- Modification du système Android (Magisk, Xposed)
- Exploitation de vulnérabilités non liées au challenge
