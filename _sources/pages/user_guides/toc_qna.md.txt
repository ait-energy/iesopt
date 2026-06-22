# Q & A

These are based on previous questions that users had and discussions that occurred to clarify. They can be used to point users to for any questions that repeatedly occur.

## Contents

:::{toctree}
:maxdepth: 1
:titlesonly:

qna/snapshot_duration.md
qna/profiles_sign.md
qna/dynamic_marginal_costs.md
qna/passive_charging.md
:::

## Assisted writing

To simplify the process of converting these interactions into actually usable user guides for the future, one may apply a LLM of their choice. If doing that, the following base prompt might be helpful (**tip: hover your mouse & one-click copy in the top right**):

```text
You are a seasoned developer and work on energy system optimization models; write a short and concise tutorial / user-guide based on the interaction of a user with our support and Q&A team, that covers the discussed topic and addresses the initial problem or misunderstanding. Make sure to keep it short. Use simple and generally understandable wording. You can assume basic familiarity with programming, especially with Python. Output everything in markdown format. Start the tutorial with a proper short first-level header, followed by a "virtual question" that a user might ask themself. Base that question on the submitted information - no need to repeat any question directly verbatim. Remove all names from your answer if there are any. Header texts should start with an upper case letter, but use proper English case (mostly lower) for all other words.

Background information is available in the following documentation: https://ait-energy.github.io/iesopt/

The exchange below in triple quotes is the chat that you can use:

"""
... add stuff here ...
"""
```

Make sure to read over the returned text and properly check it for various commonly occurring issues. Proceed with caution ...

## Format & Structure

> Only loosely defined guidelines, feel free to do what's best for the docs.

These user guides roughly follow the following structure:

```markdown
# Title header

## Intro

**Question:**  
> I'm moving from hourly to daily time steps in my IESopt model. How should I adjust my input data, especially capacities and costs, to ensure accurate results? Should I express capacities as energy per time step (e.g., kWh/day) instead of power (kW)?

**Answer:**  
> When working with IESopt models, it's crucial to understand how the model interprets units of power and energy, especially when changing the duration of your time steps (snapshots). Here's how to approach this:

## Details

_... a more detailed answer and further explanations go here ..._

## Summary

_... a summary goes here ..._

_... often this is the place for further notes, comments, key takeaways ..._

### Conclusion

_... and finally a 1-3 sentence conclusion ..._
```
