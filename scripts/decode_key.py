#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de décodage XOR pour OWASP UnCrackable Level 3
Ce script applique un XOR byte par byte entre les 24 octets encodés extraits de la librairie native
et la clé de chiffrement (pizzapizzapizzapizzapizzapizza) pour obtenir le mot de passe en clair.
"""

def main():
    print("[*] Décodage de la clé pour UnCrackable Level 3...")

    # Données extraites de Ghidra (FUN_001012c0), converties du little-endian
    # 0x1549170f1311081d -> 1d 08 11 13 0f 17 49 15
    # 0x15131d5a1903000d -> 0d 00 03 19 5a 1d 13 15
    # 0x14130817005a0e08 -> 08 0e 5a 00 17 08 13 14
    encoded_hex = "1d0811130f1749150d0003195a1d1315080e5a0017081314"
    encoded_bytes = bytes.fromhex(encoded_hex)

    print(f"[-] Hexadécimal encodé : {encoded_hex}")

    # La clé XOR répétée (24 octets)
    xor_key_str = "pizzapizzapizzapizzapizzapizza"
    xor_key_bytes = xor_key_str.encode('utf-8')
    
    print(f"[-] Clé XOR (24 bytes) : {xor_key_str}")

    if len(encoded_bytes) != len(xor_key_bytes):
        print("[!] Attention : Les longueurs ne correspondent pas!")
        return

    # Opération XOR
    secret_bytes = bytes(a ^ b for a, b in zip(encoded_bytes, xor_key_bytes))
    secret_text = secret_bytes.decode('utf-8')

    print("\n[+] ==========================================")
    print(f"[+] Clé secrète trouvée : {secret_text}")
    print("[+] ==========================================\n")

if __name__ == "__main__":
    main()
