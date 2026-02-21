#ifndef SECURITY_H
#define SECURITY_H

#include <string>

using namespace std;

// Hashing the application password using SHA-256 and making it the key
string createKey(const string& passwd, const string& filePath);

// Encrypting the string using the key and AES-256 encryption
string encryptString(const string& text, const string& key);

// Decrypting the string using the key and AES-256 decryption
string decryptString(const string& encryptText, const string& key);

// Binary to hexadecimal conversion
string binaryToHex(unsigned char* binary, int length);

// Hexadecimal to binary conversion
unsigned char* hexToBinary(const string& hex);

// Printing OpenSSL errors
void handleErrors();

// Pin validation function
bool validatePin(const string& pin, const string& filePath);

// Getting the key from the settings file
string getKey(const string& filePath);

#endif // SECURITY_H