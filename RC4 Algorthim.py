# Key Scheduling Algorithm
def generate_key_schedule(key):
    schedule = [i for i in range(256)]  # Initialize schedule with values from 0 to 255
    
    index = 0
    for j in range(256):
        index = (index + schedule[j] + key[j % len(key)]) % 256
        
        # Swap values at positions j and index
        temp = schedule[j]
        schedule[j] = schedule[index]
        schedule[index] = temp
        
    return schedule

# Stream Generation Algorithm
def generate_stream(schedule):
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (schedule[i] + j) % 256
        
        # Swap values at positions i and j
        temp = schedule[j]
        schedule[j] = schedule[i]
        schedule[i] = temp
        
        yield schedule[(schedule[i] + schedule[j]) % 256]

# Encryption Function
def encrypt_text(plain_text, key):
    plain_text = [ord(char) for char in plain_text]  # Convert characters to ASCII values
    key = [ord(char) for char in key]
    
    schedule = generate_key_schedule(key)
    stream_generator = generate_stream(schedule)
    
    cipher_text = ''
    for char in plain_text:
        encrypted_char = char ^ next(stream_generator)  # XOR operation with key stream
        cipher_text += str(hex(encrypted_char))[2:].upper()  # Convert to hexadecimal and append to ciphertext
        
    return cipher_text

# Decryption Function
def decrypt_text(cipher_text, key):
    cipher_text = cipher_text.split('0X')[1:]  # Split ciphertext into individual hexadecimal values
    cipher_text = [int('0x' + c.lower(), 0) for c in cipher_text]  # Convert hex values to integers
    key = [ord(char) for char in key]
    
    schedule = generate_key_schedule(key)
    stream_generator = generate_stream(schedule)
    
    plain_text = ''
    for char in cipher_text:
        decrypted_char = char ^ next(stream_generator)  # XOR operation with key stream
        plain_text += chr(decrypted_char)  # Convert ASCII value to character and append to plaintext
        
    return plain_text

# Main Function
if __name__ == '__main__':
    choice = input('Enter 1 for Encrypt, or 2 for Decrypt: ').upper()
    if choice == '1':
        print('----Encryption----')
        plain_text = input('Enter your plaintext: ')
        key = input('Enter your secret key: ')
        result = encrypt_text(plain_text, key)
        print('Encrypted Result: ')
        print(result)
    elif choice == '2': 
        print('----Decryption----')
        cipher_text = input('Enter your ciphertext: ')
        key = input('Enter your secret key: ')
        result = decrypt_text(cipher_text, key)
        print('Decrypted Result: ')
        print(result)
    else:
        print('Enter specified characters for Encrypt & Decrypt')
