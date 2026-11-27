#include <pybind11/pybind11.h>
#include "weights.hpp"


namespace py = pybind11;


int add(int a, int b) {
    return a + b;
}

PYBIND11_MODULE(ai_engine, module) {
    module.doc() = "Gomoku AI engine";

    module.def("add", &add, "Add two integers");

    py::class_<HeuristicWeights>(module, "HeuristicWeights")
        .def(
            py::init<
                int, int, int,
                int, int, int,
                int,
                int, int, int, int, int,
                int, int
            >()
        )
        .def_readwrite("three_blocked_stones", &HeuristicWeights::three_blocked_stones)
        .def_readwrite("three_half_blocked_stones", &HeuristicWeights::three_half_blocked_stones)
        .def_readwrite("three_open_stones", &HeuristicWeights::three_open_stones)
        .def_readwrite("four_blocked_stones", &HeuristicWeights::four_blocked_stones)
        .def_readwrite("four_half_blocked_stones", &HeuristicWeights::four_half_blocked_stones)
        .def_readwrite("four_open_stones", &HeuristicWeights::four_open_stones)
        .def_readwrite("five_open_stones", &HeuristicWeights::five_open_stones)
        .def_readwrite("capture_one", &HeuristicWeights::capture_one)
        .def_readwrite("capture_two", &HeuristicWeights::capture_two)
        .def_readwrite("capture_three", &HeuristicWeights::capture_three)
        .def_readwrite("capture_four", &HeuristicWeights::capture_four)
        .def_readwrite("capture_five", &HeuristicWeights::capture_five)
        .def_readwrite("stone_capture", &HeuristicWeights::stone_capture)
        .def_readwrite("central_position", &HeuristicWeights::central_position);}
