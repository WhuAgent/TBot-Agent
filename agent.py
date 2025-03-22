from agent_network.base import BaseAgent
from agent_network.exceptions import ReportError


class worker(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)
        
    def forward(self, messages, **kwargs):
        if error_message := kwargs.get("graph_error_message"):
            prompt = f"错误：{error_message}"
        else:
            task = kwargs.get("task")
            prompt = task
            
            if ocr_result :=  kwargs.get("ocr_result"):
                prompt += f"\n\n相关文件的文字识别结果为 {ocr_result}"
            if image_result := kwargs.get("image_result"):
                prompt += f"\n\n相关图片的识别结果为 {image_result}"
        self.add_message("user", prompt, messages)
        response = self.chat_llm(messages,
                                 api_key="sk-ca3583e3026949299186dcbf3fc34f8c",
                                 base_url="https://api.deepseek.com",
                                 model="deepseek-chat",
                                 response_format={"type": "json_object"})
        
        response_data = response.content
        
        if "tool_name" in response_data:
            result = {**response_data["tool_args"]}
            return result, response_data["tool_name"]
        elif "result" in response_data:
            result = {
                "result": response_data["result"]
            }
            return result
        else:
            raise ReportError("unknown response format", "worker")
    

class ocr_tool(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)
        
    def forward(self, messages, **kwargs):
        ocr_file_name = kwargs.get("ocr_file_name")
        if not ocr_file_name:
            raise ReportError("ocr_file_name is not provided", "worker")
        
        import easyocr
        reader = easyocr.Reader(['ch_sim','en'])
        ocr_result = reader.readtext(ocr_file_name, detail=0)
        self.log("assistant", ocr_result)
        
        result = {
            "ocr_result": ocr_result
        }
        return result, "worker"
    
    
class imageAgent(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)
        
    def forward(self, messages, **kwargs):
        task = kwargs.get("task")
        imagePath = kwargs.get("imagePath")
        prompt = task
        content=[]
        content.append({"type":"text","text":prompt})
        # imagePath 有效性检查
        import requests
        def isAccessible(url):
            try:
                response = requests.get(url, timeout=5)  # 设置超时时间
                # 判断状态码是否为 200（成功）
                if response.status_code == 200:
                    return True
                else:
                    return False
            except requests.exceptions.RequestException as e:
                # 捕获所有请求异常（如超时、连接错误等）
                return False
        import os
        content=[]
        if os.path.exists(imagePath) and os.path.isfile(imagePath):
            # 本地图片处理
            # 将图像转换为Base64编码
            import base64
            
            with open(imagePath, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            content=[{
                    "type": "text",
                    "text":task
                    },                    
                    {
                        "type": "image_url",
                        "image_url": {"url": image_base64}
                    }]
            self.add_message("user", content, messages)
            from openai import OpenAI
            client = OpenAI(
                base_url='https://qianfan.baidubce.com/v2',
                api_key='bce-v3/ALTAK-4ArGT1LC7hVC6PrFjYeLR/688e8990de782f5c073eab80330b98c880f2dac5'
            )
            try:
                response = client.chat.completions.create(
                    model="ernie-4.5-8k-preview", 
                    messages=[{
                        "role":"user",
                        "content":content
                    }]
                    )
                response_data = response.choices[0].message.content
                self.log("assistant", response_data)
                result = {
                    "image_result": response_data
                }
            except Exception as e:
                errorMessage="对输入图片的要求如下：单个图片文件的大小不超过10 MB;图片数量受模型图文总 Token 上限（即最大输入）的限制，所有图片的总 Token 数必须小于模型的最大输入;"
                result = {
                    "image_result": errorMessage
                }
                raise ReportError("wrong file path", "worker")
        elif isAccessible(imagePath):
            # 网页图片处理
                content=[{
                        "type": "text",
                        "text":task
                        },                    
                        {
                            "type": "image_url",
                            "image_url": {"url": imagePath}
                        }
                        ]
                self.add_message("user", content, messages)
                from openai import OpenAI
                base_url="https://qianfan.baidubce.com/v2"
                api_key="baidu api-key"
                client = OpenAI(
                    base_url='https://qianfan.baidubce.com/v2',
                    api_key=''
                )
                response = client.chat.completions.create(
                    model="ernie-4.5-8k-preview", 
                    messages=[{
                        "role":"user",
                        "content":content
                    }]
                    )
                try:
                    response_data = response.choices[0].message.content
                    self.log("assistant", response_data)
                    result = {
                        "image_result": response_data
                    }
                except Exception as e:
                    errorMessage="对输入图片的要求如下：单个图片文件的大小不超过10 MB;图片数量受模型图文总 Token 上限（即最大输入）的限制，所有图片的总 Token 数必须小于模型的最大输入;"
                    result = {
                        "image_result": errorMessage
                    }
                    raise ReportError("wrong image url", "worker")
        else:
            result = {"image_result": "文件不存在或者链接无法访问，请提供正确的本地文件地址或者网页图片链接"}
        return result,"worker"
    
    # 可能有用的工具
    # lenso.ai
    