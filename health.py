from fastapi import FastAPI
import psutil
import platform
from datetime import datetime

app = FastAPI()

def get_server_health():
    # Get system information
    system_info = {
        "hostname": platform.node(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "memory_used_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }
    return system_info

@app.get("/api/serverhealthcheck")
def server_health_check():
    health_info = get_server_health()
    return health_info

# Run the app
# To run: `uvicorn <script_name>:app --reload`
