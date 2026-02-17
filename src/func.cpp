#include "func.h"

#include <string>
#include <iostream>
#include <vector>
#include <iterator>
#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

vector<Account> loadAccounts(const string& key)
{
        // Create json file if it does not exist
        ifstream in("DBfiles/accounts.json");
        if (!in.is_open())
        {
                ofstream out("DBfiles/accounts.json");
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

bool addAccount(const Account& account, vector<Account>& accounts)
{
        // Check if the account already exists based on email and company
        for (Account& acc : accounts)
        {
                if (acc.getEmail() == account.getEmail() && acc.getCompany() == account.getCompany())
                {
                        cout << "Account already exists!" << endl;
                        return false;
                }
        }

        // Check if the email is less than 100 characters and does not contain (" ")
        if (account.getEmail().length() > 100 || account.getEmail().find('"') != string::npos)
        {
                cout << "Invalid email!" << endl;
                return false;
        }

        // Check if the password is less than 100 characters and does not contain (" ")
        if (account.getPassword().length() > 100 || account.getPassword().find('"') != string::npos)
        {                cout << "Invalid password!" << endl;
                return false;
        }

        // Check if the company is less than 100 characters and does not contain (" ")
        if (account.getCompany().length() > 100 || account.getCompany().find('"') != string::npos)
        {                cout << "Invalid company!" << endl;
                return false;
        }

        // Check if the name is less than 100 characters and does not contain (" ")
        if (account.getName().length() > 100 || account.getName().find('"') != string::npos)
        {                cout << "Invalid name!" << endl;
                return false;
        }


        accounts.push_back(account);
        return true;
}

void removeAccount(string email, string company, vector<Account>& accounts)
{
        // Remove the account with the given email and company
        for (auto it = accounts.begin(); it != accounts.end(); ++it)
        {
                if (it->getEmail() == email && it->getCompany() == company)
                {
                        accounts.erase(it);
                        cout << "Account removed successfully!" << endl;
                        return;
                }
        }
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

bool updateAccount(Account& account, vector<Account>& accounts)
{
        // Check if the company is less than 100 characters and does not contain (" ")
        if (account.getCompany().length() > 100 || account.getCompany().find('"') != string::npos)
        {
                cout << "Invalid company!" << endl;
                return false;
        }

        // Check if the email is less than 100 characters and does not contain (" ")
        if (account.getEmail().length() > 100 || account.getEmail().find('"') != string::npos)
        {
                cout << "Invalid email!" << endl;
                return false;
        }

        // Check if the password is less than 100 characters and does not contain (" ")
        if (account.getPassword().length() > 100 || account.getPassword().find('"') != string::npos)
        {
                cout << "Invalid password!" << endl;
                return false;
        }

        // Check if the name is less than 100 characters and does not contain (" ")
        if (account.getName().length() > 100 || account.getName().find('"') != string::npos)
        {
                cout << "Invalid name!" << endl;
                return false;
        }

        for (Account& acc : accounts)
        {
                if (acc.getEmail() == account.getEmail() && acc.getCompany() == account.getCompany())
                {
                        acc.setCompany(account.getCompany());
                        acc.setEmail(account.getEmail());
                        acc.setPassword(account.getPassword());
                        acc.setName(account.getName());
                        cout << "Account updated successfully!" << endl;
                        return true;
                }
        }

        cout << "Account not found!" << endl;
        return false;
}

void saveAccounts(const vector<Account>& accounts, const string& key)
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

        ofstream out("DBfiles/accounts.json");
        out << j.dump(4);
        out.close();
}