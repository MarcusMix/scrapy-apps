from datetime import datetime

# Mapeamento dos meses em português para inglês
months_map = {
    'janeiro': 'January',
    'fevereiro': 'February',
    'março': 'March',
    'abril': 'April',
    'maio': 'May',
    'junho': 'June',
    'julho': 'July',
    'agosto': 'August',
    'setembro': 'September',
    'outubro': 'October',
    'novembro': 'November',
    'dezembro': 'December'
}

def format_date(date_str):
    try:
        # Separa a data em partes
        parts = date_str.split(' de ')
        if len(parts) == 3:
            day, month_pt, year = parts
            # Remove espaços em branco e converte o mês para inglês
            month_en = months_map.get(month_pt.strip().lower())
            if month_en:
                # Constrói a string da data em inglês
                date_en = f"{day.strip()} {month_en} {year.strip()}"
                # Converte para datetime e formata
                date_obj = datetime.strptime(date_en, '%d %B %Y')
                return date_obj.strftime('%d/%m/%Y')
        return date_str
    except Exception as e:
        # Em caso de erro, imprime a exceção (opcional) e retorna a string original
        print(f"Erro ao formatar a data: {e}")
        return date_str