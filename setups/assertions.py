import json
import jsonschema
from pathlib import Path
from typing import Dict

from setups import basemodel_Imitation_Game
from setups.setup import JSON_SCHEMA_PATH


def assert_valid_markup_ct_general(markup: Dict):
    """
    Checks for general compliance this_user_dict to expected structure of basemodel_Imitation_Game jsonschema

    :param markup: output from create_new_user as dict
    """
    scheme = get_markup_scheme()
    # print(jsonschema.Draft7Validator.check_schema(scheme))  # OPEN when debug schema
    correct = jsonschema.Draft7Validator(scheme).is_valid(markup)
    errors = sorted(jsonschema.Draft7Validator(scheme).iter_errors(markup), key=str)
    for e in errors:
        print(
            f"path in markup : {e.path}, instance value : {e.instance}\n"
            f"path in scheme : {e.schema_path}, should be value : {e.schema}\n"
            f"{e.message}\n"
            f"*****"
        )
    assert correct, str(errors)


def get_markup_scheme() -> Dict[str, Path]:
    """
    Return basemodel_Imitation_Game jsonschema as dict

    :param
    :return: basemodel_Imitation_Game jsonschema as dict
    """
    return json.load(open(JSON_SCHEMA_PATH, "r"))


if __name__ == "__main__":
    test_user = basemodel_Imitation_Game.Player(userid=0, username="test_user")
