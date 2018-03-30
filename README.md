# decrypt_gpg-py
python software to bruteforce a gpg file, crypted by symmetric cipher.

# Help:
`python decrypt_gpg.py --help`

usage: decrypt_gpg.py [-h] [-o OUTPUT] [-i INPUT] [-d DICT]

optional arguments:

  -h, --help            show this help message and exit

Specifica File:

  -o OUTPUT, --output OUTPUT
                        Specify the name of decrypted file
                        
  -i INPUT, --input INPUT
                        Specify the file to decrypt
                        
  -d DICT, --dict DICT
                        Specfy the dictionary file, if not specified, the input file will be decrypted trying every combinations                     

                        
# Example

`python decrypt_gpg.py -o decrypted_file.txt -i crypted_file.txt.gpg`

`python decrypt_gpg.py -o decrypted_file.txt -i crypted_file.txt.gpg -d passList.txt`

                        
# Dependencies
python
                        
