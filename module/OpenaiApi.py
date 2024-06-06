import openai
import os
def ai(text):
    os.environ["http_proxy"] = "http://localhost:2080"
    os.environ["https_proxy"] = "http://localhost:2080"

    # optional; defaults to `os.environ['OPENAI_API_KEY']`
    openai.api_key = "sk-R7wfFDtqkbGSZFOn618007334f1c4d4b8e31Cb797568598d"

    # all client options can be configured just like the `OpenAI` instantiation counterpart
    openai.base_url = "https://free.gpt.ge/v1/"
    openai.default_headers = {"x-foo": "true"}

    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{text}",
            },
        ],
    )
    return completion.choices[0].message.content

# 正常会输出结果：Hello there! How can I assist you today ?

if __name__=="__main__":
    print(ai("写一个冒泡算法"))