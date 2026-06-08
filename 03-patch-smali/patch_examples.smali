# Exemple de patch smali — Bloc avant/après

# ====================================================
# AVANT (code original dans onCreate)
# ====================================================

# :cond_0
# const-string v0, "Rooting or tampering detected."
# invoke-direct {p0, v0}, Lsg/vantagepoint/uncrackable3/MainActivity;->showDialog(Ljava/lang/String;)V
# .line 130
# :cond_1
# new-instance v0, Lsg/vantagepoint/uncrackable3/CodeCheck;

# ====================================================
# APRÈS — Méthode A (return-void)
# ====================================================

# :cond_0
# return-void
# .line 130
# :cond_1
# new-instance v0, Lsg/vantagepoint/uncrackable3/CodeCheck;

# ====================================================
# APRÈS — Méthode B (goto :cond_1)
# ====================================================

# :cond_0
# goto :cond_1
# .line 130
# :cond_1
# new-instance v0, Lsg/vantagepoint/uncrackable3/CodeCheck;

# ====================================================
# BONUS : Neutraliser showDialog()
# ====================================================

# .method private showDialog(Ljava/lang/String;)V
#     .locals 3
#     return-void
# .end method
