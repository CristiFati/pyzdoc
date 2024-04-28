#include <Windows.h>

#define ZDOC_EXPORTS
#include "zdoc.h"

#define SENTINEL 0x80000000


static CRITICAL_SECTION _func, _cb;
static HHOOK _hook = NULL;
static int _x = 0;
static int _y = 0;
static DWORD _tid = 0;

static LRESULT CALLBACK _hookFunc(int nCode, WPARAM wParam, LPARAM lParam)
{
    if (nCode < 0) {
        return CallNextHookEx(NULL, nCode, wParam, lParam);
    }
    switch (nCode) {
        case HCBT_CREATEWND: {
            EnterCriticalSection(&_cb);
            if (_tid == GetCurrentThreadId()) {
                LPCBT_CREATEWNDW pcw = (LPCBT_CREATEWNDW)lParam;
                if (pcw) {
                    LPCREATESTRUCTW pcs = pcw->lpcs;
                    if (pcs) {
                        if (_x != SENTINEL) {
                            pcs->x = _x;
                        }
                        if (_y != SENTINEL) {
                            pcs->y = _y;
                        }
                        if (_hook) {
                            UnhookWindowsHook(WH_CBT, _hookFunc);
                            _hook = NULL;
                        }

                    }
                }
            }
            LeaveCriticalSection(&_cb);
            break;
        }
        default: {
            break;
        }
    }
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

int MessageBoxXY(HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, UINT uType, int x, int y)
{
    int ret = 0;
    EnterCriticalSection(&_func);
    _x = x;
    _y = y;
    _tid = GetCurrentThreadId();
    _hook = SetWindowsHookExW(WH_CBT, _hookFunc, 0, _tid);
    ret = MessageBoxW(hWnd, lpText, lpCaption, uType);
    LeaveCriticalSection(&_func);
    return ret;
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    // Perform actions based on the reason for calling.
    switch (fdwReason)
    {
        case DLL_PROCESS_ATTACH: {
            // Initialize once for each new process.
            // Return FALSE to fail DLL load.
            InitializeCriticalSection(&_func);
            InitializeCriticalSection(&_cb);
            break;
        }
        case DLL_THREAD_ATTACH: {
            // Do thread-specific initialization.
            break;
        }
        case DLL_THREAD_DETACH: {
            // Do thread-specific cleanup.
            break;
        }
        case DLL_PROCESS_DETACH: {

            if (lpvReserved != NULL)
            {
                break; // do not do cleanup if process termination scenario
            }
            DeleteCriticalSection(&_cb);
            DeleteCriticalSection(&_func);
            // Perform any necessary cleanup.
            break;
        }
        default: {
            break;
        }
    }
    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}

