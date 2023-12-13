import requests

def make_api_request():
    try:
        api_url = input("API URL'sini girin: ")
        http_method = input("HTTP methodunu girin (GET, POST, PUT, DELETE vb.): ")

        if http_method.upper() not in ["GET", "POST", "PUT", "DELETE"]:
            print("Geçersiz HTTP methodu!")
            return

        custom_params = {}
        if http_method.upper() == "GET":
            # Kullanıcıdan GET için isteğe özel parametreler alma
            params_count = int(input("Kaç tane isteğe özel parametre gireceksiniz? "))
            print("Parametreleri girin (param_adı:param_değeri formatında): ")
            for _ in range(params_count):
                param = input().split(':')
                if len(param) == 2:
                    custom_params[param[0]] = param[1]
                else:
                    print("Geçersiz parametre formatı, örnek: param_adı:param_değeri")

        response = requests.request(http_method.upper(), api_url, params=custom_params)

        if response.status_code == 200:
            data = response.json()
            print("Başarılı istek! Gelen veri:\n", data)
        else:
            print('Sorgu başarısız oldu. Hata kodu:', response.status_code)
    except requests.RequestException as e:
        print('Bağlantı hatası:', e)

make_api_request()