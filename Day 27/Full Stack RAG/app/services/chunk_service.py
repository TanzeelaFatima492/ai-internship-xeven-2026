from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split_text(
        self,
        text: str
    ) -> list[str]:

        return self.text_splitter.split_text(text)