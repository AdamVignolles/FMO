#Fonction de hachage code par Lenny
import hashlib

def hachage_str (chain_charactere:str) :
    """Fonction de hachage transforme un str en un hach en hexadecimal avec la fonction de hachage cryptographique md5"""
    hach = chain_charactere.encode()
    hach = hashlib.md5(hach).hexdigest()
    return hach
assert(hachage_str ("569test987") == "3828e46a93f546328caebc43a105a496")