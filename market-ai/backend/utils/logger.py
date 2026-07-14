from loguru import logger 

logger.add(
    "logs/system.log" ,
    rotation = "10MB",
    retention = "10 days"
)

