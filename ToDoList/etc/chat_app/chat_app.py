import reflex as rx
from .page1 import page_1
from openai import OpenAI, AsyncOpenAi

class State(rx.State):
    q: str
    qa_list: list[list[str]] = \
        [
            ["1+1=", "11입니다"],
            ["3.9와 3.11 중에 어느게 크지?", "3.11입니다."]
        ]
    
    async def append_qa(self, d):
        self.q = d["q"]
        self.answer = ""
        
        self.qa_list.append(
            [self.q, self.answer]
        )
        
        client = AsyncOpenAi()
        session = await client.chat.completions.create(
            messages=[{
                "role":"user",
                "content":self.q,
            }],
            model="gpt-4o-mini",
            stop=None,
            stream=True
        )
        yield
        
        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    break
                self.answer += item.choices[0].delta.content
                self.qa_list[-1][1] = self.answer
                yield
        

def qa(qna):
    return rx.box(
        rx.box(qna[0],
               background_color = "green",
               text_align="right"),
        rx.box(qna[1],
               background_color="orange",
               text_align="left")
    )


@rx.page()
def index() -> rx.Component:
    return rx.container(
        rx.foreach(State.qa_list, qa),
        rx.form(
            rx.input(
                placeholder="write a question",
                name="q"
            ),
            on_submit=lambda e: State.append_qa(e),
            #State.append_qa가 사용자입력 데이터를 {"q": 사용자입력} 사전으로 받아서 처리하게 됩니다.
            reset_on_submit=True
        )
    )

app = rx.App()