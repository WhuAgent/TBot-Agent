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
            if calculator_result := kwargs.get("calculator_result"):
                prompt += f"\n\n精确计算得到的结果为 {calculator_result}"
                
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
    
class calculator_tool(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)
        self.tools=[
            {
                "type": "function",
                "function": {
                    "name": "devid",
                    "description": "计算两个数相除",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "num1": {
                                "type": "string",
                                "description": "被除数",
                            },
                            "num2": {
                                "type": "string",
                                "description": "除数",
                            }
                        },
                        "required": ["num1","num2"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add",
                    "description": "计算两个数相加",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "num1": {
                                "type": "string",
                                "description": "加数",
                            },
                            "num2": {
                                "type": "string",
                                "description": "加数",
                            }
                        },
                        "required": ["num1","num2"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "minus",
                    "description": "计算两个数相减",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "num1": {
                                "type": "string",
                                "description": "被减数",
                            },
                            "num2": {
                                "type": "string",
                                "description": "减数",
                            }
                        },
                        "required": ["num1","num2"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "mult",
                    "description": "计算两个数相乘",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "num1": {
                                "type": "string",
                                "description": "乘数",
                            },
                            "num2": {
                                "type": "string",
                                "description": "乘数",
                            }
                        },
                        "required": ["num1","num2"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "sum",
                    "description": "计算一列数据相加",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "allNums": {
                                "type": "string",
                                "description": "一列字符串表示的数据，比如\"[1.23, 4.56, 7.89]\"",
                            }
                        },
                        "required": ["allNums"]
                    }
                }
            },
        ]
        
    def call_function(self,tool):
        import json
        from decimal import Decimal,getcontext
        import ast
        
        getcontext().prec=8
        
        function=tool.function
        function_name=function.name
        if function_name == "devid":
            function_args = json.loads(function.arguments)
            num1=function_args.get("num1")
            num2=function_args.get("num2")
            return Decimal(num1)/Decimal(num2)
        elif function_name == "add":
            function_args = json.loads(function.arguments)
            num1=function_args.get("num1")
            num2=function_args.get("num2")
            return Decimal(num1)+Decimal(num2)
        elif function_name == "minus":
            function_args = json.loads(function.arguments)
            num1=function_args.get("num1")
            num2=function_args.get("num2")
            return Decimal(num1)-Decimal(num2)
        elif function_name == "mult":
            function_args = json.loads(function.arguments)
            num1=function_args.get("num1")
            num2=function_args.get("num2")
            return Decimal(num1)*Decimal(num2)
        elif function_name == "sum":
            function_args = json.loads(function.arguments)
            num1=function_args.get("allNums")
            paesed_list=ast.literal_eval(num1)
            decimal_list=[Decimal(str(item)) for item in paesed_list]
            return sum(decimal_list)
        else:
            return None
            
        
    def callLlm(self,messages,api_key,base_url,model):
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        openai_messages = []
        for message in messages:
            openai_messages.append(message.to_openai_message())
        response = client.chat.completions.create(
            model=model,
            messages=openai_messages,
            tools=self.tools
        )
        return response.choices[0].message
        
    def forward(self, messages, **kwargs):
        task = kwargs.get("computeTask")
        prompt = task+"请选择你要调用的工具，你必须要调用一个工具来获得结果"
        self.add_message("user", prompt, messages)
        message=self.callLlm(messages,
                        api_key="sk-ca3583e3026949299186dcbf3fc34f8c",
                        base_url="https://api.deepseek.com",
                        model="deepseek-chat",
                        )
        callculate_result=""
        if message.tool_calls:
            tool=message.tool_calls[0]
            compute_result=self.call_function(tool)
            callculate_result= "精确计算得到的结果是："+str(compute_result)
        else:
            callculate_result = str(message.content)
        self.log("assistant", callculate_result)
        result={
            "calculator_result": callculate_result
        }
        return result, "worker"