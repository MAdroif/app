from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import os
from flask_cors import CORS

# Konfigurasi autentikasi Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets ']
SERVICE_ACCOUNT_INFO = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))  # Ganti dengan path file JSON
SPREADSHEET_ID = '1XmQwRT5BqWSFDY_iv9RqlfgvWNOaI7LxyGf3heQPBdI'  # Ganti dengan ID spreadsheet Anda

creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Fungsi membaca data
def read_data():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A:C").execute()
    values = result.get('values', [])
    return values

# Fungsi menulis data
def write_data(new_row):
    body = {'values': [new_row]}
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A:C",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    return result

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)

# *** TAMBAHKAN BAGIAN INI ***
@app.route('/')
def home():
    return "Backend Anda berjalan dengan baik!"

# Endpoint untuk membaca data
@app.route('/read', methods=['GET'])
def read():
    data = read_data()
    return jsonify(data)

# Endpoint untuk menulis data
@app.route('/write', methods=['POST'])
def write():
    new_row = request.json
    if not new_row or not isinstance(new_row, list) or len(new_row) != 3:
        return jsonify({"error": "Invalid input"}), 400
    write_data(new_row)
    return jsonify({"message": "Data berhasil ditambahkan!"})

if __name__ == '__main__':
    app.run(debug=True)
