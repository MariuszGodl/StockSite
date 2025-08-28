from openai import OpenAI
from Other.imports import *



def parse_creation_date(raw_date: str) -> datetime.date:
    # Clean up string
    date_str = raw_date.strip()
    
    # Normalize separators: spaces, slashes -> dashes
    date_str = re.sub(r"[\/\s]+", "-", date_str)
    
    # Possible formats to try
    formats = [
        "%Y-%m-%d",  # 2025-08-28
        "%d-%m-%Y",  # 28-08-2025
        "%m-%d-%Y",  # 08-28-2025
    ]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    # If nothing works, raise an error
    raise ValueError(f"Unrecognized date format: {raw_date}")

def company_classifcation(company_name, company_ticker, company_description):

    gpw_categories = [
        "Banks",
        "Insurance & Financial ",
        "Real Estate Developers",
        "Construction &  Materials",
        "Energy",
        "Oil & Gas ",
        "Mining & Metals",
        "Chemicals",
        "Pharmaceuticals & Biotech",
        "Food & Beverages",
        "Retail & Wholesale Trade",
        "IT Services & Software ",
        "Telecommunications",
        "Media & Entertainment",
        "Transport & Logistics",
        "Automotive & Machinery",
        "Electronics & Electrl Equip",
        "Paper, Packaging & Printing",
        "Tourism, Hotels & Leisure",
        "Clothing & Textiles",
        "Other"
    ]

    # initialize client
    client = OpenAI(api_key=os.getenv("KEY"))
    # company_name = 'Magna Polonia SA'
    # company_ticker= '06MAGNA'
    # company_description = 'Grupa Kapitałowa Magna Polonia koncentruje się na działalności inwestycyjnej oraz świadczeniu usług w branży IT i telekomunikacji. Spółka dominująca realizuje inwestycje w spółki z sektorów nowych technologii, IT, automatyki i energetyki. Kluczowe obszary działalności Grupy obejmują: tworzenie systemów geoinformatycznych i map cyfrowych, usługi transmisji danych oraz rozwój innowacyjnych rozwiązań telematycznych. Grupa dostarcza również oprogramowanie i systemy nawigacyjne dla firm transportowych. Działalność jest prowadzona głównie na rynku krajowym. Grupa pozyskuje kapitał m.in. poprzez emisję obligacji oraz inwestycje w instrumenty finansowe.'
    # # basic query
    category_resp = client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {"role": "system", "content": "Answer in one of the categories without punctuation"},
            {"role": "user", "content": f'Classify the company {company_name} ({company_ticker}) into one of {gpw_categories}. Description: {company_description}'}
        ]
    )
    category = category_resp.choices[0].message.content.strip()

    # Creation date query
    date_resp = client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {"role": "system", "content": "Answer in only date format YYYY-MM-DD without punctuation"},
            {"role": "user", "content": f'Provide the creation date of the company {company_name} ({company_ticker}). Description: {company_description}'}
        ]
    )
    creation_date = parse_creation_date(date_resp.choices[0].message.content)
    #print(category, creation_date)
    return category, creation_date

