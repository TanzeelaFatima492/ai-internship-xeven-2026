import os

async def write_document(filename: str, content: str) -> str:
    """Save content to a file"""
    os.makedirs("outputs", exist_ok=True)
    with open(f"outputs/{filename}.txt", "w") as f:
        f.write(content)
    return f"✅ Document saved: {filename}"