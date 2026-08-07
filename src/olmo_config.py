# use the following code to grab the correct revision and store as constants.

# import re
# LAST_STAGE1 = lambda names: max(
#    (b for b in names if b.startswith("stage1")),
#    key=lambda b: int(re.search(r"step(\d+)", b).group(1)),
#)


OLMO_REVISIONS = {
    "OLMo-2-0425-1B": "stage1-step1907359-tokens4001B",
    "OLMo-2-1124-7B": "stage1-step928646-tokens3896B",
    "OLMo-2-1124-13B": "stage1-step596057-tokens5001B",
}


# Call in every OLMo Notebook

# from src.olmo_config import OLMO_REVISIONS
# revision = OLMO_REVISIONS[model_id]

