import datetime

def generate_script():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    script = f"""
    Imagine if the Moon disappeared...

    Without the Moon, Earth's tides would collapse.
    Nighttime animals would go into chaos.
    Our planet's tilt could shift wildly over time,
    causing extreme weather and seasons.

    That's what could happen... if the Moon vanished.
    ({today})
    """
    print(script)

if __name__ == "__main__":
    generate_script()
