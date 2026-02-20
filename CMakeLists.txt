cmake_minimum_required(VERSION 3.23)

project(PasswordManager LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find dependencies
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(OpenSSL REQUIRED)

# Add source files
set(SOURCES
    src/bindings.cpp
    src/account.cpp
    src/func.cpp
    src/security.cpp
)

# Create the Python module
pybind11_add_module(bindings ${SOURCES})

# Include directories for your headers
target_include_directories(bindings PRIVATE src)

# Link libraries
target_link_libraries(bindings
    PRIVATE
        pybind11::module
        nlohmann_json::nlohmann_json
        OpenSSL::Crypto
)

# Optionally, print status messages for user
message(STATUS "Python3 include dirs: ${Python3_INCLUDE_DIRS}")
message(STATUS "pybind11 found: ${pybind11_FOUND}")
message(STATUS "nlohmann_json found: ${nlohmann_json_FOUND}")
message(STATUS "OpenSSL found: ${OPENSSL_FOUND}")

# Set output directory and prefix for the library
set_target_properties(bindings PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}"
    PREFIX ""  # Ensures no 'lib' prefix
)

