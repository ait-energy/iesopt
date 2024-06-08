import os
if "IESOPT_DOCS_NOEXEC" in os.environ and os.environ["IESOPT_DOCS_NOEXEC"] == "true":
    print("Detected docs environment, will skip setting up Julia.")
