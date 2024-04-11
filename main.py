# FLOW
# Generate a key
# Generate a cipher
# Encrypt/decrypt the data with the cipher
from flask import Flask, redirect, url_for, render_template, request
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate a key for AES encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key) # Generate a cipher

# b'q9Cc1Iq0GJay-f3zEd9YuyOQr_OaZeVCuUfB8GMEAOo='

# render the interface
@app.route('/')
def index():
    try:
        # Check if an error message is present in the query parameters
        error_message = request.args.get('error_message')
        
        print("error_message:", error_message)
        # Render the index.html template, passing the error message to the template
        return render_template('index.html', error_message=error_message)
    except Exception as c:
        print("Ïndex err:", c)

# page rendering for encryption
@app.route('/encrypt', methods=['POST'])
def encrypt():
    # wrap code in try and except block to display error and prevent app breakage
    try:
        # Retrieve the data submitted in the form
        data = request.form['data']
        
        # Encrypt the data using the cipher suite
        encrypted_data = cipher_suite.encrypt(data.encode())
        
        # Render the result.html template with the encrypted data
        # Decode the encrypted data from bytes to string for rendering
        return render_template('result.html', result=encrypted_data.decode())
    except Exception as x:
        # If an error occurs, render an error template with the error message
        error_message = "An error Occured"
        return render_template('error.html', error_message=error_message)

# page rendering for decryption
@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        # Retrieve the encrypted data submitted in the form
        data = request.form['data']
        
        # Decrypt the data using the cipher suite
        decrypted_data = cipher_suite.decrypt(data.encode())
        
        # Render the result.html template with the decrypted data
        # Decode the decrypted data from bytes to string for rendering
        return render_template('result.html', result=decrypted_data.decode())
    except Exception as x:
        # If an error occurs, render an error template with the error message
        print(x)
        # If an error occurs, redirect back to the index page with the error message as a query parameter
        error_message = "Wrong Key For Decryption"
        return redirect(url_for('index', error_message=error_message))

if __name__ == '__main__':
    app.run(debug=True)
