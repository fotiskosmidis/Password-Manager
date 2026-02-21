#ifndef FUNC_H
#define FUNC_H

#include "account.h"
#include "security.h"

#include <string>
#include <iostream>
#include <vector>

using namespace std;

// function declarations
vector<Account> loadAccounts(const string& key, const string& filePath);
int verifyAccount(const Account& account, vector<Account>& accounts);
Account getAccount(string email, string company, vector<Account>& accounts);
void saveAccounts(const vector<Account>& accounts, const string& key, const string& filePath);

#endif // FUNC_H