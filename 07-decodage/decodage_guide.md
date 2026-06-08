# 🔓 Étape 7 — Décodage XOR et Validation

> **Objectif** : Écrire un script Python pour appliquer l'opération XOR entre la clé encodée extraite de Ghidra et la clé de chiffrement (dérivée du contexte), puis valider le mot de passe dans l'application.

---

## 7.1 La logique du XOR

L'opération XOR (ou exclusif, symbole `^`) est symétrique :
`A ^ B = C`
`C ^ B = A`

Ici :
- `C` = La clé encodée trouvée dans Ghidra (`1d081113...`)
- `B` = La clé de chiffrement (le pattern répété "pizza" jusqu'à 24 caractères, soit `pizzapizzapizzapizzapizzapizza`)
- `A` = Le secret en clair que nous cherchons.

---

## 7.2 Script Python de décodage

Créez le fichier `scripts/decode_key.py` (ou exécutez directement ce qui suit) :

```python
# === DÉCODAGE DE LA CLÉ ENCODÉE ===

# 1. La clé encodée trouvée dans Ghidra (en Little-Endian, concaténée)
encoded_hex = "1d0811130f1749150d0003195a1d1315080e5a0017081314"
encoded = bytes.fromhex(encoded_hex)

# 2. La clé de XOR (24 octets)
xor_key = b"pizzapizzapizzapizzapizzapizza"

# 3. Opération XOR byte par byte
secret = bytes(a ^ b for a, b in zip(encoded, xor_key))

# 4. Affichage du résultat
print("Clé secrète trouvée :", secret.decode())
```

---

## 7.3 Exécution du script

```bash
python scripts/decode_key.py
```

**Résultat attendu :**
```text
Clé secrète trouvée : making owasp great again
```

---

## 7.4 Validation finale dans l'application

1. Ouvrez l'application patchée (`UnCrackable-Level3-patched.apk`) sur l'émulateur.
2. Saisissez la phrase obtenue : **`making owasp great again`**
3. Cliquez sur **VERIFY**.

**Résultat :** Un popup s'affiche indiquant **"Success!"**.

> 🎉 **Félicitations !** Vous avez déjoué les protections Java, désarmé les mécanismes anti-debug natifs, contourné l'obfuscation et reconstitué la logique cryptographique pour craquer le Level 3 d'UnCrackable.
