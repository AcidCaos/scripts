
## fer el CA

# generar SK pel nou CA i request de certificat pel CA (per auto-firmarse)
openssl req -new -extensions v3_ca -keyout ssl.key/ca_key.pem -out ssl.csr/ca_cert-req.pem
# (entrar dades CA)

# parsejar la request de certificat per veure què hi ha. (hi ha la PK del CA)
openssl asn1parse -i -dump -in ssl.csr/ca_cert-req.pem > ssl.csr/ca_cert-req.txt

# Ara el CA ha de autofirmar-se la request amb la seva SK. Generar self-signed certificat:
openssl req -new -x509 -in ssl.csr/ca_cert-req.pem -out ssl.crt/ca_cert.crt -days 365 -key ssl.key/ca_key.pem
# (entrar dades CA)

# parsejar el certificat (autogenerat)
openssl asn1parse -i dump -in ssl.crt/ca_cert.crt > ssl.crt/ca_cert.txt

## Server

# fer el certificate request pel server. També genera la clau privada SK
openssl req -new -extensions v3_req -keyout ssl.key/server_key.pem -out ssl.csr/server_cert-req.pem
# (entrar dades Server)

# mirar si la request està ben feta
openssl req -in ssl.csr/server_cert-req.pem -text -verify

# 1.4.4 signar certificat del Server amb la clau SK del CA
openssl x509 -req -in ssl.csr/server_cert-req.pem -out ssl.crt/server_cert.crt -days 365 -CA ssl.crt/ca_cert.crt -CAkey ssl.key/ca_key.pem -CAcreateserial

# parsejar el certificat del server:
openssl asn1parse -i -dump -in ssl.crt/server_cert.crt > ssl.crt/server_cert.txt

# comprovar que el certificat està ben fet:
openssl x509 -in ssl.crt/server_cert.crt -text

## User

# generar request de certificacio pel user
openssl req -new -extensions v3_req -keyout ssl.key/client_key.pem -out ssl.csr/client_cert-req.pem

# comprovar que està ben feta la request
openssl req -in ssl.csr/client_cert-req.pem -text -verify

# firmar el certificat amb SK de CA
openssl x509 -req -in ssl.csr/client_cert-req.pem -out ssl.crt/client_cert.crt -days 365 -CA ssl.crt/ca_cert.crt -CAkey ssl.key/ca_key.pem -CAcreateserial

#################

# Export the user certificate and its private key 
# This step consists of exporting the user certificate so then 
#  we can import it afterwards in the browser. (PKCS#12) (un .p12)

# exportar certificat del client en format .p12 pel navegador.
openssl pkcs12 -export -in ssl.crt/client_cert.crt -inkey ssl.key/client_key.pem -out client_cert.p12 -name "clientCert"

#################

# Install the certificates in the browser

# 1. > Afegir a "Autorities" el ca_cert.crt
# 2. > Afegir a "My certificates" el client_cert.p12

