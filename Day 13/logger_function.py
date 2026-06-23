def log(level, *messages, **options):
    # Default options
    timestamp = options.get("timestamp", True)
    file_name = options.get("file", "log.txt")
    format_type = options.get("format", "text")

    # Combine messages
    message = " ".join(str(m) for m in messages)

    # Simple color tags (terminal-style simulation)
    colors = {
        "INFO": "NORMAL",
        "WARNING": "YELLOW",
        "ERROR": "RED"
    }

    color = colors.get(level.upper(), "NORMAL")

    # Create log string
    log_entry = ""

    if timestamp:
        import datetime
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry += f"[{time}] "

    if format_type == "json":
        log_entry += str({
            "level": level,
            "message": message,
            "color": color
        })
    else:
        log_entry += f"{level.upper()} ({color}): {message}"

    # Print log
    print(log_entry)

    # Save to file
    with open(file_name, "a") as f:
        f.write(log_entry + "\n")


# 🔹 Examples
log("INFO", "System started")
log("WARNING", "Low disk space", "Drive C:")
log("ERROR", "System crash", timestamp=True)
log("INFO", "User login", format="json")