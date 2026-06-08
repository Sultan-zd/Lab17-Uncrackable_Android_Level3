# 🔧 Étape 3 — Patch smali : Suppression anti-root / anti-tampering

> **Objectif** : Modifier le bytecode smali pour supprimer les vérifications de root et d'intégrité dans `onCreate()`.

---

## 3.1 Ouvrir le fichier cible

### Chemin exact

```
uncrackable3/smali/sg/vantagepoint/uncrackable3/MainActivity.smali
```

### Méthodes d'ouverture

| Éditeur | Instructions |
|---------|-------------|
| **VS Code** (recommandé) | `File → Open Folder → uncrackable3` → naviguer dans l'explorateur |
| **Notepad++** | `File → Open → chemin complet` |
| **vim/nano** | `vim uncrackable3/smali/sg/vantagepoint/uncrackable3/MainActivity.smali` |

### Vérification

La première ligne du fichier doit être :

```smali
.class public Lsg/vantagepoint/uncrackable3/MainActivity;
```

---

## 3.2 Localiser le bloc à modifier

### Recherche

Appuyer sur `Ctrl + F` → taper `showDialog` → `Entrée`

Vous trouverez **3 résultats** :

| # | Emplacement | Description |
|---|-------------|-------------|
| 1 | Méthode `showDialog` | La méthode complète (popup + exit) |
| 2 | Méthode `onCreate` | **← À PATCHER** — l'appel au popup |
| 3 | Méthode `access$000` | Accesseur synthétique |

---

## 3.3 Le bloc exact à modifier (dans `onCreate`)

Naviguer vers le **2ème résultat** (environ ligne 126) :

```smali
.line 126
invoke-static {}, Lsg/vantagepoint/util/RootDetection;->checkRoot1()Z
move-result v0
if-nez v0, :cond_0

invoke-static {}, Lsg/vantagepoint/util/RootDetection;->checkRoot2()Z
move-result v0
if-nez v0, :cond_0

invoke-static {}, Lsg/vantagepoint/util/RootDetection;->checkRoot3()Z
move-result v0
if-nez v0, :cond_0

invoke-virtual {p0}, Lsg/vantagepoint/uncrackable3/MainActivity;->getApplicationContext()Landroid/content/Context;
move-result-object v0
invoke-static {v0}, Lsg/vantagepoint/util/IntegrityCheck;->isDebuggable(Landroid/content/Context;)Z
move-result v0
if-nez v0, :cond_0

sget v0, Lsg/vantagepoint/uncrackable3/MainActivity;->tampered:I
if-eqz v0, :cond_1

:cond_0
const-string v0, "Rooting or tampering detected."
invoke-direct {p0, v0}, Lsg/vantagepoint/uncrackable3/MainActivity;->showDialog(Ljava/lang/String;)V

.line 130

:cond_1
new-instance v0, Lsg/vantagepoint/uncrackable3/CodeCheck;
```

---

## 3.4 Appliquer le patch

### Méthode A — La plus simple (recommandée)

**Sélectionner ces 2 lignes :**

```smali
const-string v0, "Rooting or tampering detected."
invoke-direct {p0, v0}, Lsg/vantagepoint/uncrackable3/MainActivity;->showDialog(Ljava/lang/String;)V
```

**Remplacer par :**

```smali
return-void
```

**Résultat :**

```smali
:cond_0
return-void

.line 130

:cond_1
new-instance v0, Lsg/vantagepoint/uncrackable3/CodeCheck;
```

### Méthode B — Alternative (plus propre)

Remplacer les mêmes 2 lignes par :

```smali
goto :cond_1
```

**Résultat :**

```smali
:cond_0
goto :cond_1

.line 130

:cond_1
new-instance v0, Lsg/vantagepoint/uncrackable3/CodeCheck;
```

### Comparaison des deux méthodes

| Aspect | Méthode A (`return-void`) | Méthode B (`goto :cond_1`) |
|--------|---------------------------|---------------------------|
| Simplicité | ✅ Très simple | ✅ Simple |
| Effet | Quitte `onCreate` à cet endroit | Saute le message, continue normalement |
| Risque | Le code après `cond_1` ne s'exécute pas | ❌ Aucun |
| Recommandation | Débutants | Plus propre techniquement |

> **Recommandation** : Pour ce challenge, les deux méthodes fonctionnent. Méthode A est la plus rapide.

---

## 3.5 Bonus : Neutraliser la méthode `showDialog`

Naviguer vers le **1er résultat** de la recherche `showDialog` (la définition de la méthode).

**Remplacer le contenu complet de la méthode par :**

```smali
.method private showDialog(Ljava/lang/String;)V
    .locals 3
    return-void
.end method
```

> Cela neutralise complètement la méthode. Même si elle est appelée depuis un autre endroit, elle ne fera rien.

---

## 3.6 Résumé des modifications

```diff
  :cond_0
- const-string v0, "Rooting or tampering detected."
- invoke-direct {p0, v0}, Lsg/vantagepoint/uncrackable3/MainActivity;->showDialog(Ljava/lang/String;)V
+ return-void
  
  .line 130
  
  :cond_1
  new-instance v0, Lsg/vantagepoint/uncrackable3/CodeCheck;
```

---

## 3.7 Sauvegarder

- `Ctrl + S` dans VS Code / Notepad++
- Vérifier que le fichier est bien modifié (date de modification mise à jour)

---

## 3.8 Vérification

- [x] Le fichier `MainActivity.smali` a été modifié
- [x] Les 2 lignes `const-string` + `invoke-direct showDialog` ont été remplacées
- [x] Le fichier est sauvegardé
- [x] Aucune erreur de syntaxe smali (les labels `:cond_0` et `:cond_1` sont cohérents)

> ✅ **Validation** : Le patch smali est appliqué. Prochaine étape : recompiler l'APK.
