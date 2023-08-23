#pragma once

#pragma comment(lib, "winmm.lib")
#pragma comment(lib, "User32.lib")

#define PY_SSIZE_T_CLEAN  /* Make "s#" use Py_ssize_t rather than int. */
#include <Python.h>
#undef PY_SSIZE_T_CLEAN
#include <signal.h> /* Press ctrl+C to exit */
#include <Windows.h>
#include <mmsystem.h>

static LRESULT CALLBACK WndProc(HWND hwnd, UINT uint, WPARAM wparam, LPARAM plaram) {}

PyObject* windowsPlayer(PyObject *self, PyObject *args)
{
	Py_RETURN_NONE;
}