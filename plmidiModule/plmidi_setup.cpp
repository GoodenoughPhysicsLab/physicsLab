#if !defined(_MSC_VER) || !defined(_WIN32)
#   error "This code must be compiled with MSVC on Windows"
#endif

#include "plmidi_sound.hpp"

PYBIND11_MODULE(plmidi, m) {
    //m.def("sound", _plmidi::sound);
    m.def("sound_by_midiOutShortMsg", _plmidi::sound_by_midiOutShortMsg);
    // plmidiInitError
    py::register_exception<_plmidi::plmidiExc_InitErr>(m, "plmidiInitError");
}