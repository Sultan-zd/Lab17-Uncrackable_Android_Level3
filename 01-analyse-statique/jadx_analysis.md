# 🔍 Étape 1 — Analyse statique avec Jadx-GUI

> **Objectif** : Comprendre la structure Java de l'application avant de passer au code natif.

---

## 1.1 Ouvrir l'APK dans Jadx-GUI

1. Lancer **Jadx-GUI** (`jadx-gui.bat` sur Windows)
2. `File → Open file → UnCrackable-Level3.apk`
3. Naviguer vers : `sg.vantagepoint.uncrackable3 → MainActivity`

> **Note** : Le package est `sg.vantagepoint` (pas `com.owasp`). C'est normal pour ce challenge.

---

## 1.2 Éléments clés identifiés dans MainActivity

### `verifyLibs()`

```java
private void verifyLibs() {
    // Vérifie le CRC des fichiers .so et du DEX
    // Utilise la fonction native baz() pour la comparaison
    // Si le CRC ne correspond pas → tampered = 31337
}
```

**Rôle** : Protection d'intégrité. Si les librairies natives ou le bytecode DEX ont été modifiés, la variable `tampered` est mise à `31337`.

### `onCreate()`

```java
protected void onCreate(Bundle savedInstanceState) {
    verifyLibs();  // Vérifie l'intégrité
    
    // Détection de root
    if (RootDetection.checkRoot1() || 
        RootDetection.checkRoot2() || 
        RootDetection.checkRoot3() ||
        IntegrityCheck.isDebuggable(getApplicationContext()) ||
        tampered != 0) {
        showDialog("Rooting or tampering detected.");
    }
    
    System.loadLibrary("foo");  // Charge libfoo.so
}
```

**Rôle** : Point d'entrée qui vérifie root + intégrité + debug. Si un problème est détecté → popup bloquant → l'app quitte.

### `verify(View view)`

```java
public void verify(View view) {
    String input = ((EditText) findViewById(R.id.edit_text)).getText().toString();
    if (this.check.check_code(input)) {
        // Success!
    }
}
```

**Rôle** : La vérification du mot de passe est déléguée à `check.check_code()` — une méthode **native** dans `libfoo.so`.

### `System.loadLibrary("foo")`

Charge la librairie `libfoo.so` qui contient :
- La logique de vérification du mot de passe
- Les protections anti-debug et anti-Frida
- La clé encodée en XOR

---

## 1.3 Diagramme de flux Java

```
onCreate()
    │
    ├── verifyLibs()
    │       └── baz() [native] → CRC check
    │               └── si mismatch → tampered = 31337
    │
    ├── RootDetection.checkRoot1/2/3()
    │
    ├── IntegrityCheck.isDebuggable()
    │
    ├── if (root || tampered) → showDialog() → EXIT
    │
    └── System.loadLibrary("foo") → libfoo.so chargée
              │
              └── .init_array → sub_73D0 (anti-debug/anti-Frida)
```

---

## 1.4 Classes utilitaires identifiées

| Classe | Méthode | Rôle |
|--------|---------|------|
| `RootDetection` | `checkRoot1()` | Vérifie `su` dans le PATH |
| `RootDetection` | `checkRoot2()` | Vérifie les fichiers root connus |
| `RootDetection` | `checkRoot3()` | Vérifie les propriétés système |
| `IntegrityCheck` | `isDebuggable()` | Vérifie le flag debug de l'APK |
| `CodeCheck` | `check_code()` | **Native** — vérification du secret |
| `MainActivity` | `verifyLibs()` | CRC des .so et DEX via `baz()` |

---

## 1.5 Conclusion de l'analyse statique Java

| Observation | Implication |
|-------------|-------------|
| La vérification du secret est native | Analyse avec Ghidra obligatoire |
| 4 couches de protection Java | Patch smali nécessaire |
| CRC vérifié au démarrage | Le patch de la librairie doit être accompagné d'un patch du CRC check |
| `libfoo.so` chargée dans onCreate | Les protections natives sont actives dès le démarrage |

> ✅ **Validation** : Le code Java décompilé est visible et compris. La prochaine étape est de patcher le code smali pour supprimer les protections Java.
