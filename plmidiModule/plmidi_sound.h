#pragma once

#include <Python.h>
#include <Windows.h>
#include <mmsystem.h>

/*
 * Input: 
 *        type:     midi事件, 暂时只支持 note_on 与 note_off
 *        time:     间隔这么多时间之后执行该type
 *        note:     midi音高/音调
 *        velocity: midi音符的响度
 *        channel:  midi通道, 对应midi音色
 */
PyObject * 
plmidi_sound(PyObject *self, PyObject *args)
{
    PyObject *musiclist; // must be a python list
    if (!PyArg_ParseTuple(args, "O", &musiclist)) {
        PyErr_SetString(PyExc_TypeError, "");
        return NULL;
    }

    if (!PyList_Check(musiclist)) {
        PyErr_SetString(PyExc_TypeError, "");
        return NULL;
    }

    for (Py_ssize_t i = 0; i < PyList_Size(musiclist); ++i)
    {
        PyObject *message = PyList_GetItem(musiclist, i);
        //pass
    }
    Py_RETURN_NONE;
}
