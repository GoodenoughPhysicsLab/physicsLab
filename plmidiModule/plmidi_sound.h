#pragma once

#pragma comment(lib, "winmm.lib")

#define PY_SSIZE_T_CLEAN  /* Make "s#" use Py_ssize_t rather than int. */
#include <Python.h>
#undef PY_SSIZE_T_CLEAN
#include <signal.h> /* Press ctrl+C to exit */
#include <Windows.h>
#include <mmsystem.h>

#define PLMIDI_INIT_NOERROR 1
#define PLMIDI_DO_NOT_INIT 0
#define PLMIDI_INIT_ERROR -1

#define GET_ATTR(val, str) \
    PyLong_AsLong(PyObject_GetAttrString(val, str))
#define GET_BYTES_ITEM(val, item) \
    (BYTE)PyLong_AsLong(PyList_GetItem(val, item))    

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

// Input -> piece: mido.MidiTrack
PyObject* plmidi_sound(PyObject *self, PyObject *args)
{
    // check inputs and init
    PyObject *piece; // type: mido.MidiTrack
    if (!PyArg_ParseTuple(args, "O", &piece)) {
        PyErr_SetString(PyExc_TypeError, NULL);
        return NULL;
    }
    if (!PyList_Check(piece)) {
        PyErr_SetString(PyExc_TypeError, "Input must be a python list");
    }

    // init midi player
    HMIDIOUT handle;
    if (plmidi_initflag == PLMIDI_DO_NOT_INIT) 
    {
        if (midiOutOpen(&handle, MIDI_MAPPER, 0, 0, CALLBACK_NULL) != MMSYSERR_NOERROR) {
            plmidi_initflag = PLMIDI_INIT_ERROR;
        } else {
            plmidi_initflag = PLMIDI_INIT_NOERROR;
        }
    }
    if (plmidi_initflag == PLMIDI_INIT_ERROR) {
        PyErr_SetString(plmidiExc_InitErr, "init midi player fail");
    }
    MIDIHDR midiHeader;
    ZeroMemory(&midiHeader, sizeof(MIDIHDR));

    // init Ctrl+C to exit
    signal(SIGINT, plmidi_exit);

    /* 
     * The reason why midiOutShortMsg is not used is because it is asynchronous,
     * which can cause short notes to not be played
     * However, midi message "program_change" still use midiOutShortMsg,
     * I can hardly understand it can not work when I use midiOutLongMsg
     */
    double tempo = 500'000;
    for (Py_ssize_t i = 0; i < PyList_Size(piece); i++)
    {
        PyObject *msg = PyList_GetItem(piece, i);
        PyObject *bytes = PyObject_CallMethod(msg, "bytes", NULL);
        const char *msg_type = PyUnicode_AsUTF8(PyObject_GetAttrString(msg, "type"));

        // sound midi
        if (strcmp(msg_type, "program_change") == 0) {
            midiOutShortMsg(handle, GET_ATTR(msg, "program") << 8 | 0xC0 + GET_ATTR(msg, "channel"));
        }
        else if (strcmp(msg_type, "note_on") == 0)
        {
            BYTE msg_bytes[] = { GET_BYTES_ITEM(bytes, 0), GET_BYTES_ITEM(bytes, 1), GET_BYTES_ITEM(bytes, 2) };

            midiHeader.lpData = (LPSTR)&msg_bytes;
            midiHeader.dwBufferLength = sizeof(msg_bytes);
            if (midiOutPrepareHeader(handle, &midiHeader, sizeof(MIDIHDR)) != MMSYSERR_NOERROR) {
                PyErr_SetString(plmidiExc_InitErr, NULL);
            }
            midiOutLongMsg(handle, &midiHeader, (UINT)sizeof(MIDIHDR));
        }
        else if (strcmp(msg_type, "note_off") == 0)
        {
            BYTE msg_bytes[] = { GET_BYTES_ITEM(bytes, 0), GET_BYTES_ITEM(bytes, 1), GET_BYTES_ITEM(bytes, 2) };

            midiHeader.lpData = (LPSTR)&msg_bytes;
            midiHeader.dwBufferLength = sizeof(msg_bytes);
            if (midiOutPrepareHeader(handle, &midiHeader, sizeof(MIDIHDR)) != MMSYSERR_NOERROR) {
                PyErr_SetString(plmidiExc_InitErr, NULL);
            }
            midiOutLongMsg(handle, &midiHeader, (UINT)sizeof(MIDIHDR));
        }
        else if (strcmp(msg_type, "set_tempo") == 0) {
            tempo = (double)GET_ATTR(msg, "tempo");
        }
        Sleep(GET_ATTR(msg, "time") * tempo / 500'000);
    }

    midiOutUnprepareHeader(handle, &midiHeader, sizeof(MIDIHDR));
    midiOutClose(handle);
    Py_RETURN_NONE;
}

#undef GET_ATTR
#undef GET_ITEM