#pragma once

#if defined(_WIN32)
#  if defined(ZDOC_STATIC)
#    define ZDOC_EXPORT_API
#  else  // ZDOC_STATIC
#    if defined(ZDOC_EXPORTS)
#      define ZDOC_EXPORT_API __declspec(dllexport)
#    else  // ZDOC_EXPORTS
#      define ZDOC_EXPORT_API __declspec(dllimport)
#    endif  // ZDOC_EXPORTS
#  endif  // ZDOC_STATIC
#else  // _WIN32
#  define ZDOC_EXPORT_API
#endif  // _WIN32

#if defined(_WIN32)
#  include <Windows.h>
#else  // _WIN32
#endif  // _WIN32

#if defined(__cplusplus)
extern "C" {
#endif  // __cplusplus

#  if defined(_WIN32)

ZDOC_EXPORT_API int MessageBoxXY(HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, UINT uType, int x, int y);
ZDOC_EXPORT_API int clearHooks();

#  else  // _WIN32
#  endif  // _WIN32

#if defined(__cplusplus)
}
#endif  // __cplusplus

