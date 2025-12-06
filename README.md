# 职能沟通翻译助手

一个基于DeepSeek大模型的智能翻译工具，帮助产品经理和开发工程师之间进行更顺畅的沟通。支持双向翻译：将产品需求翻译为技术语言，将技术方案翻译为业务语言。

## ✨ 功能特性

- 🔄 **双向翻译**：支持产品→开发和开发→产品两个方向的翻译
- 🌊 **流式输出**：实时显示AI生成过程，提升用户体验
- 🎨 **简洁界面**：现代化的Web界面，操作简单直观
- ⚡ **快速响应**：基于FastAPI的高性能后端服务
- 🧠 **智能理解**：使用DeepSeek大模型，准确理解上下文

## 📋 项目结构

```
.
├── app.py                 # FastAPI后端主程序
├── deepseek_client.py     # DeepSeek API客户端（支持流式）
├── prompts.py            # 提示词模板
├── config.py             # 配置文件
├── requirements.txt      # Python依赖
├── env.example           # 环境变量示例
├── static/
│   └── index.html       # 前端界面
├── test_cases.md        # 测试用例
└── README.md            # 本文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 确保已安装Python 3.8+
pip install -r requirements.txt
```

### 2. 配置API Key

复制环境变量示例文件并填入你的DeepSeek API Key：

```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

编辑 `.env` 文件，填入你的API Key：

```env
DEEPSEEK_API_KEY=your_actual_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
```

> 💡 **获取API Key**：访问 [DeepSeek官网](https://www.deepseek.com/) 注册账号并获取API Key

### 3. 运行项目

```bash
python app.py
```

或者使用uvicorn直接运行：

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问应用

打开浏览器访问：http://localhost:8000

## 📖 使用说明

### 产品需求 → 开发视角

1. 选择"📱 产品 → 开发"方向
2. 在输入框中粘贴产品需求描述
3. 点击"开始翻译"按钮
4. 查看实时生成的翻译结果

**翻译结果包含：**
- 推荐算法类型建议
- 数据来源和处理方式
- 性能和实时性要求
- 预估开发工作量

### 开发方案 → 产品视角

1. 选择"💻 开发 → 产品"方向
2. 在输入框中粘贴技术方案描述
3. 点击"开始翻译"按钮
4. 查看实时生成的翻译结果

**翻译结果包含：**
- 对用户体验的实际影响
- 支持的业务增长空间
- 成本降低的商业价值

## 🧪 测试用例

项目包含2个测试用例，详见 `test_cases.md` 文件：

1. **测试用例1**：产品需求翻译为开发视角
2. **测试用例2**：技术方案翻译为产品视角

运行测试：
1. 启动服务
2. 访问 http://localhost:8000
3. 按照 `test_cases.md` 中的内容进行测试

## 🎯 提示词设计思路

### 设计原则

1. **角色定位明确**：明确AI的角色（技术翻译助手/产品翻译助手）
2. **输出结构化**：要求输出包含特定的要点，确保信息完整
3. **语言风格适配**：技术语言专业但易懂，业务语言通俗易懂
4. **上下文理解**：提示词引导AI理解输入内容的上下文

### 产品→开发提示词要点

```
- 角色：技术翻译助手
- 输出要求：
  1. 推荐算法类型建议
  2. 数据来源和处理方式
  3. 性能和实时性要求
  4. 预估开发工作量
- 语言风格：专业但易懂的技术语言
```

### 开发→产品提示词要点

```
- 角色：产品翻译助手
- 输出要求：
  1. 对用户体验的实际影响
  2. 支持的业务增长空间
  3. 成本降低的商业价值
- 语言风格：通俗易懂的业务语言，避免技术术语
```

### 提示词优化建议

- **迭代优化**：根据实际使用效果，不断优化提示词
- **示例引导**：可以在提示词中加入示例，提升输出质量
- **长度控制**：提示词要清晰简洁，避免过于冗长
- **参数调整**：可以通过调整temperature等参数控制输出风格

## 🔧 技术架构

### 后端技术栈

- **FastAPI**：现代化的Python Web框架，支持异步和流式响应
- **httpx**：异步HTTP客户端，用于调用DeepSeek API
- **python-dotenv**：环境变量管理

### 前端技术栈

- **原生HTML/CSS/JavaScript**：无需额外依赖，轻量高效
- **Fetch API + Stream**：实现流式数据接收和显示

### 核心功能实现

1. **流式输出**：使用Server-Sent Events (SSE)实现实时数据传输
2. **API调用**：异步调用DeepSeek API，支持流式响应
3. **错误处理**：完善的错误捕获和用户提示

## 📝 API接口说明

### POST /api/translate

翻译接口，支持流式输出。

**请求体：**
```json
{
  "content": "要翻译的内容",
  "direction": "product_to_dev"  // 或 "dev_to_product"
}
```

**响应：**
Server-Sent Events (SSE) 流式响应，每个chunk格式：
```
data: {"content": "翻译文本片段"}
```

### GET /api/health

健康检查接口。

**响应：**
```json
{
  "status": "ok",
  "deepseek_configured": true
}
```

## 🐛 常见问题

### 1. API Key未配置

**错误信息**：`请设置DEEPSEEK_API_KEY环境变量`

**解决方法**：
- 确保已创建 `.env` 文件
- 检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 是否正确设置
- 重启服务

### 2. 翻译失败

**可能原因**：
- API Key无效或过期
- 网络连接问题
- API调用频率限制

**解决方法**：
- 检查API Key是否有效
- 检查网络连接
- 稍后重试

### 3. 前端页面无法访问

**解决方法**：
- 确保服务已启动（检查终端输出）
- 检查端口8000是否被占用
- 尝试访问 http://127.0.0.1:8000

## 🔒 安全建议

1. **保护API Key**：不要将 `.env` 文件提交到版本控制系统
2. **生产环境**：建议使用环境变量或密钥管理服务
3. **HTTPS**：生产环境建议使用HTTPS加密传输

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📮 联系方式

如有问题或建议，请提交Issue。

---

**祝使用愉快！** 🎉

