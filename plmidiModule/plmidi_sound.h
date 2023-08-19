#pragma once

#define PY_SSIZE_T_CLEAN  /* Make "s#" use Py_ssize_t rather than int. */
#include <Python.h>
#undef PY_SSIZE_T_CLEAN
#include <signal.h> /* Press ctrl+C to exit */
#include <Windows.h>
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")

#define PLMIDI_INIT_NOERROR 1
#define GET_ATTR(val, str) \
    PyLong_AsLong(PyObject_GetAttrString(val, str))

static int8_t plmidi_initflag = 0; // -1: fail, 0: ready to init, 1: success initialized

// plmidiInitError
PyObject *plmidiExc_InitErr = NULL;

// if Ctrl+C, then exit
static void plmidi_exit(int signal)
{
    if (signal == SIGINT) {
        Py_Exit(0);
    }
}

// Input -> piece: mido.MidiTrack, tempo: int
PyObject* plmidi_sound(PyObject *self, PyObject *args)
{
    // check inputs and init
    PyObject *piece; // a python list
    long tempo;
    if (!PyArg_ParseTuple(args, "Ol", &piece, &tempo)) {
        PyErr_SetString(PyExc_TypeError, "input type must be an integer or plmidi setup fail");
        return NULL;
    }

    // init midi player
    HMIDIOUT handle;
    if (plmidi_initflag == 0) 
    {
        if (midiOutOpen(&handle, MIDI_MAPPER, 0, 0, CALLBACK_NULL) != MMSYSERR_NOERROR) {
            plmidi_initflag = -1;
        } else {
            plmidi_initflag = 1;
        }
    }
    if (plmidi_initflag == -1) {
        PyErr_SetString(plmidiExc_InitErr, "init midi player fail");
    }

    // init exit
    signal(SIGINT, plmidi_exit);

    // main loop
    for (Py_ssize_t i = 0; i < PyList_Size(piece); ++i)
    {
        PyObject *msg = PyList_GetItem(piece, i);
        const char *msg_type = PyUnicode_AsUTF8(PyObject_GetAttrString(msg, "type"));

        // sound midi
        if (strcmp(msg_type, "program_change") == 0) {
            midiOutShortMsg(handle, GET_ATTR(msg, "program") << 8 | 0xC0 + GET_ATTR(msg, "channel"));
        } else if (strcmp(msg_type, "note_on") == 0) {
            midiOutShortMsg(handle, GET_ATTR(msg, "velocity") << 16 | GET_ATTR(msg, "note") << 8 | 0x90 + GET_ATTR(msg, "channel"));
        } else if (strcmp(msg_type, "note_off") == 0) {
            midiOutShortMsg(handle, GET_ATTR(msg, "velocity") << 16 | GET_ATTR(msg, "note") << 8 | 0x80 + GET_ATTR(msg, "channel"));
        }
        Sleep(GET_ATTR(msg, "time") * tempo / 500'000); 
    }

    midiOutClose(handle);
    Py_RETURN_NONE;
}

#undef GET_ATTR