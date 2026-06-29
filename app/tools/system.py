import psutil
import shutil
import subprocess

def gpu_status() -> dict:
    try:
        r = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if r.returncode != 0:
            return {"available": False, "error": r.stderr.strip()}

        first_line = r.stdout.strip().splitlines()[0]
        name, util, mem_used, mem_total, temp, power = [x.strip() for x in first_line.split(",")]
        return {
            "available": True,
            "name": name,
            "util_percent": int(float(util)),
            "memory_used_mb": int(float(mem_used)),
            "memory_total_mb": int(float(mem_total)),
            "temperature_c": int(float(temp)),
            "power_watts": float(power),
        }
    except Exception as e:
        return {"available": False, "error": str(e)}

def status() -> dict:
    disk = shutil.disk_usage("/")
    ram = psutil.virtual_memory()
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": ram.percent,
        "ram_used_gb": round(ram.used / 1024**3, 2),
        "ram_total_gb": round(ram.total / 1024**3, 2),
        "disk_percent": round(disk.used / disk.total * 100, 1),
        "disk_used_gb": round(disk.used / 1024**3, 2),
        "disk_total_gb": round(disk.total / 1024**3, 2),
        "gpu": gpu_status(),
    }
