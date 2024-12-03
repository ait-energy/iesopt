# Julia

If you are interested in more details on how to use [IESopt.jl](https://github.com/ait-energy/IESopt.jl) directly, please refer to it's [documentation](https://ait-energy.github.io/IESopt.jl/stable/).

:::{tip}
The public API of the Python wrapper was, as far as possible, designed to be almost identical to the one of the Julia package, so things should look similar.

For example, the following Python code:

```python
import iesopt

model = iesopt.generate("config.iesopt.yaml")

my_result = model.get_component("turbine").exp.out_water
```

can be translated to Julia like this:

```julia
import IESopt

model = IESopt.generate!("config.iesopt.yaml")

my_result = IESopt.get_component(model, "turbine").exp.out_water
```

:::
