#ifndef FUNC_H
#define FUNC_H

#include "account.h"
#include "security.h"

#include <string>
#include <iostream>
#include <vector>

using namespace std;

// function declarations
vector<Account> loadAccounts(const string& key);
bool addAccount(const Account& account, vector<Account>& accounts);
void removeAccount(string email, string company, vector<Account>& accounts);
Account getAccount(string email, string company, vector<Account>& accounts);
bool updateAccount(Account& account, vector<Account>& accounts);
void saveAccounts(const vector<Account>& accounts, const string& key);

#endif // FUNC_H