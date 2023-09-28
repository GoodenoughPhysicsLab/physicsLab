#if !defined(_MSC_VER) || !defined(_WIN32)
#   error "This code must be compiled with MSVC on Windows"
#endif

#include "pybind11/pybind11.h"
#include "plmidi_sound.hpp"

static PyMethodDef plmidi_methods[] = {
    {"sound", _plmidi::sound, METH_VARARGS, "sound midi by using plmidi"},
    {"sound_by_midiOutShortMsg", _plmidi::sound_by_midiOutShortMsg, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef plmidi = {
    PyModuleDef_HEAD_INIT,
    "plmidi",
    NULL, /* doc */
    -1,   /* size of per-interpreter state of the module,
             or -1 if the module keeps state in global variables. */
    plmidi_methods
};

PyMODINIT_FUNC
PyInit_plmidi(void)
{
    PyObject *py_module = PyModule_Create(&plmidi);
    plmidiExc_InitErr = PyErr_NewException("plmidi.plmidiInitError", NULL, NULL);
    Py_XINCREF(plmidiExc_InitErr);
    if (PyModule_AddObject(py_module, "plmidiInitError", plmidiExc_InitErr) < 0) {
        Py_XDECREF(plmidiExc_InitErr);
        Py_CLEAR(plmidiExc_InitErr);
        Py_DECREF(py_module);
        return NULL;
    }

    return py_module? py_module: NULL;
}