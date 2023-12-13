from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        try:
            data = pd.read_csv('users.csv')
            data = data.to_dict('records')
            return {'data': data}, 200
        except FileNotFoundError:
            return {'message': 'Veri dosyası bulunamadı.'}, 404
        except Exception as e:
            return {'message': 'Beklenmeyen bir hata oluştu.', 'error': str(e)}, 500

    def post(self):
        try:
            json = request.get_json()

            if 'name' not in json or 'age' not in json or 'city' not in json:
                return {'message': 'Eksik bilgi, lütfen tüm alanları doldurun.'}, 400

            name = json['name']
            age = json['age']
            city = json['city']

            if not name.strip() or not city.strip():
                return {'message': 'İsim ve şehir boş olamaz.'}, 400

            if not str(age).isdigit() or int(age) < 0:
                return {'message': 'Geçersiz yaş bilgisi.'}, 400

            req_data = pd.DataFrame({
                'name': [name],
                'age': [age],
                'city': [city]
            })

            data = pd.read_csv('users.csv')
            data = pd.concat([data, req_data], ignore_index=True)
            data.to_csv('users.csv', index=False)
            return {'message': 'Kayıt başarıyla eklendi.'}, 200
        except KeyError as ke:
            return {'message': f'Geçersiz istek: {str(ke)} eksik.'}, 400
        except Exception as e:
            return {'message': 'Beklenmeyen bir hata oluştu.', 'error': str(e)}, 500

    def delete(self):
        try:
            name = request.args.get('name')
            if not name:
                return {'message': 'Silinmek istenen kullanıcının adını belirtmelisiniz.'}, 400

            data = pd.read_csv('users.csv')
            if name in data['name'].values:
                data = data[data['name'] != name]
                data.to_csv('users.csv', index=False)
                return {'message': 'Kayıt başarıyla silindi.'}, 200
            else:
                return {'message': 'Kayıt bulunamadı.'}, 404
        except Exception as e:
            return {'message': 'Beklenmeyen bir hata oluştu.', 'error': str(e)}, 500

class Cities(Resource):
    def get(self):
        try:
            data = pd.read_csv('users.csv', usecols=[2])
            data = data.to_dict('records')
            return {'data': data}, 200
        except FileNotFoundError:
            return {'message': 'Veri dosyası bulunamadı.'}, 404
        except Exception as e:
            return {'message': 'Beklenmeyen bir hata oluştu.', 'error': str(e)}, 500

class Name(Resource):
    def get(self, name):
        try:
            data = pd.read_csv('users.csv')
            data = data.to_dict('records')
            for entry in data:
                if entry['name'] == name:
                    return {'data': entry}, 200
            return {'message': 'Bu isimle kayıt bulunamadı.'}, 404
        except FileNotFoundError:
            return {'message': 'Veri dosyası bulunamadı.'}, 404
        except Exception as e:
            return {'message': 'Beklenmeyen bir hata oluştu.', 'error': str(e)}, 500

# Endpoint isimlendirmesi güncellendi
api.add_resource(Users, '/users/all')
api.add_resource(Cities, '/users/cities')
api.add_resource(Name, '/users/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
