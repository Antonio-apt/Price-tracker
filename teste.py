
from bs4 import BeautifulSoup
html = '<span class="PriceUI-bwhjk3-11 cmTHwB PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ">R$ <!-- -->1.879,99</span>'

html = BeautifulSoup(html, features="html.parser")
html = html.get_text()
print(html)