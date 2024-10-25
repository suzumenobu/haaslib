from typing import List, Dict
from typing_extensions import Any, Optional
from pydantic import BaseModel, Field

class HaasScriptCompileError(BaseModel):
    """Script compilation error"""
    pass  # Base class for compilation errors

class LuaScriptCompileError(HaasScriptCompileError):
    """Lua-specific script compilation error"""
    pass  # Add specific Lua error fields if needed

class VisualScriptCompileError(HaasScriptCompileError):
    """Visual script compilation error"""
    command_guid: str = Field(alias="CommandGuid")
    input_guid: str = Field(alias="InputGuid")

    class Config:
        populate_by_name = True

class HaasScriptCompileRecord(BaseModel):
    """Script compilation record"""
    source_code: str = Field(alias="SourceCode")
    compile_result: Any = Field(alias="CompileResult")
    user_id: str = Field(alias="UserId")
    script_id: str = Field(alias="ScriptId")
    script_name: str = Field(alias="ScriptName")
    script_description: str = Field(alias="ScriptDescription")
    script_type: str = Field(alias="ScriptType")
    script_status: str = Field(alias="ScriptStatus")
    command_name: str = Field(alias="CommandName")
    is_command: bool = Field(alias="IsCommand")
    is_valid: bool = Field(alias="IsValid")
    created_unix: int = Field(alias="CreatedUnix")
    updated_unix: int = Field(alias="UpdatedUnix")

    class Config:
        populate_by_name = True

class HaasScriptOlderVersion(BaseModel):
    """Previous version of a script"""
    id: str = Field(alias="Id")
    script_id: str = Field(alias="ScriptId")
    version: str = Field(alias="Version")
    created: int = Field(alias="Created")
    source_code: str = Field(alias="SourceCode")

    class Config:
        populate_by_name = True

class HaasScriptInputField(BaseModel):
    """Script input field definition"""
    pass  # Add specific input field properties as needed

class HaasScriptScanField(BaseModel):
    """Script scan field definition"""
    pass  # Add specific scan field properties as needed
