# Variable COP and minimum conversion

## Introduction
Usually, the COP is defined by: 

$$ COP = \frac{\text{heat out}}{\text{electricity in}} $$

A result from the optimization at example timestep 3367 is:

$$ COP = \frac{34}{23.34} = 1.46 $$

Which doesn't fit to the COP given in the parameter file for this timestep, which is 2.56. 


## Question
>  How is the variable COP in example 15 used in the conversion from electricity to heat? How is the necessary electricity input calculated? 

## Answer
In example 15, the heat pump has a maximum heating capacity (rated power) of 100kW and a minimum conversion of 20% of the heating capacity. 

In addition, there are two different conversion expressions given: One for operating at minimum conversion where the transformation from electricity to heat is 1-to-1

$$ \text{conversion~at~min}:~1~\text{electricity} \longrightarrow 1~\text{heat} $$

And one for operating points above that minimum up to the maximum capacity: 

$$ \text{conversion}:1\text{electricity} \longrightarrow COP\text{heat} $$

When looking at the results there are three important variables that should be considered which have the following values at the example timestep 3367: 
* heatpump_exp_out_heat_primal: 34
* heatpump_exp_in_electricity_primal: 23.34
* heatpump_var_conversion_primal: 14

The heat output comprises two parts: 
* A 1-to-1 conversion of electricity to heat with an efficiency of 1; so this part equals always 20 as soon as the heat pump is turned on. 
* Every additionally required kW heating power is converted by an efficiency that is dependent on the COP at this timestep; in our example time step 3367 it is 2.56. 

This results in a total COP which is dependent on the power to be converted: With an increasing heat demand (meaning an increased part-load above minimum conversion), the total COP increases as well. At full-load, the total COP equals the COP from the parameter file. Between the minimum conversion and full-load, there is a linear correlation between heat out above minimum and electricity in above minimum. 

Calculation example: 

$$
\begin{align}
    & COP_{at~min} = 1 \\
    & COP_{over~min} = \frac{ COP_{at~max} \cdot (1-\alpha) \cdot \beta}{\beta - (COP_{at~max} \cdot \alpha)} = \frac{2.56 \cdot (1-0.2) \cdot 1}{1 - (2.56 \cdot 0.2)} = 4.197
\end{align}
$$

Where the second one is only applied to the delta above 20kW!

$$
\begin{align}
    & COP_{at~max} = COP_{from~file~at~t=3367} = 2.56 \\
    & COP_{total} = \frac{\text{out}}{\text{in}} = 1.46
\end{align}
$$

For a heating demand of 34 kW and a $COP_{at~max}$ of 2.56 one will need the following electricity:

$$
\text{In} = \frac{\alpha * \text{capacity}}{COP_{at~min}} + (34kW - \alpha \cdot \text{capacity}) \cdot \frac{1}{COP_{over~min}} = \frac{20kW}{1} +  \frac{14kW}{4.197} = 23.34 kW 
$$ 



## Details

A detailed derivation of the $COP_{over~min}$ equation: 

We assume the conversion to be given as

$$ 1~\text{electricity} \longrightarrow COP~\text{heat} $$

modified at a minimum conversion $\alpha$ ($\alpha = 0.2$ in the example) to

$$ 1~\text{electricity} \longrightarrow \beta~\text{heat} $$

with $\beta = 1.0$ in the example.

When calculating the "interpolated" COP, $COP_{over~min}$, we use the upper bound of the range as
interpolation node. At this (full) conversion, the output is simply given as

$$ \text{out} = \text{capacity} $$

since this is how the capacity is specified in the config. 

While the necessary amount of (input) electricity is known to
be $\alpha \cdot \text{capacity} \cdot \frac{1}{\beta}$, every conversion above this is linked to $COP_{over~min}$, resulting in
the total input electricity (at maximum conversion) being

$$ \text{in} = \alpha \cdot \text{capacity} \cdot \frac{1}{\beta} + (1 - \alpha) \cdot \text{capacity} \cdot \frac{1}{COP_{over~min}} $$

We know that the following must hold at the maximum operating point:

$$ COP_{at~max} = \frac{\text{out}}{\text{in}} $$

With the above, this leads to:

$$
\begin{align}
    & COP_{at~max} = \frac{\text{out}}{\text{in}} = \frac{\text{capacity}}{\alpha \cdot \text{capacity} \cdot \frac{1}{\beta} + (1 - \alpha) \cdot \text{capacity} \cdot \frac{1}{COP_{over~min}}} \\
    \Leftrightarrow \quad & COP_{at~max} = \frac{1}{\frac{\alpha}{\beta} + \frac{(1 - \alpha)}{COP_{over~min}}} = \frac{\beta \cdot COP_{over~min}}{\alpha \cdot COP_{over~min} + (1 - \alpha) \cdot \beta} \\
    \Leftrightarrow \quad & COP_{at~max} \cdot \alpha \cdot COP_{over~min} + COP_{at~max} \cdot (1 - \alpha) \cdot \beta = \beta \cdot COP_{over~min} \\
    \Leftrightarrow \quad & COP_{over~min} = \frac{COP_{at~max} \cdot (1 - \alpha) \cdot \beta}{\beta - COP_{at~max} \cdot \alpha}
\end{align}
$$

where the last equation gives the final calculation of the "interpolated" $COP_{over~min}$

---

The plot shows the total COP calculated for three different $COP_{at~max}$ values over the possible operation range. 

![showcase](https://gist.github.com/user-attachments/assets/87682e1f-4935-4615-a352-53f6fb8af2fa)

## Summary

The COP from the parameter file isn't used directly to calculate the necessary electricity input to meet the heating power demand. The minimum electricity input is always 20kW as soon as the heat pump is turned on. The additionally required electricity input is calculated by the last formula, where the COP out of the parameter file is used. 

