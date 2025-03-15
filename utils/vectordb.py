import os

from langchain_core.documents import Document
from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings

from utils.md import get_task_and_commands, get_task_and_plan
from utils.read_config_data import read_yaml_data

openai_config_path = "tbot/config/openai.yml"
openai_config = read_yaml_data(openai_config_path)

milvus_config_path = "tbot/config/milvus.yaml"
milvus_config = read_yaml_data(milvus_config_path)

openai_embedding_client = OpenAIEmbeddings(model="text-embedding-3-large",
                                           openai_api_base=openai_config["base_url"],
                                           openai_api_key=openai_config["api_key"])


class TaskPlanVectorDB:
    def __init__(self, manual_root):
        docs = []

        for root, dirs, files in os.walk(manual_root):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    data = get_task_and_plan(file_path)
                    docs.append(Document(page_content=data["task"], metadata={"plan": "->".join(data["plan"])}))

        self.vectordb = Milvus.from_documents(documents=docs,
                                              embedding=openai_embedding_client,
                                              connection_args={"host": milvus_config["host"],
                                                               "port": milvus_config["port"]},
                                              collection_name="TaskPlanVectorDB",
                                              drop_old=True)

    def get_relevant_plans(self, query):
        query = f"用户要完成的任务为: {query}, 有历史完成过的任务可供参考吗？"
        res = self.vectordb.similarity_search(query, k=5)
        res.sort(key=lambda ele: ele.metadata["pk"])

        references = []

        for item in res:
            references.append({
                "task": item.page_content,
                "plan": item.metadata["plan"].split("->")
            })

        return references


class CommandVectorDB:
    def __init__(self, manual_root):
        docs = []

        for root, dirs, files in os.walk(manual_root):
            for file in files:
                if file.endswith(".txt"):
                    action = os.path.basename(root)
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        command = f.read()
                    docs.append(Document(page_content=command, metadata={"action": action}))

        self.vectordb = Milvus.from_documents(documents=docs,
                                              embedding=openai_embedding_client,
                                              connection_args={"host": milvus_config["host"],
                                                               "port": milvus_config["port"]},
                                              collection_name="ActionVectorDB",
                                              drop_old=True)

    def get_relevant_commands(self, query):
        query = f"用户要执行的动作为: {query}, 有哪些命令可能有用？"
        res = self.vectordb.similarity_search(query, k=5)
        res.sort(key=lambda ele: ele.metadata["pk"])

        actions = set()
        for item in res:
            actions.add(item.metadata["action"])

        return actions