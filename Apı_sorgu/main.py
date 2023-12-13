import requests

# API'nin URL'si
api_url = 'https://dog.ceo/api/breeds/image/random'  # Örnek bir API URL'si

# GET isteği gönderme
response = requests.get(api_url)

# Yanıtı kontrol etme
if response.status_code == 200:  # Başarılı bir şekilde cevap alındı mı?
    data = response.json()  # Yanıtı JSON formatına dönüştürme
    print(data)  # Veriyi ekrana yazdırma veya istediğiniz şekilde işleme alma
else:
    print('Sorgu başarısız oldu. Hata kodu:', response.status_code)
