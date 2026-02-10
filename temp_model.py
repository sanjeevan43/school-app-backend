class BusDriverAssign(BaseModel):
    driver_id: Optional[str] = Field(None, description="Driver ID (UUID) or null to unassign")
