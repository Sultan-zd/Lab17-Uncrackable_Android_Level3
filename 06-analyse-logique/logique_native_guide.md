# 🧠 Étape 6 — Analyse de la logique native (Ghidra)

> **Objectif** : Comprendre comment la librairie vérifie le mot de passe, identifier l'obfuscation et extraire les données chiffrées utiles.

---

## 6.1 Trouver le point d'entrée JNI

1. Retournez dans Ghidra (avec `libfoo.so` ouvert).
2. Dans le **Symbol Tree**, cherchez la fonction appelée depuis Java.
   - D'après l'analyse Java, la méthode était `CodeCheck.check_code()`.
   - La convention de nommage JNI est `Java_package_Classe_methode`.
   - Cherchez : `Java_sg_vantagepoint_uncrackable3_CodeCheck_check_code` (ou approchant, selon le code décompilé).
3. Double-cliquez pour accéder à la fonction.

### Fonction `Java_sg...check_code`
Cette fonction est courte. Elle extrait généralement la chaîne de caractères passée par Java (via `GetStringUTFChars`) et appelle une fonction interne pour faire le vrai travail.
Suivez l'appel vers la fonction principale de vérification, souvent nommée `FUN_001012c0` (ou similaire, selon l'architecture).

---

## 6.2 Analyse de la fonction principale (`FUN_001012c0`)

Double-cliquez sur `FUN_001012c0`.

### Le mur d'obfuscation

Dès l'ouverture, vous êtes confronté à un énorme bloc de code répétitif :
```c
uVar2 = uVar2 * 0x41c64e6d + 0x3039;
puVar3 = (undefined8 *)malloc(0x10);
*puVar3 = 0;
puVar3[1] = 0;
// ... répétition ~90 fois
```

**Analyse :**
- `0x41c64e6d + 0x3039` : C'est un **LCG (Linear Congruential Generator)**, un algorithme pseudo-aléatoire classique.
- `malloc(0x10)` répété des dizaines de fois en construisant des listes chaînées.
- **Conclusion** : C'est de l'**obfuscation** (type O-LLVM ou Tigress). L'auteur a ajouté du code "mort" ou inutile pour noyer le code réel et ralentir le reverse engineer.

### Ignorer le bruit, regarder la fin

Dans les fonctions obfusquées, l'action réelle (initialisation de variables, calcul du secret) se trouve souvent à la toute fin, juste avant le `return`.
Faites défiler le pseudo-code jusqu'aux dernières lignes.

---

## 6.3 Identifier la clé encodée

À la fin de la fonction, vous observez des écritures séquentielles dans un buffer mémoire (souvent le paramètre `param_1`) :

```c
*(undefined8 *)param_1 = 0x1549170f1311081d;
*(undefined8 *)((long)param_1 + 8) = 0x15131d5a1903000d;
*(undefined8 *)((long)param_1 + 0x10) = 0x14130817005a0e08;
```

**Analyse :**
- Trois écritures de `undefined8` (8 octets, un "qword").
- $3 \times 8 = 24$ octets.
- Rappelez-vous l'application : le champ de saisie demande exactement 24 caractères.
- **Conclusion** : C'est la **clé encodée**.

### Extraire les octets (Attention au Little-Endian)

L'architecture (x86_64 / ARM64) utilise le **Little-Endian**. L'octet de poids faible est stocké en premier en mémoire.
La constante affichée `0x1549170f1311081d` s'écrit en mémoire de droite à gauche.

Utilisez le **Byte Viewer** de Ghidra ou inversez manuellement les octets par groupes de 2 :

1. `0x1549170f1311081d` → `1d 08 11 13 0f 17 49 15`
2. `0x15131d5a1903000d` → `0d 00 03 19 5a 1d 13 15`
3. `0x14130817005a0e08` → `08 0e 5a 00 17 08 13 14`

**Chaîne concaténée complète (hexadécimal) :**
`1d0811130f1749150d0003195a1d1315080e5a0017081314`

---

## 6.4 Comprendre la vérification (Le secret complet)

Que fait la librairie avec ce buffer `param_1` ?
Faites un clic droit sur la variable cible de ces écritures → **Find References**.

Vous trouverez une fonction de comparaison :
1. Elle vérifie si la longueur de l'entrée utilisateur est exactement 24 (`iVar1 == 0x18`).
2. Elle initie une boucle avec un pas de 3, ou similaire, comparant l'entrée avec des octets.
3. Ces octets de référence sont calculés dynamiquement par un **XOR** (Souvent représenté par l'opérateur `^`).

Dans le code Java du SDK de l'application originale ou ailleurs (le challenge donne des indices), la clé de XOR est donnée comme étant "pizzapizzapizzapizzapizzapizza" (24 fois 'p' ou répétition de "pizza").
*(Note: Historiquement pour ce challenge, la clé XOR peut être générée en temps réel, ou stockée dans des variables globales comme DAT_00107040, mais la logique est une comparaison XOR bit à bit).*

> ✅ **Validation** : Nous avons la clé encodée en hexadécimal et l'algorithme sous-jacent (XOR). Il ne reste plus qu'à scripter le décodage pour obtenir le mot de passe final.
