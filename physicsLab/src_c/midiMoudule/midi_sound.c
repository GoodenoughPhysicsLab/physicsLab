#include <Python.h>
#include <Windows.h>
#include <mmsystem.h>

// input: [(待确定), ()...]
static PyObject* 
midi_sound(PyObject *self, PyObject *args)
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


static PyMethodDef midi_methods[] = {
    {"midi_sound", midi_sound, METH_VARARGS, "play midi by using C"},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef midi = {
    PyModuleDef_HEAD_INIT,
    "midi",
    NULL,
    -1,
    midi_methods
};

PyMODINIT_FUNC
PyInit_midi(void)
{
    PyObject* m = PyModule_Create(&midi);
    if (!m) {
        return NULL;
    }
    return m;
}
