import reflex as rx
from .pages.content import content
from .pages.about import about

class State(rx.State):
    pass

def index(): #1. add_page 방식
    return rx.heading("Hello world!")

#2. 데코레이터방식
@rx.page(route="/custom-route")
def custom():
    return rx.heading("custom route")
#3. 동적 라우팅
@rx.page(route="/[...id]/")
def dynamic_index():
    return rx.vstack(
        rx.heading(rx.State.id)
    )

app = rx.App()
app.add_page(index) #1. add_page 방식
app.add_page(about) #pages/에서 import
app.add_page(content) #pages/에서 import
