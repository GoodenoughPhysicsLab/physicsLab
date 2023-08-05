#include <Python.h>
#include "plmidi_sound.h"
#include "plmidi_playWindows.h"

static PyMethodDef plmidi_methods[] = {
    {"sound", plmidi_sound, METH_VARARGS, "sound midi by using C"},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef plmidi = {
    PyModuleDef_HEAD_INIT,
    "plmidi",
    NULL,
    -1,
    plmidi_methods
};

PyMODINIT_FUNC
PyInit_plmidi(void)
{
    PyObject *m = PyModule_Create(&plmidi);
    if (!m) {
        return NULL;
    }
    return m;
}