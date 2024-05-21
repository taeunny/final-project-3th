import json
import requests
import gradio as gr
BACKEND_URL = ""

def res(message: str, history, tone: str) -> str:
    payload = {"msg": message,
               "tone": tone,
               }
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
        submit_btn="보내기",
        retry_btn="다시 보내기 ↩",
        undo_btn="이전 대화 삭제 ❌",
        clear_btn="전체 대화 삭제 💫",
        additional_inputs=
            gr.Radio(choices=["멘토스", "전문적인 상담사", "문어체", "안드로이드", "아재", "entp", "할아버지", "나루토", "선비", "소심한"], label="말투 선택", value="멘토스"),
        additional_inputs_accordion_name ="말투를 변경하고 싶으시면 클릭해주세요😀",
        )

demo.queue().launch(debug=True, share=True)
