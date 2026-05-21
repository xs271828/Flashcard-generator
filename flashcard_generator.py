import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com",
)


def generate_question(answer: str, context: str) -> dict:
    """使用 DeepSeek API，根据关键词和上下文生成问答闪卡。"""

    if answer.lower() not in context.lower():
        raise ValueError(f"关键词 '{answer}' 在文本中未找到，请检查输入。")

    prompt = f"""你是一个专业的阅读理解出题助手。
请根据以下【文章内容】和【关键词】，生成一道高质量的问答题。

【关键词】：{answer}
【文章内容】：
{context[:3000]}

要求：
- 问题要围绕关键词，考查对文章的理解
- 答案要简洁准确，直接来自文章
- 用中文输出（如文章是英文则用英文）

请严格按以下 JSON 格式返回，不要输出其他内容：
{{"question": "问题内容", "answer": "答案内容"}}"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=256,
    )

    raw = response.choices[0].message.content.strip()

    # 去掉可能的 markdown 代码块
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    return {"question": result["question"], "answer": result["answer"]}
