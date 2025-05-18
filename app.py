from flask import Flask, render_template, request, redirect, url_for
import hashlib, random

app = Flask(__name__)

def plaintext_to_binary(text: str) -> str:
    data = text.encode('utf-8')
    return ''.join(format(b, '08b') for b in data)

def binary_to_plaintext(bin_str: str) -> str:
    data = bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))
    return data.decode('utf-8', errors='replace')

def generate_stream_key(seed: str, chain_index: int, length: int) -> str:
    current = seed.encode('utf-8')
    # 초기 해시 체인 offset
    for _ in range(chain_index):
        current = hashlib.sha256(current).digest()
    # 비트 하나씩 뽑아내는 해시체인
    ks = []
    for _ in range(length):
        h = hashlib.sha256(current).digest()
        prng = random.Random(int.from_bytes(h, 'big'))
        bit_seq = [prng.randint(0,1) for _ in range(128)]
        idx2 = h[0] % 128
        ks.append(str(bit_seq[idx2]))
        current = h
    return ''.join(ks)

@app.route('/')
def home():
    return redirect(url_for('encrypt'))

@app.route('/encrypt', methods=['GET','POST'])
def encrypt():
    result_bin = result_hex = keystream = ""
    used_idx = next_idx = 0

    if request.method == 'POST':
        seed   = request.form['seed']
        used_idx = int(request.form['chain_index'])
        plain  = request.form['plaintext']

        plain_bin = plaintext_to_binary(plain)
        keystream = generate_stream_key(seed, used_idx, len(plain_bin))
        # XOR
        cipher_bits = ''.join(
            str(int(b)^int(k))
            for b,k in zip(plain_bin, keystream)
        )
        # HEX
        result_hex = ''.join(
            format(int(cipher_bits[i:i+8],2), '02x')
            for i in range(0, len(cipher_bits),8)
        )
        result_bin = cipher_bits
        # 다음 사용할 인덱스
        next_idx = used_idx + len(keystream)

    return render_template('encrypt.html',
        result_bin=result_bin,
        result_hex=result_hex,
        keystream=keystream,
        used_idx=used_idx,
        next_idx=next_idx
    )

@app.route('/decrypt', methods=['GET','POST'])
def decrypt():
    result_plain = result_bin = keystream = ""
    used_idx = next_idx = 0

    if request.method == 'POST':
        seed   = request.form['seed']
        used_idx = int(request.form['chain_index'])
        fmt    = request.form['format']
        cipher = request.form['ciphertext'].strip()

        if fmt == 'hex':
            result_bin = ''.join(
                format(int(cipher[i:i+2],16), '08b')
                for i in range(0, len(cipher),2)
            )
        else:
            result_bin = cipher

        keystream = generate_stream_key(seed, used_idx, len(result_bin))
        plain_bits = ''.join(
            str(int(c)^int(k))
            for c,k in zip(result_bin, keystream)
        )
        result_plain = binary_to_plaintext(plain_bits)
        next_idx = used_idx + len(keystream)

    return render_template('decrypt.html',
        result_plain=result_plain,
        result_bin=result_bin,
        keystream=keystream,
        used_idx=used_idx,
        next_idx=next_idx
    )

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
