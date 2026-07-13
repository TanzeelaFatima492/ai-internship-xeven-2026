from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=500,

            chunk_overlap=100,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " "
            ]
        )

    def split_text(
        self,
        text: str
    ):

        return self.text_splitter.split_text(text)