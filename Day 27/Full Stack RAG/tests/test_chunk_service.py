from app.services.chunk_service import ChunkService

text = """
Margherita Pizza

Price Rs.850

Fresh mozzarella cheese

Pepperoni Pizza

Price Rs.1200

Spicy pepperoni

Chicken Burger

Price Rs.650

Crispy chicken
""" * 30


service = ChunkService()

chunks = service.split_text(text)

print("Chunks:", len(chunks))

for i, chunk in enumerate(chunks):

    print("=" * 50)

    print(f"Chunk {i+1}")

    print(chunk[:200])