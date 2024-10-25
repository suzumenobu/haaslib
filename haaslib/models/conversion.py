from pydantic import BaseModel, Field

class AmountConversionResultObject(BaseModel):
    """Amount conversion result"""
    conversion_rate: float = Field(alias="ConversionRate")
    converted_amount: float = Field(alias="ConvertedAmount")

    class Config:
        populate_by_name = True
