#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>

#include "account.h"
#include "func.h"
#include "security.h"

namespace py = pybind11;

PYBIND11_MODULE(bindings,m)
{
        // Account.h bindings
        py::class_<Account>(m, "Account")
                .def(py::init<std::string, std::string, std::string>())
                .def(py::init<std::string, std::string, std::string, std::string>())
                .def("getCompany", &Account::getCompany)
                .def("getEmail", &Account::getEmail)
                .def("getPassword", &Account::getPassword)
                .def("getName", &Account::getName)
                .def("setCompany", &Account::setCompany)
                .def("setEmail", &Account::setEmail)
                .def("setPassword", &Account::setPassword)
                .def("setName", &Account::setName);

        // func.h bindings
        m.def("loadAccounts", &loadAccounts);
        m.def("addAccount", &addAccount);
        m.def("removeAccount", &removeAccount);
        m.def("getAccount", &getAccount);
        m.def("updateAccount", &updateAccount);
        m.def("saveAccounts", &saveAccounts);

        // security.h bindings
        m.def("createKey", &createKey);
        m.def("encryptString", &encryptString);
        m.def("decryptString", &decryptString);
        m.def("binaryToHex", &binaryToHex);
        m.def("hexToBinary", &hexToBinary);
        m.def("handleErrors", &handleErrors);
        m.def("validatePin", &validatePin);
        m.def("getKey", &getKey);
}