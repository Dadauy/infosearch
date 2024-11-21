import requests
from bs4 import BeautifulSoup

# for i in range(1, 4 + 1):
#     url = f"https://magizoo.ru/stati/koshki/?PAGEN_1={i}"
#     response = requests.get(url)
#     print(response)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     element = soup.find_all('a', class_='entry', href=True)
#     for link in element:
#         urls.append(link['href'])
# print(urls)

urls = ['/stati/koshki/koshka-otkazyvaetsya-ot-kotyat-prichiny-chto-delat/',
        '/stati/koshki/vybor-podhodyashchej-zashchity-ot-kleshchej/',
        '/stati/koshki/chto-nado-znat-o-sterilizacii-koshek/', '/stati/koshki/kakuyu-porodu-koshki-vybrat/',
        '/stati/koshki/kak-podruzhit-koshek-v-odnom-dome/', '/stati/koshki/koltunorezy-dlya-koshek/',
        '/stati/koshki/kakaya-trava-polezna-dlya-koshek/', '/stati/koshki/obzor-korma-brit-dlya-koshek/',
        '/stati/koshki/kakie-vitaminy-davat-koshke-ot-vypadeniya-shersti/', '/stati/koshki/koshachij-shampun-ot-bloh/',
        '/stati/koshki/kak-vylechit-svishch-u-koshki/', '/stati/koshki/kak-vybrat-lezhanku-dlya-koshki/',
        '/stati/koshki/vybor-lotka-dlya-koshki/', '/stati/koshki/kak-polzovatsya-kogterezkoj/',
        '/stati/koshki/pasta-dlya-vyvedeniya-shersti-u-koshek/', '/stati/koshki/anticarapki-dlya-koshek/',
        '/stati/koshki/kak-odevat-i-vygulivat-koshku-na-povodke/', '/stati/koshki/lechenie-lishaya-u-koshek/',
        '/stati/koshki/kak-otuchit-kota-drat-mebel/', '/stati/koshki/oshejniki-ot-bloh-i-kleshchej-dlya-koshek/',
        '/stati/koshki/kak-kormit-beremennuyu-koshku/', '/stati/koshki/pochemu-koshki-kusayutsya-i-kak-ih-otuchit/',
        '/stati/koshki/pochemu-u-koshki-tekut-slezy/', '/stati/koshki/vybiraem-kogtetochku-dzhut-ili-sizal/',
        '/stati/koshki/kak-pravilno-chistit-ushi-koshke/', '/stati/koshki/pochemu-ot-koshki-neprijatno-pahnet/',
        '/stati/koshki/kak-otuchit-kota-metit-territoriju/', '/stati/koshki/kak-zastavit-koshku-pit-vodu/',
        '/stati/koshki/opasnaja-eda-dlja-koshek/', '/stati/koshki/artrit-u-sobak/',
        '/stati/koshki/adaptacija-kotjonka-v-novom-dome/', '/stati/koshki/6-prichin-pochemu-kishki-spyat-s-hozyaevami/',
        '/stati/koshki/mochekamennaya-bolezn-u-kotov/', '/stati/koshki/pochemu-koshka-topchet-vas-lapami/',
        '/stati/koshki/chumka-u-sobak-i-koshek/', '/stati/koshki/priznaki-beremennosti-u-koshki/',
        '/stati/koshki/stress-u-koshki/', '/stati/koshki/kastratsiya-kota-i-sterilizatsiya-koshki/',
        '/stati/koshki/kak-i-chem-strich-koshke-kogti/', '/stati/koshki/kak-vybrat-preparaty-ot-glistov-dlya-koshek/',
        '/stati/koshki/pochemu-lazernaya-ukazka-vredna-dlya-koshek/',
        '/stati/koshki/chitaem-sostav-sukhogo-korma-dlya-koshek-pravilno/', '/stati/koshki/chto-takoe-kholistik-korm/',
        '/stati/koshki/vybor-koshachyego-napolnitelya/', '/stati/koshki/kak-pomyt-kota/',
        '/stati/koshki/kak-pomyt-kotenka/', '/stati/koshki/kogtetochki-chto-eto-takoe-i-zachem-oni-nuzhny/',
        '/stati/koshki/obzor-korma-viskas/', '/stati/koshki/furminatory-dlya-koshek/',
        '/stati/koshki/obzor-korma-royal-canin-dlya-koshek/', '/stati/koshki/obzor-korma-pro-plan-dlya-koshek/',
        '/stati/koshki/uhod-za-kotom-posle-kastracii/', '/stati/koshki/osobennosti-holistik-kormov-dlya-koshek/',
        '/stati/koshki/kakie-vitaminy-mozhno-davat-koshke/', '/stati/koshki/kak-pravilno-podobrat-korm-dlya-koshki/',
        '/stati/koshki/kak-vybrat-perenosku-dlya-koshki/',
        '/stati/koshki/reyting-luchshikh-kormov-dlya-sterilizovannykh-koshek-i-kastrirovannykh-kotov/',
        '/stati/koshki/prichiny-i-lechenie-ponosa-u-koshek/', '/stati/koshki/domiki-dlya-koshek/',
        '/stati/koshki/sredstva-dlja-uhoda-za-sherstju-sobak-i-koshek/',
        '/stati/koshki/blohi-i-kleshhi-u-koshek-lechenie/', '/stati/koshki/kak-vybrat-dieticheskij-korm-dlja-koshek/',
        '/stati/koshki/kakie-vitaminy-davat-koshke/', '/stati/koshki/kakuju-igrushku-vybrat-dlja-koshki/',
        '/stati/koshki/kak-sdelat-domik-dlja-koshki/', '/stati/koshki/kak-vybrat-furminator/',
        '/stati/koshki/kak-vybrat-korm-dlya-kotenka/', '/stati/koshki/sovety-po-vyboru-kogtetochki/',
        '/stati/koshki/odezhda-dlya-domashnikh-pitomtsev/']
print(len(urls))

# for idx, url in enumerate(urls):
#     response = requests.get("https://magizoo.ru" + url)
#     print(idx, url, response)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     title = soup.find_all('h1', class_='site-title')[0].get_text()
#     text = soup.find_all('div', class_="news__detail__detailText")[0].get_text()
#     with open(f"Ytrain/{idx}.txt", "w", encoding="utf8") as file:
#         file.writelines(title)
#     with open(f"Xtrain/{idx}.txt", "w", encoding="utf8") as file:
#         file.writelines(text)
