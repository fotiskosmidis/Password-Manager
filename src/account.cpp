#include "account.h"
#include <string>

using namespace std;

Account::Account(string company, string email, string password)
{
        this->company = company;
        this->email = email;
        this->password = password;
        this->name = "";
}

Account::Account(string company, string email, string password, string name)
{
        this->company = company;
        this->email = email;
        this->password = password;
        this->name = name;
}

string Account::getCompany() const
{
        return company;
}

string Account::getEmail() const
{
        return email;
}

string Account::getPassword() const
{
        return password;
}

string Account::getName() const
{
        return name;
}

void Account::setCompany(string company)
{
        this->company = company;
}

void Account::setEmail(string email)
{
        this->email = email;
}

void Account::setPassword(string password)
{
        this->password = password;
}

void Account::setName(string name)
{
        this->name = name;
}