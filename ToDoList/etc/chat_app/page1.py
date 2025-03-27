import reflex as rx

@rx.page(route="1", title="page1")
def page_1():
    return rx.text("PAGE 1")