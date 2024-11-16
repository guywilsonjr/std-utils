#include <Python.h>

static PyObject* range_tuple(PyObject* self, PyObject* args) {
    int n;

    // Parse the input argument (an integer)
    if (!PyArg_ParseTuple(args, "i", &n)) {
        return NULL;
    }

    // Create a new tuple with n elements
    PyObject *tuple = PyTuple_New(n);
    if (!tuple) {
        return NULL;
    }

    // Fill the tuple with integers from 0 to n-1
    for (int i = 0; i < n; i++) {
        PyTuple_SET_ITEM(tuple, i, PyLong_FromLong(i));
    }

    return tuple;
}

// Define the methods for this module
static PyMethodDef RangeMethods[] = {
    {"range_tuple", range_tuple, METH_VARARGS, "Return a tuple of integers from 0 to n-1"},
    {NULL, NULL, 0, NULL}
};

// Define the module
static struct PyModuleDef rangemodule = {
    PyModuleDef_HEAD_INIT,
    "range_module",
    "A module that returns a tuple of integers from 0 to n-1",
    -1,
    RangeMethods
};

// Module initialization function
PyMODINIT_FUNC PyInit_range_module(void) {
    return PyModule_Create(&rangemodule);
}
