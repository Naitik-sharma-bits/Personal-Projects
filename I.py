import requests as r
from bs4 import BeautifulSoup

def secrt_msg(url):
    data_points = []
    try:
        response = r.get(url)
        response.raise_for_status()
    except r.exceptions.RequestException as e:
        print(f"Error fetching the document: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        print("Error: No table found in the document")
        return
    rows = table.find_all('tr')
    if not rows:
        print("Error: The table contains no rows.")
        return

    max_x = 0
    max_y = 0

    for row in rows:
        cols = [ele.get_text(strip=True) for ele in row.find_all(['td', 'th'])]

        if len(cols) < 3 or not cols[0].isdigit():
            continue

        try:
            x = int(cols[0])
            char = cols[1]
            y = int(cols[2])
            data_points.append((x, char, y))
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        except ValueError:
            continue

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, char, y in data_points:
        grid[max_y - y][x] = char

    for row in grid:
        print(''.join(row))

secrt_msg("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")