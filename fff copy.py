from PyPDF2 import PdfReader
import regex as re
import pandas as pd

# Function to extract Stage 1 complaints
def extract_stage1_complaints(text):
    stage1_pattern = re.compile(
        r"(?P<Programme>.+?)\s+(?P<Service>BBC\s\w+)\s+(?P<Date>\d{2}/\d{2}/\d{2,4})\s+(?P<Main_Issue>.+?)\s+(?P<Number_of_Complaints>\d+)"
    )
    return [match.groupdict() for match in stage1_pattern.finditer(text)]

# Function to extract Stage 2 complaints
def extract_stage2_complaints(text):
    stage2_pattern = re.compile(
        r"(?P<Programme>.+?)\s+(?P<Service>BBC[\w\s]+)\s+(?P<Date>\d{2}/\d{2}/\d{2,4})\s+(?P<Issue>.+?)\s+(?P<Outcome>Resolved|Not upheld|Upheld)"
    )
    return [match.groupdict() for match in stage2_pattern.finditer(text)]

# Function to extract text and structured data from a PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    # Extract text
    extracted_text = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text.strip())
            else:
                print(f"Warning: No text found on page {i} in {pdf_path}")
        except Exception as e:
            print(f"Error extracting text from page {i} in {pdf_path}: {e}")

    # Combine all text into a single string
    return "\n".join(extracted_text)

# Function to process potential links
def clean_links(text):
    """Remove embedded links in text."""
    return re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)

# Main function
def main():
    pdf_path = "/home/lucy/Desktop/transphobse/data/bbc_complaint_pdfs/7 - 20 June 2021.pdf"
    text = extract_text_from_pdf(pdf_path)

    if not text:
        print("No text extracted from the PDF.")
        return

    # Clean text for embedded links
    text = clean_links(text)

    # Extract Stage 1 and Stage 2 complaints
    stage1_data = extract_stage1_complaints(text)
    stage2_data = extract_stage2_complaints(text)

    # Convert data to DataFrames for structured viewing
    stage1_df = pd.DataFrame(stage1_data)
    stage2_df = pd.DataFrame(stage2_data)

    print("Stage 1 Complaints:")
    print(stage1_df)

    print("\nStage 2 Complaints:")
    print(stage2_df)

    # Save to CSV for future reference
    stage1_df.to_csv("stage1_complaints.csv", index=False)
    stage2_df.to_csv("stage2_complaints.csv", index=False)

if __name__ == "__main__":
    main()
