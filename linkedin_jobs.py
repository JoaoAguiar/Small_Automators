import requests
import threading
import os
import flet as ft

def procurar_vagas(titulo, codigo_pais, work_from_home):
    url = "https://jsearch.p.rapidapi.com/search"
    query = f"{titulo}"

    headers = {
        "X-RapidAPI-Key": "132a194c79msh0d0b19d09d4c927p14a36ajsn841cbb868d67",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": "1",
        "num_pages": "5",
        "country": codigo_pais,
        "date_posted": "all",
        "work_from_home": work_from_home,
        "employment_types": "FULLTIME, PARTTIME, INTERN",
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    vagas_encontradas = set()

    if "data" in data:
        for vaga in data["data"]:
            vagas_encontradas.add((vaga['job_title'], vaga['employer_name'], vaga['job_city'], vaga['job_country'], vaga['job_apply_link']))
    
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

def create_output_directory():
    default_dir = r"C:\Users\jpagu\Downloads\LinkedIn Jobs"

    if not os.path.exists(default_dir):
        try:
            os.makedirs(default_dir)
    
            return default_dir
        except Exception as e:
            return None
    
    return default_dir

def main(page: ft.Page):
    page.title = "LinkedIn Job Search"
    page.window_resizable = False
    page.window.center()
    page.theme_mode = "light"
    page.padding = 30
    page.window.height = 575
    page.window.width = 500
    # page.window_icon = r"C:\caminho\para\seu\icon.ico"
    
    # Create UI elements
    title = ft.Text(
        "LinkedIn Job Search",
        size=30,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900,
        text_align=ft.TextAlign.CENTER
    )
    
    job_title_field = ft.TextField(
        label="Job Title",
        hint_text="e.g., Data Analyst",
        width=250,
        border_radius=10,
        border_color=ft.Colors.BLUE_600,
        focused_border_color=ft.Colors.BLUE_600,
    )
    
    country_field = ft.TextField(
        label="Country",
        hint_text="e.g., Portugal, Germany, USA",
        width=250,
        border_radius=10,
        border_color=ft.Colors.BLUE_600,
        focused_border_color=ft.Colors.BLUE_600,
    )

    search_button = ft.ElevatedButton(
        text="Search Jobs",
        width=100,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=False
    )
    
    progress_ring = ft.ProgressRing(
        visible=False,
        color=ft.Colors.BLUE_600,
        width=25,
        height=25
    )
    
    status_text = ft.Text(
        "Ready to search for jobs",
        size=14,
        color=ft.Colors.BLUE_600,
        text_align=ft.TextAlign.CENTER
    )
    
    output_info = ft.Text(
        f"Results saved to: C:\\Users\\jpagu\\Downloads\\LinkedIn Jobs",
        size=12,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER
    )
        
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def show_success_dialog(message, file_path):
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Search Completed!", color=ft.Colors.GREEN_600),
            content=ft.Column([
                ft.Text(message),
                ft.Divider(),
                ft.Text("File saved to:", weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(file_path, size=12),
                    bgcolor=ft.Colors.GREY_100,
                    padding=10,
                    border_radius=5
                )
            ], tight=True),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(success_dialog))
            ],
        )
        page.dialog = success_dialog
        success_dialog.open = True
        page.update()
    
    def search_jobs(e):
        titulo = job_title_field.value.strip()
        localizacao = country_field.value.strip()
        codigo_pais = obter_codigo_pais(localizacao)

        if not titulo or not localizacao or not codigo_pais:
            return
        
        output_dir = create_output_directory()
        
        # Update UI for searching
        search_button.disabled = True
        progress_ring.visible = True
        status_text.value = "Searching for jobs... Please wait"
        status_text.color = ft.Colors.BLUE_600

        page.update()
        
        def search_thread():
            try:
                vagas_encontradas = set()
                
                # Search for both remote and on-site jobs
                for work_from_home in ["true", "false"]:
                    vagas = procurar_vagas(titulo, codigo_pais, work_from_home)
                    vagas_encontradas.update(vagas)
                
                if vagas_encontradas:
                    # Save results to file
                    output_file = os.path.join(output_dir, f"linkedin_jobs_{titulo.replace(' ', '_')}_{codigo_pais}.txt")
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(f"Job Title: {titulo}\n")
                        f.write(f"Country: {localizacao} ({codigo_pais.upper()})\n")
                        f.write(f"Total jobs found: {len(vagas_encontradas)}\n\n")
                        
                        for i, vaga in enumerate(vagas_encontradas, 1):
                            f.write(f"{i}. {vaga[0]} at {vaga[1]}\n")
                            f.write(f"   📍 {vaga[2]}, {vaga[3]}\n")
                            f.write(f"   🔗 {vaga[4]}\n\n")
                    
                    def update_ui_success():
                        progress_ring.visible = False
                        search_button.disabled = False
                        status_text.value = f"Search completed! Found {len(vagas_encontradas)} jobs"
                        status_text.color = ft.Colors.BLUE_600
                        
                        page.update()

                        show_success_dialog(f"Found {len(vagas_encontradas)} job(s)!", output_file)
                    
                    page.run_thread(update_ui_success)
                else:
                    def update_ui_no_results():
                        progress_ring.visible = False
                        search_button.disabled = False
                        status_text.value = "No jobs found"
                        status_text.color = ft.Colors.ORANGE_600
                        
                        page.update()
                    
                    page.run_thread(update_ui_no_results)
                    
            except Exception as ex:
                def update_ui_error():
                    progress_ring.visible = False
                    search_button.disabled = False
                    status_text.value = "Search failed"
                    status_text.color = ft.Colors.RED_600

                    page.update()
                
                page.run_thread(update_ui_error)

        threading.Thread(target=search_thread, daemon=True).start()

    search_button.on_click = search_jobs
    
    # Layout
    page.add(
        ft.Container( 
            content=ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=title,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=30)
                    ),
                    
                    # Input fields
                    ft.Container(
                        content=ft.Column([
                            job_title_field,
                            ft.Container(height=5),
                            country_field,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=25)
                    ),
                    
                    # Search button and progress
                    ft.Container(
                        content=ft.Column([
                            search_button,
                            ft.Container(height=10),
                            progress_ring,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=25)
                    ),
                    
                    # Status and info
                    ft.Container(
                        content=ft.Column([
                            status_text,
                            ft.Container(height=5),
                            output_info,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
                    offset=ft.Offset(0, 0),
                )
            ),
            alignment=ft.alignment.center,  
            expand=True,                   
        )
    )

if __name__ == "__main__":
    ft.app(main)