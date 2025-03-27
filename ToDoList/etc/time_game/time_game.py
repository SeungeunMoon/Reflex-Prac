from datetime import datetime as dt
import time
import reflex as rx

class State(rx.State):
    records:list = []
    raw_text: str = "hi"
    
    counter_a:int =0
    counter_b: int = 0
    
    @rx.var
    def upper_text(self) -> str:
        return self.raw_text.upper() if self.raw_text else "EMPTY"
    
    @rx.var(cache=False)
    def cur_time(self) -> str:
        now = dt.now()
        return now.strftime("%H:%M:%S") + f".{now.microsecond // 10000:02} {'신' if now.microsecond // 10000 <1 else "까비" if now.microsecond // 10000 <= 10 or now.microsecond // 10000 >= 90 else "분발!"}"

    @rx.event
    def add_record(self):
        self.records.append(self.cur_time)
        
    @rx.event
    def clear_records(self):
        self.records = []
    
    @rx.event
    def no_func(self):
        pass

    @rx.var(cache=False)
    def last_touch_time(self)->str:
        return time.strftime("%H:%M:%S")
    
    @rx.event
    def increment_a(self):
        self.counter_a += 1
    @rx.event
    def increment_b(self):
        self.counter_b += 1
    
    @rx.var()
    def last_counter_a_update(self) -> str:
        return f"{self.counter_a} at {time.strftime('%H:%M:%S')}"
    @rx.var()
    def last_counter_b_update(self) -> str:
        return f"{self.counter_b} at {time.strftime('%H:%M:%S')}"
    
    
    
    
    
@rx.page()
def index():
    return rx.container(
        rx.heading("Computed var 알아보기"),
        rx.heading(State.upper_text),
        rx.input(
            on_change=State.set_raw_text,
            placeholder="Type..."
        ),
        rx.heading("땡 맞추기 게임"),
        rx.moment(
            format="HH:mm:ss.SS",
            interval=10,
        ),
        rx.hstack(
            rx.button("RECORD", on_click=State.add_record),
            rx.button("CLEAR", on_click=State.clear_records)
        ),
        rx.foreach(
            State.records[::-1][:6], rx.text 
        ),
        rx.vstack(
            rx.heading("Caching 기능 알아보기"),
            rx.text(
                f"State touched at {State.last_touch_time}"
            ),
            rx.text(
                f"Counter A: {State.last_counter_a_update}"
            ),
            rx.text(
                f"Counter B: {State.last_counter_b_update}"
            ),
            rx.hstack(
                rx.button(
                    "A",
                    on_click=State.increment_a
                ),
                rx.button(
                    "B",
                    on_click=State.increment_b
                ),
                rx.button(
                    "N",
                    on_click=State.no_func
                )
            )
        )
    )
    
    
    
app = rx.App()
