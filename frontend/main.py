import json
import requests
import gradio as gr
BACKEND_URL = ""

def res(message: str, history: list) -> str:
    payload = {"msg": message}
    response = requests.post(
        BACKEND_URL + "/counselor", data=json.dumps(payload)
    ).json()
    answer = response["result"]
    return answer

demo = gr.ChatInterface(
        fn=res,
        textbox=gr.Textbox(placeholder="고민을 얘기해주세요🙌", container=False, scale=1),
        title="멘토스(Mental Mate Talk on Support)",
        description="멘토스는 당신의 고민을 들어주며 격려해주는 상담친구에요😊",
        theme="soft",
        examples=[["나 우울해"], ["너무 짜증나"], ["사는게 쉽지않아"]],
        retry_btn="다시보내기 ↩",
        undo_btn="이전챗 삭제 ❌",
        clear_btn="전챗 삭제 💫"
)

demo.queue().launch(debug=True, share=True)
