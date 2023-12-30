#include <iostream>
#include "pybind11/pybind11.h"

namespace py = pybind11;

namespace plmidi::process_bar
{

class MidiProcessBar {
    static constexpr int _length = 50;
    int _status = 1;
    int _duration = 0;
public:
    MidiProcessBar(int midi_duration) {
        this->_duration = midi_duration;
    }

    ~MidiProcessBar() {
        py::print("\n");
    }

    bool is_not_end() {
        return this->_status <= this->_length;
    }

    int status() {
        return this->_status;
    }

    int length() {
        return this->_length;
    }

    void update() {
        ::std::cout << "\r";
        this->_status += 1;
    }

    void print() {
        int i{};
        for (; i < this->_status; ++i) {
            ::std::cout << "-";
        }
        for (; i < this->_length; ++i) {
            ::std::cout << " ";
        }
        ::std::cout << " " << this->_duration / this->_length * this->_status <<  "/" <<  this->_duration;
    }
};

} // namespace plmidi::process_bar