# Aeromat AI

材料科学智能教学助手

## 学生使用（无需打包）

1. 确保安装了 Python 3.8+（https://www.python.org/downloads/）
2. **双击 `run.bat`**
3. 首次运行自动安装依赖
4. 浏览器打开 http://localhost:8501

## 可选：启用云端LLM

```cmd
set DASHSCOPE_API_KEY=你的通义千问密钥
run.bat
```

## 更新知识库

在 `knowledge/docs/` 或 `knowledge/faqs/` 中添加 .md 文件即可。

## 教师打包（可选）

如需生成 exe 分发给学生，运行：
```
python build.py
```

输出目录：`dist/AeromatAI/`