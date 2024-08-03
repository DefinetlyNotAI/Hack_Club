#include <iostream>
#include <comdef.h>
#include <Wbemidl.h>

#pragma comment(lib, "wbemuuid.lib")

int main() {
    HRESULT hres;

    // Initialize COM.
    hres = CoInitializeEx(0, COINIT_MULTITHREADED);
    if (FAILED(hres)) {
        std::cout << "Failed to initialize COM library. Error code = 0x" << std::hex << hres << std::endl;
        return 1; // Program has failed.
    }

    // Set general COM security levels.
    hres = CoInitializeSecurity(
        NULL,
        -1,                          // COM negotiates service
        NULL,                        // Authentication services
        NULL,                        // Reserved
        RPC_C_AUTHN_LEVEL_DEFAULT,   // Default authentication
        RPC_C_IMP_LEVEL_IMPERSONATE, // Default Impersonation
        NULL,                        // Authentication info
        EOAC_NONE,                   // Additional capabilities
        NULL                         // Reserved
    );

    if (FAILED(hres)) {
        std::cout << "Failed to initialize security. Error code = 0x" << std::hex << hres << std::endl;
        CoUninitialize();
        return 1; // Program has failed.
    }

    // Declare pLoc and pSvc here
    IWbemLocator *pLoc = NULL;
    IWbemServices *pSvc = NULL;

    // Create an instance of WbemLocator to connect to WMI through
    hres = CoCreateInstance(
        CLSID_WbemLocator,
        0,
        CLSCTX_INPROC_SERVER,
        IID_IWbemLocator, (LPVOID *)&pLoc);

    if (FAILED(hres)) {
        std::cout << "Failed to create IWbemLocator object. Error code = 0x" << std::hex << hres << std::endl;
        CoUninitialize();
        return 1; // Program has failed.
    }

    // Connect to the root\cimv2 namespace with the current user.
    hres = pLoc->ConnectServer(
        _bstr_t(L"ROOT\\CIMV2"), // Object path of WMI namespace
        NULL,                    // User name
        NULL,                    // User password
        0,                       // Locale
        0,                       // Security flags
        0,                       // Authority
        0,                       // Context object
        &pSvc                     // pointer to IWbemServices proxy
    );

    if (FAILED(hres)) {
        std::cout << "Could not connect. Error code = 0x" << std::hex << hres << std::endl;
        pLoc->Release();
        CoUninitialize();
        return 1; // Program has failed.
    }

    std::cout << "Connected to ROOT\\CIMV2 WMI namespace" << std::endl;

    // Cleanup
    pSvc->Release();
    pLoc->Release();
    CoUninitialize();

    return 0; // Program successfully completed.
}
