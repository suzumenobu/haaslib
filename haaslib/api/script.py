from typing import List
from ..executor import RequestsExecutor, Authenticated
from ..models.script import ScriptConfig
from ..exceptions import ScriptError

def get_scripts(executor: RequestsExecutor[Authenticated]) -> List[ScriptConfig]:
    """Returns available scripts"""
    response = executor.execute(
        endpoint="ScriptAPI",
        response_type=List[ScriptConfig],
        query_params={
            "channel": "GET_SCRIPTS"
        }
    )
    if not response.Success:
        raise ScriptError(f"Failed to get scripts: {response.Error}")
    return response.Data
