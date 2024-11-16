#include <Python.h>
#include <string.h>
#include <stdlib.h>  // for malloc, free

// A struct to represent each key-value pair
typedef struct {
    const char* key;
    const char* value;
} NamespaceItem;

// A struct representing the immutable namespace (dictionary-like)
typedef struct PyImmutableNamespace {
    PyObject_HEAD
    struct ImmutableNamespace* namespace;
} PyImmutableNamespace;

// A struct representing the immutable namespace (dictionary-like)
typedef struct {
    NamespaceItem* items;
    size_t size;
} ImmutableNamespace;

// Function to create a new ImmutableNamespace
ImmutableNamespace* create_namespace(NamespaceItem* items, size_t size) {
    ImmutableNamespace* namespace = (ImmutableNamespace*)malloc(sizeof(ImmutableNamespace));
    if (namespace == NULL) {
        return NULL;
    }
    namespace->items = items;
    namespace->size = size;
    return namespace;
}

// Function to retrieve a value by key (very fast look-up)
const char* get_value(const ImmutableNamespace* namespace, const char* key) {
    for (size_t i = 0; i < namespace->size; ++i) {
        if (strcmp(namespace->items[i].key, key) == 0) {
            return namespace->items[i].value;
        }
    }
    return NULL;  // Return NULL if the key is not found
}

// Function to get an item from the namespace in Python
static PyObject* py_get_value(PyImmutableNamespace* self, PyObject* args) {
    const char* key;
    if (!PyArg_ParseTuple(args, "s", &key)) {
        return NULL;
    }

    const char* value = get_value(self->namespace, key);
    if (value == NULL) {
        Py_RETURN_NONE;
    }

    return PyUnicode_FromString(value);
}

// Function to create a new ImmutableNamespace object in Python
static PyObject* py_create_namespace(PyObject* self, PyObject* args) {
    PyObject* key_value_pairs;
    if (!PyArg_ParseTuple(args, "O", &key_value_pairs)) {
        return NULL;
    }

    // Ensure key_value_pairs is a tuple
    if (!PyTuple_Check(key_value_pairs)) {
        PyErr_SetString(PyExc_TypeError, "The argument must be a tuple of key-value pairs.");
        return NULL;
    }

    size_t size = PyTuple_Size(key_value_pairs);
    NamespaceItem* items = (NamespaceItem*)malloc(size * sizeof(NamespaceItem));
    if (items == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

    for (size_t i = 0; i < size; ++i) {
        PyObject* pair = PyTuple_GetItem(key_value_pairs, i);

        // Ensure each pair is a tuple with 2 elements
        if (!PyTuple_Check(pair) || PyTuple_Size(pair) != 2) {
            PyErr_SetString(PyExc_TypeError, "Each element of the tuple must be a tuple of (key, value).");
            free(items);
            return NULL;
        }

        PyObject* key_obj = PyTuple_GetItem(pair, 0);
        PyObject* value_obj = PyTuple_GetItem(pair, 1);

        if (!PyUnicode_Check(key_obj) || !PyUnicode_Check(value_obj)) {
            PyErr_SetString(PyExc_TypeError, "Both key and value must be strings.");
            free(items);
            return NULL;
        }

        // Ensure UTF-8 strings are properly handled
        const char* key = PyUnicode_AsUTF8(key_obj);
        const char* value = PyUnicode_AsUTF8(value_obj);

        items[i].key = key;
        items[i].value = value;
    }

    ImmutableNamespace* namespace = create_namespace(items, size);
    if (namespace == NULL) {
        free(items);
        PyErr_NoMemory();
        return NULL;
    }

    PyImmutableNamespace* result = (PyImmutableNamespace*)PyObject_New(PyImmutableNamespace, &PyImmutableNamespace_Type);
    if (result == NULL) {
        free(items);
        free(namespace);
        return NULL;
    }
    result->namespace = namespace;

    return (PyObject*)result;
}

// Python object deallocation function
static void py_immutable_namespace_dealloc(PyImmutableNamespace* self) {
    if (self->namespace) {
        free(self->namespace->items);
        free(self->namespace);
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

// Define the methods of the ImmutableNamespace class
static PyMethodDef PyImmutableNamespace_methods[] = {
    {"get_value", (PyCFunction)py_get_value, METH_VARARGS, "Get a value by key"},
    {NULL}  // Sentinel
};

// Define the Python type for the ImmutableNamespace class
static PyTypeObject PyImmutableNamespace_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "immutable_namespace.ImmutableNamespace",  // Name of the class
    sizeof(PyImmutableNamespace),              // Size of the object
    0,                                         // Basics: item size and allocation
    (destructor)py_immutable_namespace_dealloc, // Deallocation method
    0,                                         // Generic methods
    0,                                         // Generic methods
    0,                                         // Generic methods
    0,                                         // Generic methods
    0,                                         // Generic methods
    0,                                         // Generic methods
    0,                                         // Generic methods
    0,                                         // Generic methods
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,  // Type flags
    0,                                         // Documentation
    0,                                         // Traversal
    0,                                         // Clear
    0,                                         // Rich comparison
    0,                                         // Weak references
    0,                                         // Iteration
    0,                                         // Methods
    PyImmutableNamespace_methods,              // Methods
};

// Module methods
static PyMethodDef module_methods[] = {
    {"create_namespace", py_create_namespace, METH_VARARGS, "Create a new ImmutableNamespace"},
    {NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "immutable_namespace",  // Module name
    "An efficient immutable namespace",  // Module docstring
    -1,  // Size of per-interpreter state of the module
    module_methods
};

// Module initialization function
PyMODINIT_FUNC PyInit_immutable_namespace(void) {
    PyObject* m;

    if (PyType_Ready(&PyImmutableNamespace_Type) < 0)
        return NULL;

    m = PyModule_Create(&module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&PyImmutableNamespace_Type);
    PyModule_AddObject(m, "ImmutableNamespace", (PyObject*)&PyImmutableNamespace_Type);

    return m;
}
