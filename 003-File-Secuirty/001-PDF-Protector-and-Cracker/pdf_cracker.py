#!/usr/bin/env python3
import PyPDF2
import sys
import os
def crack_pdf(pdf_file, wordlist):
    if os.path.exists(pdf_file) == False:
        print(f'[!] PDF file "{pdf_file}" not found.')
        return
    if os.path.exists(wordlist) == False:
        print(f'[!] Wordlist "{wordlist}" not found.')
        return
    
    with open(pdf_file, "rb") as file:
        pdf = PyPDF2.PdfReader(pdf_file)
        if not pdf.is_encrypted:
            print(f'[!] "{pdf_file}" is not encrypted.')
            return
        
        with open(wordlist, "r") as file:
            for password in file:
                password = password.strip()
                result = pdf.decrypt(password)
                if result:
                    print(f"[+] Password found: {password}")
                    sys.exit(0)
                else:
                    print(f"[-] Incorrect password: {password}")
                    
    print("[X] Password not found in the wordlist.")

def main():
    if len(sys.argv) != 3:
        print("[!] Not enough arguments")
        print("Usage: python3 pdf_cracker.py <encrypted.pdf> <wordlist.txt>")
        sys.exit(1)
    else:
        encrypted_pdf = sys.argv[1]
        wordlist = sys.argv[2]
        crack_pdf(encrypted_pdf, wordlist)

if __name__ == "__main__":
    main()