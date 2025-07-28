import requests

def procurar_vagas(titulo, codigo_pais, work_from_home):
    url = "https://jsearch.p.rapidapi.com/search"
    query = f"{titulo}"

    headers = {
        "X-RapidAPI-Key": "132a194c79msh0d0b19d09d4c927p14a36ajsn841cbb868d67",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,                                   # Free-form jobs search query. It is highly recommended to include job title and location as part of the query
        "page": "1",                                      # Page to return (each page includes up to 10 results)
        "num_pages": "1",                                 # Number of pages to return
        "country": codigo_pais,                           # Country code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country from which to return job postings
        "date_posted": "all",                             # Find jobs posted within the time you specify. all, today, 3days, week, month
        "work_from_home": work_from_home,                 # Only return remote jobs.
        "employment_types": "FULLTIME, PARTTIME, INTERN", # Find jobs of particular employment types, specified as a comma delimited list of the following values: FULLTIME, PARTTIME, INTERN.
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    vagas_encontradas = set()

    if "data" in data:
        for vaga in data["data"]:
            print(f"\n🔹 {vaga['job_title']} at {vaga['employer_name']}")
            print(f"📍 {vaga['job_city']}, {vaga['job_country']}")
            print(f"🔗 {vaga['job_apply_link']}")
            vagas_encontradas.add((vaga['job_title'], vaga['employer_name'], vaga['job_city'], vaga['job_country'], vaga['job_apply_link']))
    else:
        print("Nenhuma vaga encontrada ou erro na API.")

    return vagas_encontradas


def obter_codigo_pais(localizacao):
    localizacao = localizacao.strip().lower()
    
    paises = {
        "portugal": "pt", "espanha": "es", "frança": "fr", "france": "fr", "alemanha": "de", "germany": "de",
        "itália": "it", "italia": "it", "italy": "it", "reino unido": "gb", "united kingdom": "gb", "uk": "gb",
        "irlanda": "ie", "ireland": "ie", "holanda": "nl", "netherlands": "nl", "bélgica": "be", "belgica": "be", "belgium": "be",
        "suíça": "ch", "suica": "ch", "switzerland": "ch", "austria": "at", "polônia": "pl", "polonia": "pl", "poland": "pl",
        "noruega": "no", "norway": "no", "suécia": "se", "suecia": "se", "sweden": "se", "finlândia": "fi", "finlandia": "fi", "finland": "fi",
        "estados unidos": "us", "united states": "us", "usa": "us",
        "canadá": "ca", "canada": "ca",
        "austrália": "au", "australia": "au"
    }

    for nome, codigo in paises.items():
        if nome in localizacao:
            return codigo
        
    return None

def main():
    print("=== Busca de Vagas ===")

    titulo = input("Título: ").strip()
    localizacao = input("País: ").strip()
    codigo_pais = obter_codigo_pais(localizacao)

    if not codigo_pais:
        print("País não suportado.")
        return

    vagas_encontradas = set()

    for work_from_home in ["true", "false"]:
        print("\n--- Procurando vagas ---")
        vagas = procurar_vagas(titulo, codigo_pais, work_from_home)
        vagas_encontradas.update(vagas)

    with open("linkedin_jobs_result.txt", "w", encoding="utf-8") as f:
        for vaga in vagas_encontradas:
            f.write(f"🔹 {vaga[0]} at {vaga[1]}\n")
            f.write(f"📍 {vaga[2]}, {vaga[3]}\n")
            f.write(f"🔗 {vaga[4]}\n\n")

if __name__ == "__main__":
    main()