static PyObject *
caller_func(PyObject *self, PyObject* args)
{
    char* input = NULL;
    if (!PyArg_ParseTuple(args, "s", &input)) {
        return NULL;
    }
    WELD_INPUT_TYPE_0* data = (WELD_INPUT_TYPE_0*) input;
    int input_len = strlen(input);

    vec<WELD_INPUT_TYPE_0> weld_input_vec;
    weld_input_vec.size = input_len;
    weld_input_vec.ptr = data;
    input_type weld_input;
    weld_input._0 = weld_input_vec;

    struct WeldInputArgs weld_input_args;
    weld_input_args.input = &weld_input;
    weld_input_args.nworkers = 1;
    weld_input_args.memlimit = 100000000;
    weld_input_args.run_id = weld_runst_init(weld_input_args.nworkers, weld_input_args.memlimit);

    WeldOutputArgs* weld_output_args = run(&weld_input_args);
