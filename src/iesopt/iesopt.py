from .model import Model


def run(filename: str, **kwargs) -> Model:
    r"""
    Generate and optimize a IESopt model.

    Results can be accessed (after a successful optimization) using `model.results`.

    Arguments:
        filename (str): Path to the IESopt model file to load.
    
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
    model = Model(filename, **kwargs)
    model.generate()
    model.optimize()
    return model
