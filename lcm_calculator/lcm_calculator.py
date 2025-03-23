import reflex as rx
import math

class State(rx.State):
    answer: str
    
    @rx.event
    def calculator(self, x):
        nums = x["n"]
        
        cal = math.lcm(*[int(i) for i in nums.strip().split(" ")])
        self.answer = f"{cal:,}"

@rx.page(on_load=rx.set_focus('n'))
def index():
    return rx.vstack(
        rx.heading("최소공배수 계산기"),
        rx.text("띄어쓰기로 구분하여 두 개 이상의 자연수를 입력해주세요."),
        rx.form(
            rx.input(placeholder="입력 후 엔터", name='n',id='n'),
            on_submit= State.calculator,
            reset_on_submit=True,
        ),
        rx.text("최소공배수는 ",State.answer," 입니다.")
    )
    
    
app = rx.App()