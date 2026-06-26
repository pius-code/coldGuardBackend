# flake8: noqa
# type: ignore
from agent.tools.sensor import get_the_sensor_readings
from agent.tools.research_agent import do_research
from utils.logger import agentlogger

"""all the tools that the coldguard agent needs to run for now"""

from agent.core.fastmcp import mcp

_MAX_DAYS = 14

@mcp.tool
async def get_sensor_data(days: int):
    """Use this tool to retrieve historical sensor readings from the cold storage unit.
    Call this when the user asks about past temperature, humidity, or light readings,
    or when you need data to assess drug viability or generate a report.
    
    Example triggers:
    - "get me readings from the past 3 days"
    - "what has the temperature been this week"
    - "generate a drug report" (call this first to get the data)
    
    Parameters:
        days (int): Number of days back to fetch readings. 
                    Use 1 for today, 7 for a week, 30 for a month, 4 for the past 4 days.
    
    Returns:
        List of sensor readings with dateTime, temperature, humidity, and light_intensity.
    """
    days = min(days, _MAX_DAYS)
    agentlogger.info(f"Fetching sensor data for {days} day(s)")
    return await get_the_sensor_readings(days)

@mcp.tool 
async def build_vaccine_report(days: int , prompt : str):
    """Use this tool to generate a detailed pharmaceutical viability report for the stored drugs.
    Call this when the user asks for a drug report, viability assessment, or wants to know 
    if their drugs are still safe to use.
    
    Parameters:
        days (int): Number of days of sensor data to analyze. Default to 7 for a weekly report.
        prompt (str): A descriptive instruction for the research agent. Should include:
                      - What drug is being assessed
                      - What the user wants to know
                      - Any specific concerns
                      Example: "Assess the viability of Amoxicillin dry powder stored in this 
                      unit over the past 7 days. The pharmacist wants to know if the drugs are 
                      still safe to dispense. Generate a full report with potency estimate, 
                      verdict, and recommended action."
    
    Returns:
        A detailed viability report including potency estimate, verdict (SAFE/MONITOR/DO NOT USE),
        reasoning, recommended action, and estimated days before unsafe threshold is reached.
    """
    days = min(days, _MAX_DAYS)
    agentlogger.info(f"Building vaccine report for {days} day(s)")
    sensor_data = await get_the_sensor_readings(days)
    research_data = await do_research(sensor_data, prompt)
    agentlogger.info("Vaccine report generated successfully")
    return research_data



