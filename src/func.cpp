#include "func.h"

#include <string>
#include <iostream>
#include <vector>
#include <iterator>
#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

vector<Account> loadAccounts(const string& key,const string& filePath)
{
        // Create json file if it does not exist
        ifstream in(filePath);
        if (!in.is_open())
        {
                ofstream out(filePath);
                out.close();
                return vector<Account>();
        }

        // Load accounts from json file
        vector<Account> accounts;
        
        // Check if the file is empty
        in.seekg(0, ios::end);
        if (in.tellg() == 0)
        {
                in.close();
                return accounts;
        }
        in.seekg(0, ios::beg);

        json j = json::parse(in);
        
        for (size_t i = 0; i < j.size(); i++)
        {
                string company = decryptString(j[i]["company"], key);
                string email = decryptString(j[i]["email"], key);
                string password = decryptString(j[i]["password"], key);
                string name = decryptString(j[i]["name"], key);
                accounts.push_back(Account(company, email, password, name));
        }

        in.close();
        return accounts;
}

int verifyAccount(const Account& account, vector<Account>& accounts)
{
        // Check if the email is less than 100 characters and does not contain (" ")
        if (account.getEmail().length() > 100 || account.getEmail().find('"') != string::npos)
        {
                return 2;// Invalid email
        }

        // Check if the password is less than 100 characters and does not contain (" ")
        if (account.getPassword().length() > 100 || account.getPassword().find('"') != string::npos)
        {
                return 3;// Invalid password
        }

        // Check if the company is less than 100 characters and does not contain (" ")
        if (account.getCompany().length() > 100 || account.getCompany().find('"') != string::npos)
        {
                return 4;// Invalid company
        }

        // Check if the name is less than 100 characters and does not contain (" ")
        if (account.getName().length() > 100 || account.getName().find('"') != string::npos)
        {
                return 5;// Invalid name
        }

        // Check if the account already exists based on email and company
        for (Account& acc : accounts)
        {
                if (acc.getEmail() == account.getEmail() && acc.getCompany() == account.getCompany())
                {
                        return 1;// Account already exists
                }
        }

        return 0;// Account is valid
}

Account getAccount(string email, string company, vector<Account>& accounts)
{
        // Get the account with the given email and company
        for (Account& acc : accounts)
        {
                if (acc.getEmail() == email && acc.getCompany() == company)
                {
                        return acc;
                }
        }

        // Return an empty account if not found
        return  Account("", "", "");
}

void saveAccounts(const vector<Account>& accounts, const string& key, const string& filePath)
{
        // Save accounts to json file
        json j;
        for (size_t i = 0; i < accounts.size(); i++)
        {
                j[i]["company"] = encryptString(accounts[i].getCompany(), key);
                j[i]["email"] = encryptString(accounts[i].getEmail(), key);
                j[i]["password"] = encryptString(accounts[i].getPassword(), key);
                j[i]["name"] = encryptString(accounts[i].getName(), key);
        }

        ofstream out(filePath);
        out << j.dump(4);
        out.close();
}