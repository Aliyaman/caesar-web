from flask import Flask, render_template, request
from string import ascii_letters

app = Flask(__name__)

def caesar_encrypt(kelime, key):
    enc_msg = []
    for harf in kelime:
        if harf in ascii_letters:
            k = ascii_letters.index(harf)
            enc = k + key
            enc_msg.append(ascii_letters[enc].lower())
    return "".join(enc_msg)

def brute_force(kelime):
    results = []
    enc_msg = list(kelime)
    
    # Replace 'i' with 't' as in original code
    for idx, b in enumerate(enc_msg):
        if b == "i":
            enc_msg[idx] = "t"
            
    for keys in range(1, 26):
        decrypt = []
        for i in enc_msg:
            if i in ascii_letters:
                k = ascii_letters.index(i)
                dec = k - keys
                if dec < 0:
                    dec = dec + 26
                if dec > 25:
                    dec = dec - 26
                decrypt.append(ascii_letters[dec].lower())
        results.append({"text": "".join(decrypt), "key": keys})
    return results

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    original_text = ''
    encrypted_text = ''
    if request.method == 'POST':
        kelime = request.form.get('kelime', '')
        key = request.form.get('key', '')
        if kelime and key.isdigit():
            key = int(key)
            if 1 <= key <= 25:
                encrypted_text = caesar_encrypt(kelime, key)
                original_text = kelime
    return render_template('encrypt.html', 
                         original_text=original_text, 
                         encrypted_text=encrypted_text)

@app.route('/brute', methods=['GET', 'POST'])
def brute():
    results = []
    original_text = ''
    if request.method == 'POST':
        kelime = request.form.get('kelime', '')
        if kelime:
            original_text = kelime
            results = brute_force(kelime)
    return render_template('brute.html', 
                         original_text=original_text, 
                         results=results)

if __name__ == '__main__':
    app.run(debug=True) 