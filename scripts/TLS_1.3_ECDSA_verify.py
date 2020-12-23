import hashlib
import sympy
import ecpy
from ecpy.curves import Curve,Point

def sha256(x):
    return hashlib.sha256(bytes.fromhex(x)).hexdigest()

def sha384(x):
    return hashlib.sha384(bytes.fromhex(x)).hexdigest()

if __name__ == "__main__":

    # Exemple amb www.wikipedia.org
    # Es poden extreure les dades de Wireshark. (veure arxius requerits al codi). Encoding: raw binary
    # Per poder llegir payloads de TLS s'ha d'incloure l'output del navegador (sslkeylog en Firefox) a Wireshark

    print("\nComprovar que la clau publica P de www.wikipedia.org es realment un punt de la corba.")
    PK_bytes = open("subjectPublicKey.bin", 'rb').read()
    PK_X = PK_bytes[1:32+1]
    PK_Y = PK_bytes[32+1:64+1]
    print(" # PKey x =", PK_X.hex())
    print(" # PKey y =",PK_Y.hex())
    E = Curve.get_curve('secp256r1')
    G=Point(Gx, Gy, E)
    W=Point(int.from_bytes(PK_X, "big"), int.from_bytes(PK_Y, "big"), E)
    print(" # Comprovacio is_on_curve(G) =",  E.is_on_curve(G))

    print("\nCalcular l’ordre del punt P.")
    print(" # L'ordre del Punt de la clau publica de la Wikipedia és propiament l'ordre de la curva.")
    ordre_W = n
    print(" # Comprovacio ordre(Wiki) * Wiki == inf (El punt de l'infinit):", str(ordre_W * W ) == "inf")

    print("\nComprovar que la signatura ECDSA es correcta.")
    space_64 = 64 * '20'
    fixed_string = bytes('TLS 1.3, server CertificateVerify', 'ascii').hex()
    separador = '00'
    handshake_ClientHello = open("handshakeProtocol_ClientHello.bin", 'rb').read().hex()
    handshake_ServerHello = open("handshakeProtocol_ServerHello.bin", 'rb').read().hex()
    handshake_EncryptedExtensions = open("handshakeProtocol_EncryptedExtensions.bin", 'rb').read().hex()
    handshake_Certificate = open("handshakeProtocol_Certificate.bin", 'rb').read().hex()
    data_hex = handshake_ClientHello + handshake_ServerHello + handshake_EncryptedExtensions + handshake_Certificate
    data_digested = sha384(data_hex)
    to_hash = space_64 + fixed_string + separador + data_digested
    h_hex = sha256(to_hash)
    h = int(h_hex, 16)
    signature = open("signature.bin", 'rb').read()
    f1 = int.from_bytes(signature[4:37], "big")
    f2 = int.from_bytes(signature[39:71], "big")
    # aux = pow(f2, -1, n) # <-- Requires python 3.8 or later.
    aux = sympy.mod_inverse(f2, n)
    W1 = (h*aux)%n
    W2 = (f1*aux)%n
    subZero = W1*G + W2*W
    print('La firma és correcta (x0 mod q = f1) =', subZero.x % n == f1)