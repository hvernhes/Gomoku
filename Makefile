# Tools
PYTHON = python
CMAKE = cmake

# Directories
CPP_DIR = cpp
BUILD_DIR = $(CPP_DIR)/build

# Default target
.DEFAULT_GOAL := build

# Configure the C++ project
configure:
	$(CMAKE) -S $(CPP_DIR) -B $(BUILD_DIR) \
		-DCMAKE_BUILD_TYPE=Release \
		-Dpybind11_DIR="$$($(PYTHON) -m pybind11 --cmakedir)"

# Compile the C++ module
build: configure
	$(CMAKE) --build $(BUILD_DIR) --parallel

# Compile and launch the game
run: build
	PYTHONPATH=$(BUILD_DIR) $(PYTHON) -m src.gomoku

test: build
	PYTHONPATH=. pytest -v -s

# Remove generated build files
clean:
	rm -rf $(BUILD_DIR)

.PHONY: configure build run clean
