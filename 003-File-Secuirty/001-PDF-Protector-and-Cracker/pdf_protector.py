import sys
import PyPDF2

def securing_pdf(unsecure_pdf, secure_pdf, password):
    try:
        with open(unsecure_pdf, "rb") as  pdf_file:
            pdf_content = PyPDF2.PdfReader(pdf_file)
            upgraded_pdf = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_content.pages)):
            upgraded_pdf.add_page(pdf_content.pages(page_num))

        upgraded_pdf.encrypt(password)

        with open(secure_pdf, "wb") as secure_file:
            upgraded_pdf.write(secure_file)

        print(f"[*] The Secure Upgraded PDF saved as {secure_pdf}.")

    except Exception as error:
        print(f"[X] Something went wrong while working on {unsecure_pdf}.\nError: {error}")

def main():
    if len(sys.argv) == 4:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        password = sys.argv[3]
        securing_pdf(input_pdf, output_pdf, password)
    else:
        print("[!] Not enough arguments")
        print("[->] Usage: python3 script.py <input_pdf.pdf> <output_pdf.pdf> <Password>")
        sys.exit(1)

if __name__ == "__main__":
    main()


