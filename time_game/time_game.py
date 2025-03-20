from datetime import datetime as dt
import reflex as rx

class State(rx.State):
    records:list = []
    raw_text: str = "hi"
    
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

@rx.page()
def index():
    return rx.container(
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
        )
    )
    
    
    
app = rx.App()
