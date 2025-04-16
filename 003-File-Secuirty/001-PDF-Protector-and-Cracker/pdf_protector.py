import sys
import os
import PyPDF2
import getpass

def securing_pdf(unsecure_pdf, secure_pdf, password):
    try:
        with open(unsecure_pdf, "rb") as  pdf_file:
            pdf_content = PyPDF2.PdfReader(pdf_file)

            if pdf_content.is_encrypted:
                print(f'[!] The input PDF "{unsecure_pdf}" is already encrypted.')
                return
            upgraded_pdf = PyPDF2.PdfWriter()

            for page_num in range(len(pdf_content.pages)):
                upgraded_pdf.add_page(pdf_content.pages[page_num])

            if pdf_content.metadata:
                upgraded_pdf.add_metadata(pdf_content.metadata)

            upgraded_pdf.encrypt(password)

            with open(secure_pdf, "wb") as secure_file:
                upgraded_pdf.write(secure_file)

            print(f'[*] The Secure Upgraded PDF saved as "{secure_pdf}".')

    except Exception as error:
        print(f'[X] An unexpected error occurred while working on "{unsecure_pdf}", Error: {error}')

def main():
    if len(sys.argv) == 3:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]

        if not os.path.exists(input_pdf):
                print(f'[!] Input file "{input_pdf}" does not exist.')
                sys.exit(1)
        if os.path.exists(output_pdf):
                    response = input(f'[?] The file "{output_pdf}" already exists. Overwrite? (y/n): ')
                    if response.lower() != "y":
                        print("[!] Operation cancelled.")
                        sys.exit(0) 
        password = getpass.getpass("Enter password for encryption: ")  

        securing_pdf(input_pdf, output_pdf, password)
    else:
        print("[!] Not enough arguments")
        print("[->] Usage: python3 script.py <input_pdf.pdf> <output_pdf.pdf>")
        sys.exit(1)

if __name__ == "__main__":
    main()


