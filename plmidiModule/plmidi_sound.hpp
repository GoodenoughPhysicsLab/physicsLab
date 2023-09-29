#pragma once

#pragma comment(lib, "winmm.lib")

#include <ranges>
#include <vector>
#include <string>
#include <iostream>
#include <signal.h> /* Press ctrl+C to exit */
#include <Windows.h>
#include <mmsystem.h>

#include "pybind11/pybind11.h"

namespace py = pybind11;

#define PLMIDI_INIT_NOERROR 1
#define PLMIDI_DO_NOT_INIT 0
#define PLMIDI_INIT_ERROR -1

#define GET_ATTR(val, str) \
    PyLong_AsLong(PyObject_GetAttrString(val, str))
#define GET_BYTES_ITEM(val, item) \
    (BYTE)PyLong_AsLong(PyList_GetItem(val, item))    

static int8_t plmidi_initflag = 0; // -1: fail, 0: ready to init, 1: success initialized

// if Ctrl+C, then exit
static void plmidi_exit(int signal)
{
    if (signal == SIGINT) {
        Py_Exit(0);
    }
}

namespace _plmidi {

// plmidiInitError
struct plmidiExc_InitErr : public ::std::exception
{
    static constexpr ::std::string err_msg{"module plmidi init fail"};
    plmidiExc_InitErr() = default;
    ~plmidiExc_InitErr() = default;

    const char* what() const noexcept override {
        return err_msg.c_str();
    }
};

// developing
// Input -> piece: mido.MidiTrack
PyObject* sound(PyObject *self, PyObject *args)
{
    // check inputs and init
    PyObject *piece; // type: mido.MidiTrack
    if (!PyArg_ParseTuple(args, "O", &piece)) {
        throw py::type_error();
        return NULL;
    }
    if (!PyList_Check(piece)) {
        throw py::type_error("Input must be a python list");
        return NULL;
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
        throw plmidiExc_InitErr();
        return NULL;
    }

    // init Ctrl+C to exit
    signal(SIGINT, plmidi_exit);

    // create byte list
    ::std::vector<BYTE> notes{};
    for (auto _ : ::std::views::iota(0, PyList_Size(piece)))
    {
        PyObject *msg = PyList_GetItem(piece, _);
        PyObject *bytes = PyObject_CallMethod(msg, "bytes", NULL);
        for (auto i : ::std::views::iota(0, PyList_Size(bytes))) {
            notes.emplace_back(GET_BYTES_ITEM(bytes, i));
        }
    }
    if (notes.empty()) {
        ::std::cout << "notes is empty" << "\n";
        Py_Exit(0);
    }
 #ifdef PLMIDI_DEBUG
    // translate "unsigned char" to ::std::string
    // the reason do not use ::std::hex because some strange problem
    // the reason do not use printf("%X") because puts("\n") will give a new command to shell
    auto bytelist_to_hex = [] (::std::vector<BYTE>& num) -> ::std::string {
        ::std::string res{};
        int tick = 1;
        for (auto n : num) {
            unsigned char h_char = (n & 0xf0) >> 4;
            unsigned char l_char = n & 0xf;
            
            if (h_char >= 10) {
                h_char = 'A' + l_char - 10;
            } else {
                h_char += '0';
            }
            res += h_char;

            if (l_char >= 10) {
                l_char = 'A' + l_char - 10;
            } else {
                l_char += '0';
            }
            res += l_char, res += " ";

            if (tick == 15) {
                res += "\n", tick = 1;
            } else {
                tick++;
            }
        }
        res += '\n';

        return res;
    };

    ::std::cout << bytelist_to_hex(notes) << "\n";
 #endif // PLMIDI_DEBUG
    MIDIHDR midiHeader;
    ZeroMemory(&midiHeader, sizeof(MIDIHDR));

    BYTE *msg_bytes = (BYTE *)malloc(notes.size());
    ::std::memcpy(msg_bytes, &notes[0], notes.size());

    midiHeader.lpData = (LPSTR)&msg_bytes;
    midiHeader.dwBufferLength = sizeof(msg_bytes);
    if (midiOutPrepareHeader(handle, &midiHeader, sizeof(MIDIHDR)) != MMSYSERR_NOERROR) {
        throw plmidiExc_InitErr();
        return NULL;
    }
    midiOutLongMsg(handle, &midiHeader, (UINT)sizeof(MIDIHDR));

    // DWORD tempo = 500000;

    //     // sound midi
    //     else if (strcmp(msg_type, "note_on") == 0 || strcmp(msg_type, "note_off") == 0)
    //     {
    //         BYTE msg_bytes[] = { GET_BYTES_ITEM(bytes, 0), GET_BYTES_ITEM(bytes, 1), GET_BYTES_ITEM(bytes, 2) };

    //         midiHeader.lpData = (LPSTR)&msg_bytes;
    //         midiHeader.dwBufferLength = sizeof(msg_bytes);
    //         if (midiOutPrepareHeader(handle, &midiHeader, sizeof(MIDIHDR)) != MMSYSERR_NOERROR) {
    //             PyErr_SetString(plmidiExc_InitErr, NULL);
    //         }
    //         midiOutLongMsg(handle, &midiHeader, (UINT)sizeof(MIDIHDR));
    //     }
    //     else if (strcmp(msg_type, "set_tempo") == 0) {
    //         tempo = (DWORD)GET_ATTR(msg, "tempo");
    //     }
    //     Sleep(GET_ATTR(msg, "time") * tempo / 500000);
    // }

    free(msg_bytes);
    midiOutUnprepareHeader(handle, &midiHeader, sizeof(MIDIHDR));
    midiOutClose(handle);
    Py_RETURN_NONE;
}

// input -> mido.MidiTrack, tempo: int
// class mido.MidiTrack(list)
void sound_by_midiOutShortMsg(py::list piece, int tempo)
{
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
        throw plmidiExc_InitErr();
    }

    // init exit
    signal(SIGINT, plmidi_exit);

    // main loop
#ifdef PLMIDI_DEBUG
        py::print("main loop of plmidi player start");
#endif // PLMIDI_DEBUG
    for (auto msg : piece) // msg: mido.Message
    {
        ::std::string msg_type = msg.attr("type").cast<::std::string>();
#ifdef PLMIDI_DEBUG
        py::print("msg_type: ", msg_type);
#endif // PLMIDI_DEBUG
        // sound midi
        if ( msg_type.compare("program_change") == 0 ) {
            midiOutShortMsg(handle, msg.attr("program").cast<int>() << 8 | 0xC0 + msg.attr("channel").cast<int>());
        } else if ( msg_type.compare("note_on") == 0 ) {
            midiOutShortMsg(handle, msg.attr("velocity").cast<int>() << 16 | msg.attr("note").cast<int>() << 8 | 0x90 + msg.attr("channel").cast<int>());
        } else if ( msg_type.compare("note_off") == 0 ) {
            midiOutShortMsg(handle, msg.attr("velocity").cast<int>() << 16 | msg.attr("note").cast<int>() << 8 | 0x80 + msg.attr("channel").cast<int>());
        }
#ifdef PLMIDI_DEBUG
            py::print(msg);
#endif // PLMIDI_DEBUG
        Sleep(msg.attr("time").cast<int>() * tempo / 500'000); 
    }
#ifdef PLMIDI_DEBUG
    py::print("main loop of plmidi player end");
#endif // PLMIDI_DEBUG
    midiOutClose(handle);
}

} // namespace _plmidi

#undef GET_ATTR
#undef GET_ITEM