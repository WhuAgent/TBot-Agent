import os

from langchain_core.documents import Document
from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings

from utils.md import get_task_and_commands
from utils.read_config_data import read_yaml_data

openai_config_path = "config/openai_config.yaml"
openai_config = read_yaml_data(openai_config_path)

milvus_config_path = "config/milvus.yaml"
milvus_config = read_yaml_data(milvus_config_path)


class TaskVectorDB:
    def __init__(self, manual_root):
        docs = []

        for root, dirs, files in os.walk(manual_root):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    data = get_task_and_commands(file_path)
                    docs.append(Document(page_content=data["task"], metadata={"commands": ",".join(data["commands"])}))

        openai_embedding_client = OpenAIEmbeddings(model="text-embedding-3-large",
                                                   openai_api_base=openai_config["base_url"],
                                                   openai_api_key=openai_config["api_key"])

        self.vectordb = Milvus.from_documents(documents=docs,
                                              embedding=openai_embedding_client,
                                              connection_args={"host": milvus_config["host"],
                                                               "port": milvus_config["port"]},
                                              collection_name="TBotTaskManual",
                                              drop_old=True)

    def get_relevant_commands(self, query):
        query = f"用户要完成的任务为: {query}, 有历史完成过的任务可供参考吗？"
        res = self.vectordb.similarity_search(query, k=20)
        res.sort(key=lambda ele: ele.metadata["pk"])

        commands = set()

        for item in res:
            commands.update(item.metadata["commands"].split(","))

        return commands
