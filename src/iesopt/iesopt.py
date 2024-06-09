from .model import Model


def run(filename: str, verbosity: bool | str = True, **kwargs) -> Model:
    r"""
    Generate and optimize an IESopt model.

    Results can be accessed (after a successful optimization) using `model.results`.

    Arguments:
        filename (str): Path to the IESopt model file to load.
        verbosity (bool or str, optional): Verbosity level for the IESopt model, defaults to `True`. If `True`, the core
            model will be run in verbose mode, `"warning"` will show warnings (and errors), setting it to `False` will
            only show errors. If `verbosity_solve` is not set in the top-level YAML config, `verbosity = True` will
            enable solver verbose mode, otherwise the solver will be run in silent mode.

    Keyword Arguments:
        **kwargs: Additional keyword arguments to pass to the `Model` constructor.

    Returns:
        Model: The generated and optimized IESopt model.

    Example:
        ..  code-block:: python
            :caption: Run an IESopt model

            import iesopt
            iesopt.run("opt/config.iesopt.yaml")
    """
    model = Model(filename, verbosity=verbosity, **kwargs)
    model.generate()
    model.optimize()  # TODO: catch errors in generate
    return model
