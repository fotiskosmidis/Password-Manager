#ifndef ACCOUNT_H
#define ACCOUNT_H

#include <string>

using namespace std;

// define the class account
class Account
{
private:
        // name sometimes can be empty
        string company; 
        string email;
        string password;
        string name;
public:
        Account(string company, string email, string password);
        Account(string company, string email, string password, string name);
        
        // getter functions
        string getCompany() const;
        string getEmail() const;
        string getPassword() const;
        string getName() const;

        // setter functions
        void setCompany(string company);
        void setEmail(string email);
        void setPassword(string password);
        void setName(string name);
};
#endif // ACCOUNT_H