import requests
import bs4

site = "https://www.eftlab.com/knowledge-base/complete-list-of-apdu-responses"

response = requests.get(site)
response.encoding = 'utf-8'
soup = bs4.BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')


def get_sw_description(sw1, sw2):
    res = f"SW1 = {hex(sw1)}, SW2 = {hex(sw2)}\n"

    for row in table.find_all('tr'):
        cols = row.find_all('td')
        # if first value is equal to sw1 and second value is equal to sw2

        if len(cols) >= 4 and cols[0].text == f"{sw1:02X}":
            if cols[1].text == f"{sw2:02X}":
                return "SW1 = " + cols[0].text + ", SW2 = " + cols[1].text + ", description = " + cols[3].text + "\n"

            else:
                try:
                    int(cols[1].text, 16)
                except ValueError:
                    res += ("SW1 = " + cols[0].text + ", SW2 = " + cols[1].text + ", description = " + cols[3].text + "\n")

    if res == "":
        res = "No description found for SW1 = " + f"{sw1:02X}" + " and SW2 = " + f"{sw2:02X}"

    return res


if __name__ == '__main__':
    print(get_sw_description(0x6A, 0x99))
    print(get_sw_description(0x67,0))
