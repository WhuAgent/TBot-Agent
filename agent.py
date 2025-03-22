from agent_network.base import BaseAgent
from agent_network.exceptions import ReportError
import os


class worker(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)
        
    def forward(self, messages, **kwargs):
        if error_message := kwargs.get("graph_error_message"):
            prompt = f"错误：{error_message}"
        else:
            task = kwargs.get("task")
            prompt = task
            
            if ocr_result := kwargs.get("ocr_result"):
                prompt += f"\n\n相关文件的文字识别结果为 {ocr_result}"
                
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


class pdf_worker(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)

    def forward(self, messages, **kwargs):
        if error_message := kwargs.get("graph_error_message"):
            prompt = f"错误：{error_message}"
        else:
            task = kwargs.get("task")
            prompt = task

            if pdf_text := kwargs.get("pdf_text"):
                prompt += f"\n\n相关文件的文本识别结果为 {pdf_text}"
            if pdf_table := kwargs.get("pdf_table"):
                prompt += f"\n\n相关文件的表格识别结果为 {pdf_table}"
            if pdf_image_list := kwargs.get("pdf_image_list"):
                prompt += f"\n\n图片提取完成，相关文件的图片保存目录为 {pdf_image_list}"

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


# 提取PDF文本内容的文件
class pdf_extract_text(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)

    def forward(self, messages, **kwargs):
        # 检查参数
        pdf_file_name = kwargs.get("pdf_file_name")
        if not pdf_file_name:
            raise ReportError("pdf_file_name is not provided", "pdf_worker")
        if not os.path.exists(pdf_file_name):
            raise ReportError("pdf_file_name is not exist", "pdf_worker")

        import pdfplumber
        # 提取pdf文本
        pdf_text = ""
        with pdfplumber.open(pdf_file_name) as pdf:
            for page in pdf.pages:
                pdf_text = pdf_text + "\n" + page.extract_text()
        self.log("assistant", pdf_text)

        result = {
            "pdf_text": pdf_text
        }

        return result, "pdf_worker"


# pdf提取表格内容
class pdf_extract_table(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)

    def forward(self, messages, **kwargs):
        # 检查参数
        pdf_file_name = kwargs.get("pdf_file_name")
        if not pdf_file_name:
            raise ReportError("pdf_file_name is not provided", "pdf_worker")
        if not os.path.exists(pdf_file_name):
            raise ReportError("pdf_file_name is not exist", "pdf_worker")

        import pdfplumber
        from tabulate import tabulate
        # 提取pdf表格
        pdf_table = ''
        with pdfplumber.open(pdf_file_name) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    pdf_table = pdf_table + "\n\n" + tabulate(table, tablefmt="grid")

        self.log("assistant", pdf_table)

        result = {
            "pdf_table": pdf_table
        }

        return result, "pdf_worker"


class pdf_extract_image(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)

    def forward(self, messages, **kwargs):
        # 检查参数
        pdf_file_name = kwargs.get("pdf_file_name")
        if not pdf_file_name:
            raise ReportError("pdf_file_name is not provided", "pdf_worker")
        if not os.path.exists(pdf_file_name):
            raise ReportError("pdf_file_name is not exist", "pdf_worker")

        # 提取pdf图片
        output_dir = 'D:\\study\\test-agent\\images'
        self.extract_images_from_pdf(pdf_file_name, output_dir)
        self.log("assistant", output_dir)

        result = {
            "pdf_image_list": output_dir
        }

        return result, "pdf_worker"

    def extract_images_from_pdf(self, pdf_file_name, output_folder):
        import fitz
        # 检查输出文件夹是否存在，若不存在则创建
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 打开PDF文件
        pdf = fitz.open(pdf_file_name)

        # 遍历PDF的每一页
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            # 获取当前页面中的所有图片信息
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list, start=1):
                # 获取图片的XREF编号
                xref = img[0]
                # 提取图片的二进制数据
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]
                # 获取图片的扩展名
                image_ext = base_image["ext"]
                # 构建图片的保存路径
                image_name = f'page_{page_num + 1}_image_{img_index}.{image_ext}'
                image_path = os.path.join(output_folder, image_name)

                # 将图片保存到本地
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_bytes)

        # 关闭PDF文件
        pdf.close()