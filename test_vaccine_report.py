import asyncio
from datetime import datetime, timedelta
from agent.tools.research_agent import do_research

MOCK_SENSOR_DATA = [
    {"dateTime": datetime.now() - timedelta(hours=i*6), "temperature": str(26 + i % 3), "humidity": "60", "light_intensity": "low"} # noqa
    for i in range(8)
]

PROMPT = (
    "I have sensor data from the past 2 days from a cold storage unit storing Amoxicillin dry powder. " # noqa
    "Please build a full vaccine viability report based on the readings."
)


async def main():
    print("Sending mock sensor data to research agent...\n")
    result = await do_research(MOCK_SENSOR_DATA, PROMPT)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
