from typing import Any, List, Optional
from pydantic import BaseModel, Field

class HaasScriptExecutionPackage(BaseModel):
    """Script execution package"""
    script_id: str = Field(alias="ScriptId")
    script_name: str = Field(alias="ScriptName")
    script_type: str = Field(alias="ScriptType")
    is_command: bool = Field(alias="IsCommand")
    command_name: str = Field(alias="CommandName")
    source_code: str = Field(alias="SourceCode")
    commands: List[Any] = Field(alias="Commands")

    class Config:
        populate_by_name = True

class HaasCommandBase(BaseModel):
    """Base command information"""
    command_name: str = Field(alias="CommandName")
    command: str = Field(alias="Command")
    command_type: str = Field(alias="CommandType")
    category: str = Field(alias="Category")
    description: str = Field(alias="Description")
    return_description: str = Field(alias="ReturnDescription")
    parameters: List[Any] = Field(alias="Parameters")
    output_index: int = Field(alias="OutputIndex")
    is_constant: bool = Field(alias="IsConstant")
    is_primary: bool = Field(alias="IsPrimary")
    requires_call: bool = Field(alias="RequiresCall")
    resizable: bool = Field(alias="Resizable")
    output_hidden: bool = Field(alias="OutputHidden")
    output_type: str = Field(alias="OutputType")
    output_suggestions: List[Any] = Field(alias="OutputSuggestions")
    change_types: List[Any] = Field(alias="ChangeTypes")
    execution_times: List[int] = Field(alias="ExecutionTimes")

    class Config:
        populate_by_name = True
