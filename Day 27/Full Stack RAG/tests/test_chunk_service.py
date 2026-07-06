from app.services.chunk_service import ChunkService

service = ChunkService()

text = """
Pizza is made with fresh mozzarella cheese.

Our Margherita Pizza costs Rs.850.

Chicken Burger costs Rs.650.

We also have Pasta,
Garlic Bread,
French Fries,
and many desserts.
""" * 10

chunks = service.split_text(text)

print("Total Chunks:", len(chunks))

print()

for i, chunk in enumerate(chunks):

    print("=" * 50)

    print(f"Chunk {i + 1}")

    print()

    print(chunk)