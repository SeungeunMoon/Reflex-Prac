import reflex as rx
import asyncio
from time import sleep

class State(rx.State):
    answer: str
    count: int = 0
    
    def d_redirect(self):
        if self.answer.strip() == 'answer':
            return rx.redirect("/right",is_external=True)
        else:
            return rx.redirect("/wrong")
    
    def set_count(self, value):
        self.count = int(value)
    
    @rx.event(background=True)
    async def countdown(self):
        while self.count >= -1:
            async with self: #exclusive lock
                await asyncio.sleep(1)
                self.count -= 1
                if self.count < 0:
                    self.count = 0
                yield


    @rx.event
    def reset_count(self):
        self.set_count(0),
        return rx.set_value("c_sec", "")


@rx.page("/wrong")
def hidden():
    return rx.vstack(
        rx.heading("Wrong, keep it up")
    )
@rx.page("/right")
def hidden():
    return rx.vstack(
        rx.heading("Correct!")
    )
@rx.page("/")
def index():
    return rx.container(
        rx.text("정답은???"),
        rx.input(
            on_change=State.set_answer,
            on_blur=State.d_redirect),
        rx.vstack(
            rx.text(State.count),
            rx.input(
                placeholder="몇 초를 카운트 할까요?",
                on_change=lambda v: State.set_count(v), id="c_sec"),
            rx.button("COUNTDOWN", on_click=State.countdown),
            rx.button("INITIALIZE", on_click=State.reset_count)
        )
        )
    

app = rx.App()