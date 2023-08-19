#include "plmidi_sound.h"

static PyMethodDef plmidi_methods[] = {
    {"sound", plmidi_sound, METH_VARARGS, "sound midi by using plmidi"},
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
    PyObject *module = PyModule_Create(&plmidi);
    plmidiExc_InitErr = PyErr_NewException("plmidi.plmidiInitError", NULL, NULL);
    Py_XINCREF(plmidiExc_InitErr);
    if (PyModule_AddObject(module, "plmidiInitError", plmidiExc_InitErr) < 0) {
        Py_XDECREF(plmidiExc_InitErr);
        Py_CLEAR(plmidiExc_InitErr);
        Py_DECREF(module);
        return NULL;
    }

    return module? module: NULL;
}