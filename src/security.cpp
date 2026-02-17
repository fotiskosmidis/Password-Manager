#include "security.h"

#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>
#include <cstring>
#include <fstream>

// Libraries for hashing, encryption, error handling, and random number generation
#include <openssl/sha.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/rand.h>

using namespace std;

string createKey(const string& passwd) 
{
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256((unsigned char*)passwd.c_str(), passwd.size(), hash);
        string key= binaryToHex(hash, SHA256_DIGEST_LENGTH);
        
        // Create a JSON file to store the key
        ofstream keyFile("DBfiles/settings.json");
        string jsonString = R"({"key": ")" + key + R"("})";
        keyFile << jsonString;
        keyFile.close();
        return key;
}

string encryptString(const string& text, const string& key)
{
        // Convert the key from hex to binary
        unsigned char* binaryKey = hexToBinary(key);
        // Convert the text to binary
        unsigned char* binaryText = (unsigned char*)text.c_str();
        int textLength = text.size();

        // Generate a random initialization vector (IV)
        unsigned char iv[16];
        RAND_bytes(iv, sizeof(iv));

        // Create a cipher text buffer
        unsigned char cipherText[128];

        // Create and initialize the context
        EVP_CIPHER_CTX* ctx ;
        if(!(ctx = EVP_CIPHER_CTX_new()))
                handleErrors();

        // Initialize the encryption operation
        if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, binaryKey, iv))
                handleErrors();

        // Encrypt the binary text
        int tempLength;
        if(1 != EVP_EncryptUpdate(ctx, cipherText, &tempLength, binaryText, textLength))
                handleErrors();
        int cipherTextLength = tempLength;

        // Finalize the encryption
        if(1 != EVP_EncryptFinal_ex(ctx, cipherText + tempLength, &tempLength))
                handleErrors();
        cipherTextLength += tempLength;

        // Clean up
        EVP_CIPHER_CTX_free(ctx);
        // Free the binary key
        delete[] binaryKey;

        // Store the IV at the beginning of the cipher text
        unsigned char finalCipherText[144];
        memcpy(finalCipherText, iv, 16);
        memcpy(finalCipherText + 16, cipherText, cipherTextLength);
        cipherTextLength += 16;

        string encryptedText = binaryToHex(finalCipherText, cipherTextLength);
        return encryptedText;
}

string decryptString(const string& encryptedText, const string& key)
{
        // Convert the key from hex to binary
        unsigned char* binaryKey = hexToBinary(key);
        // Convert the encrypted text to binary
        unsigned char* binaryEncryptedText = hexToBinary(encryptedText);
        int encryptedTextLength = encryptedText.size() / 2;

        // Extract the IV from the beginning of the encrypted text
        unsigned char iv[16];
        memcpy(iv, binaryEncryptedText, 16);

        // Create a buffer for the decrypted text
        unsigned char decryptedText[128];

        // Create and initialize the context
        EVP_CIPHER_CTX* ctx ;
        if(!(ctx = EVP_CIPHER_CTX_new()))
                handleErrors();

        // Initialize the decryption operation
        if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, binaryKey, iv))
                handleErrors();

        // Decrypt the binary encrypted text (excluding the IV)
        int tempLength;
        if(1 != EVP_DecryptUpdate(ctx, decryptedText, &tempLength, binaryEncryptedText + 16, encryptedTextLength - 16))
                handleErrors();
        int decryptedTextLength = tempLength;

        // Finalize the decryption
        if(1 != EVP_DecryptFinal_ex(ctx, decryptedText + tempLength, &tempLength))
                handleErrors();
        decryptedTextLength += tempLength;

        // Clean up
        EVP_CIPHER_CTX_free(ctx);
        // Free the binary key and encrypted text
        delete[] binaryKey;
        delete[] binaryEncryptedText;

        string decryptedString((char*)decryptedText, decryptedTextLength);
        return decryptedString;
}

string binaryToHex(unsigned char* binary,  int length)
{
        stringstream ss;
        for (int i = 0; i < length; i++)
        {
                ss << hex << setfill('0') << setw(2) << (int)binary[i];
        }
        return ss.str();
}

unsigned char* hexToBinary(const string& hex)
{
        unsigned char* binary = new unsigned char[hex.length() / 2];
        for (size_t i = 0; i < hex.length(); i += 2)
        {
                string byteStr = hex.substr(i, 2);
                binary[i / 2] = (unsigned char)strtol(byteStr.c_str(), nullptr, 16);
        }
        return binary;
}

void handleErrors()
{
        ERR_print_errors_fp(stderr);
        abort();
}

bool validatePin(const string& pin)
{
        bool flag = false;

        string key = getKey();
        // Hash the provided PIN and compare
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256((unsigned char*)pin.c_str(), pin.size(), hash);
        string pinHash = binaryToHex(hash, SHA256_DIGEST_LENGTH);

        flag = (pinHash == key);

        return flag;
}

string getKey()
{
        ifstream keyFile("DBfiles/settings.json");
        string key;
        if (keyFile.is_open())
        {
                string line;
                getline(keyFile, line);
                keyFile.close();
                
                // Extract key value from JSON
                size_t keyPos = 9;
                size_t endPos = 73;
                key = line.substr(keyPos, endPos - keyPos);
        }
        return key;
}