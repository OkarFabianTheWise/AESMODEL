# FLOW
# Generate a key
# Generate a cipher
# Encrypt/decrypt the data with the cipher
from flask import Flask, render_template, request
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate a key for AES encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key) # Generate a cipher

# b'q9Cc1Iq0GJay-f3zEd9YuyOQr_OaZeVCuUfB8GMEAOo='

# render the interface
@app.route('/')
def index():
    return render_template('index.html')

# page rendering for encryption
@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Retrieve the data submitted in the form
    data = request.form['data']
    
    # Encrypt the data using the cipher suite
    encrypted_data = cipher_suite.encrypt(data.encode())
    
    # Render the result.html template with the encrypted data
    # Decode the encrypted data from bytes to string for rendering
    return render_template('result.html', result=encrypted_data.decode())

# page rendering for decryption
@app.route('/decrypt', methods=['POST'])
def decrypt():
    # Retrieve the encrypted data submitted in the form
    data = request.form['data']
    
    # Decrypt the data using the cipher suite
    decrypted_data = cipher_suite.decrypt(data.encode())
    
    # Render the result.html template with the decrypted data
    # Decode the decrypted data from bytes to string for rendering
    return render_template('result.html', result=decrypted_data.decode())

if __name__ == '__main__':
    app.run(debug=True)
