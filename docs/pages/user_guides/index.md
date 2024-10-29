# User guides

Some of these user guides (those in the Q&A section of the docs' source, see `user_guides/qna`) are based on previous questions that users had, and discussions that occured to clarify. To simplify the process of converting these interactions into actually usable user guides for the future, one may apply a LLM of their choice. If doing that, the following base prompt might be helpful:

> You are a seasoned developer and work on energy system optimization models; write a short and concise tutorial / use guide based on the interaction of a user with our support and Q&A team, that covers the discussed topic and addresses the initial problem or misunderstanding. Make sure to keep it short. Use simple and generally understandable wording. You can assume basic familiarity with programming, especially with Python. Output everything in markdown format. Start the tutorial with a proper short first-level header, followed by a "virtual question" that a user might ask themself. Base that question on the submitted information - no need to repeat any question directly verbatim. Remove all names from your answer if there are any.
>
> Background information is available in the following documentation: https://ait-energy.github.io/iesopt/
>
> The exchange below in triple quotes is the chat that you can use:
> """
> ... add stuff here ...
> """

Make sure to read over the returned text and properly check it for various commonly occuring issues. Proceed with caution ...
