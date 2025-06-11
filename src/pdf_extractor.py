import fitz  # PyMuPDF
import json
import os

def extract_pdf_text_with_page_numbers(pdf_path, output_json_path):
    data = []
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            lines = text.splitlines()
            start = False
            count = 0
            temp_values = {}
            for line in lines:
                if "Unweighted frequencies:" in line:
                    start = True
                elif start and count == 0:
                    # its key
                    temp_values["column_name"] = line.strip()
                    count += 1
                    temp_values["page_number"] = page_num
                elif start and count == 1:
                    # its the description
                    temp_values["column_description"] = line.strip()
                    count = 0
                    start = False
                    # check if there is code in the second line
                    if "code" == line.strip().lower():
                        words = temp_values["column_name"].split(" ")
                        temp_values["column_name"] = words[0]
                        temp_values["column_description"] = " ".join(words[1:])
                    temp_values["page_number"] = page_num
            if len(temp_values)>0:
                data.append(temp_values)

    with open(output_json_path, mode = "w") as file_buffer:
        json.dump({"descriptions" : data}, file_buffer)
    
    return data


# Example usage
if __name__ == "__main__":
    years = [19, 20, 21, 22, 23]
    for year in years:
        pdf_path = f"data/adult-codebook {year}.pdf"  # Replace with your PDF file path
        output_json_path = f"assets/adult-codebook_{year}.json"
        data = extract_pdf_text_with_page_numbers(pdf_path, output_json_path)

        for page in data:
            if len(page)>0:
                print(f"--- Page {page['page_number']} ---")
                print(f"{page['column_name']} >>> {page['column_description']}" )
                print()
