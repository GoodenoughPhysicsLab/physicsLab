#include <Python.h>
#include <Windows.h>
#include <mmsystem.h>

// input: [(待确定), ()...]
static PyObject* 
plmidi_sound(PyObject *self, PyObject *args)
{
    PyObject *musiclist; // must be a python list
    if (!PyArg_ParseTuple(self, "O", &musiclist)) {
        PyErr_SetString(PyExc_TypeError, "");
    }

    if (!PyList_Check(musiclist)) {
        PyErr_SetString(PyExc_TypeError, "");
    }

    for (Py_ssize_t i = 0; i < PyList_Size(musiclist); ++i)
    {
        PyObject* message = PyList_GetItem(musiclist, i);
        //pass
    }
    Py_RETURN_NONE;
}


static PyMethodDef plmidi_methods[] = {
    {"midi_sound", plmidi_sound, METH_VARARGS, "play midi by using C"},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef plmidi = {
    PyModuleDef_HEAD_INIT,
    "midi",
    NULL,
    -1,
    plmidi_methods
};

PyMODINIT_FUNC
PyInit_plmidi(void)
{
    PyObject* m = PyModule_Create(&plmidi);
    if (!m) {
        return NULL;
    }
    return m;
}
