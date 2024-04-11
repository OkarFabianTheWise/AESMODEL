# Import necessary modules from the Flask framework
from flask import Flask, redirect, url_for, render_template, request

# Import padding functionality from cryptography for RSA encryption
from cryptography.hazmat.primitives.asymmetric import padding

# rsa: is used for RSA key generation
from cryptography.hazmat.primitives.asymmetric import rsa

# default_backend is used for RSA key generation
from cryptography.hazmat.backends import default_backend

# hashes: hashing functionality from cryptography for hashing algorithms
from cryptography.hazmat.primitives import hashes

# flask instance
app = Flask(__name__)

# Generate RSA key pair: used to decrypt
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# public key used to encrypt
public_key = private_key.public_key()

# render the interface
@app.route('/')
def index():
    try:
        error_message = request.args.get('error_message')
        return render_template('index.html', error_message=error_message)
    except Exception as e:
        print("Error in index route:", e)

# page rendering for encryption
@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.form['data'].encode()  # Ensure data is encoded to bytes
        encrypted_data = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return render_template('result.html', result=encrypted_data.hex())  # Render hex representation of encrypted data
    except KeyError:
        error_message = "Data not provided for encryption"
    except ValueError:
        error_message = "Invalid data provided"
    except Exception as e:
        error_message = "An error occurred during encryption"
        print("Encryption error:", e)
    return render_template('error.html', error_message=error_message)

# page rendering for decryption
@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = bytes.fromhex(request.form['data'])  # Convert hex string back to bytes
        decrypted_data = private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return render_template('result.html', result=decrypted_data.decode())
    except ValueError:
        error_message = "Invalid data provided for decryption"
    except Exception as e:
        error_message = "An error occurred during decryption"
        print("Decryption error:", e)
    return redirect(url_for('index', error_message=error_message))

if __name__ == '__main__':
    app.run(debug=True)
