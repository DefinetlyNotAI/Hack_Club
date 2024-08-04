#include <iostream>
#include <fstream>
#include <Windows.h>

typedef void (*GetSystemInfoFunc)();

BOOL APIENTRY DllMain(HMODULE hModule, DWORD reason, LPVOID reserved, GetSystemInfoFunc getSystemInfo) {
    switch (reason) {
    case DLL_PROCESS_ATTACH:
        if (getSystemInfo != nullptr) {
            getSystemInfo();
        }
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

int main() {
    HINSTANCE hInst = LoadLibrary(TEXT("wmi_query.dll"));
    if (hInst == NULL) {
        std::cerr << "Failed to load wmi_query.dll" << std::endl;
        return 1;
    }

    GetSystemInfoFunc getSystemInfo = (GetSystemInfoFunc)GetProcAddress(hInst, "getSystemInfo");
    if (getSystemInfo == nullptr) {
        std::cerr << "Failed to get address of getSystemInfo" << std::endl;
        FreeLibrary(hInst);
        return 1;
    }

    DllMain(hInst, DLL_PROCESS_ATTACH, NULL, getSystemInfo);

    std::ofstream outputFile("system_info.txt");
    if (!outputFile.is_open()) {
        std::cerr << "Failed to open system_info.txt for writing" << std::endl;
        FreeLibrary(hInst);
        return 1;
    }

    outputFile << "System Information Retrieved Successfully" << std::endl;

    outputFile.close();
    FreeLibrary(hInst);

    return 0;
}
