#!/usr/bin/env python
# -*- coding: latin-1 -*-

import subprocess
import sys
import string
import itertools
import argparse

# variabile booleana, verra' settata a True quando la password è trovata, cosi' esco dal while
pwdFound = False
# variabile che specifica se deve essere usato o no il dizionario
usaDizionario = False
# gestione degli argomenti
parser = argparse.ArgumentParser()
group = parser.add_argument_group('Specifica File')
group.add_argument('-o','--output', help='Specifica il nome del file decifrato')
group.add_argument('-i','--input', help='Specifica il file da decifrare')
group.add_argument('-d','--dict', help='Inserisci il dizionario, se non specificato verrà fatto un bruteforce')
args = parser.parse_args()
if not args.output:
	print ('File di output non specificato: vedi Help --help')
	pwdFound = True
else:
	decripted = args.output
if not args.input:
	print ('File di input non specificato: vedi Help --help')
	pwdFound = True
else:
	target = args.input
if args.dict:
	usaDizionario = True
	dizionario = args.dict


caratteri = string.digits+string.ascii_letters+string.punctuation
#caratteri = string.punctuation
# aggiungo il carattere spazio, alla stringa caratteri
caratteri = ' '+caratteri
#print caratteri

# escape caratteri speciali che danno problemi nella bash
def escapeSpChar(s):
	return s.replace("\\", "\\\\").replace("'","\\'").replace('"','\\"').replace("`","\\`").replace("$","\$")

def crack(password, passwordEscaped):
	""" eseguo il comando per decifrare il file, l'esito dell'operazione viene salvato 
	# nella variabile cracked """
	cracked = subprocess.call('gpg --pinentry-mode loopback -d --output '+decripted+' --passphrase "'+passwordEscaped+'" '+target+' 2>/dev/null', shell=True)

	#se il valore contenuto il cracked e' 0, significa che il comando ha avuto esito positivo
	if cracked == 0:
		# stampo la password giusta in verde, poi rimetto i colori di default
		print ('Password Trovata: \033[32m'+password+'\033[0m\nFile decifrato con successo!')
		return 1
	# la password e' sbagliata
	elif cracked == 2:
		# stampo la password errata in rosso, poi rimetto i colori di default
		print('\033[31m'+password+'\033[0m')

# contatore, numero di caratteri della password da cui deve iniziare a provare
count = 1

# se è stato passato un dizionario, uso questo, altrimenti faccio il bruteforce
if (usaDizionario == True) and (not pwdFound):
	# conto il numero di linee nel file
	numLinee = sum(1 for i in open(dizionario))
	# variabile che tiene il conto del numero di password provate
	tested = 0

	# importo file 'password list'
	passFile = open(dizionario)

	# leggo ogni linea del file
	for line in passFile:
		tested = tested+1
		print ('Password '+str(tested)+' di '+str(numLinee))
		# pulisco la stringa letta da eventuali spazi iniziali e finali
		password = line.strip()
		passwordEscaped = escapeSpChar(password)
		# eseguo il comando per decifrare il file, l'esito dell'operazione viene salvato nella variabile cracked
		cracked = subprocess.call('gpg --pinentry-mode loopback -d --output '+decripted+' --passphrase "'+passwordEscaped+'" '+target+' 2>/dev/null', shell=True)
		
		# se il valore contenuto il cracked e' 0, significa che il comando ha avuto esito positivo
		if cracked == 0:
			# stampo la password giusta in verde, poi rimetto i colori di default
			print ('Password Trovata: \033[32m'+password+'\033[0m\nFile decifrato con successo!')
			# interrompo il ciclo for in quanto ho trovato la password
			break
		# la password e' sbagliata
		elif cracked == 2:
			# stampo la password errata in rosso, poi rimetto i colori di default
			print('\033[31m'+password+'\033[0m')
	passFile.close()

else:
	while not pwdFound:
		# faccio il prodotto cartesiano tra "count" caratteri
		""" viene fatto il prodotto cartesiano tra tutti gli elementi della variabile "caratteri"
		# restituendo una tupla di "count" elementi
		# quindi quando count=1 > i=a, i=b, ecc... quando count=2 > i=aa, i=ab, ecc... """
		for i in itertools.product(caratteri, repeat=count):
			#print i
			""" salvo in password il valore di i 
			# (uso "= ''.join(i)" al posto di "= i" perchè cosi' non mi memorizza le parentesi e gli apici) """
			password = ''.join(i)
			# escape special character \, ", ', $, `
			passwordEscaped = escapeSpChar(password)
			
			# se la password e' giusta, esco dal ciclo for
			if (crack(password, passwordEscaped) == 1):
				# setto pwdFound a True per uscire dal while
				pwdFound = True
				break
		# incremento il contatore di 1 per fare il prodotto cartesiano tra piu' caratteri
		count += 1
