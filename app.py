"""
FastAPI后端服务
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os

from deepseek_client import DeepSeekClient
from prompts import PRODUCT_TO_DEV_PROMPT, DEV_TO_PRODUCT_PROMPT
from config import HOST, PORT

app = FastAPI(title="职能沟通翻译助手", description="产品与开发之间的双向翻译工具")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务（用于前端）
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 初始化DeepSeek客户端
try:
    deepseek_client = DeepSeekClient()
except ValueError as e:
    print(f"警告: {e}")
    deepseek_client = None


class TranslationRequest(BaseModel):
    """翻译请求模型"""
    content: str
    direction: str  # "product_to_dev" 或 "dev_to_product"


@app.get("/", response_class=HTMLResponse)
async def root():
    """根路径，返回前端页面"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>前端文件未找到</h1><p>请确保static/index.html文件存在</p>",
            status_code=404
        )


@app.post("/api/translate")
async def translate(request: TranslationRequest):
    """
    翻译接口（流式输出）
    
    Args:
        request: 翻译请求，包含内容和方向
        
    Returns:
        流式响应
    """
    if deepseek_client is None:
        return JSONResponse(
            content={"error": "DeepSeek API未配置，请设置DEEPSEEK_API_KEY"},
            status_code=500
        )
    
    # 根据方向选择提示词
    if request.direction == "product_to_dev":
        prompt_template = PRODUCT_TO_DEV_PROMPT
        system_message = "你是一位专业的技术翻译助手，擅长将产品需求翻译成技术语言。"
    elif request.direction == "dev_to_product":
        prompt_template = DEV_TO_PRODUCT_PROMPT
        system_message = "你是一位专业的产品翻译助手，擅长将技术方案翻译成业务语言。"
    else:
        return JSONResponse(
            content={"error": "无效的翻译方向，请使用 'product_to_dev' 或 'dev_to_product'"},
            status_code=400
        )
    
    # 构建消息
    prompt = prompt_template.format(content=request.content)
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    async def generate():
        """生成器函数，用于流式输出"""
        try:
            async for chunk in deepseek_client.chat_stream(messages):
                # 将每个chunk包装为SSE格式
                yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_msg = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error_msg}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/api/health")
async def health():
    """健康检查接口"""
    return {
        "status": "ok",
        "deepseek_configured": deepseek_client is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)

