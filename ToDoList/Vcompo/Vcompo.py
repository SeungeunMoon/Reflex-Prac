import reflex as rx
from datetime import datetime
import asyncio

class State(rx.State):
  date_now: datetime = datetime.now()
  updating: bool = False
  value: int = 0
  b1_loading: bool = True
  b2_loading: bool = True
  
  @rx.event
  def on_update(self, date):
    return rx.toast(f"DATE updated: {date}")

  @rx.event(background=True)
  async def start_progress(self):
    async with self:
      self.value = 0
    while self.value < 100:
      await asyncio.sleep(0.1)
      async with self:
        self.value += 1
  @rx.event
  async def is_complete(self):
    await asyncio.sleep(3)
    self.b1_loading = False
    self.b2_loading = False
    
@rx.page(on_load=State.is_complete)
def index():
  return rx.center(
    rx.vstack(
        rx.avatar(
          fallback="iloc",
          color_scheme="amber"
        ),
        rx.badge(
              "BADGE",
              size="3",
              variant="outline",
        ),
        rx.badge(
          rx.flex(
            rx.icon(tag="arrow_up"),
            rx.text("9.9%"),
            spacing="1"
          ),
          color_scheme="grass"
        ),
        rx.callout(
          "WARNING", 
          icon="triangle_alert",
          color_scheme="red", role="alert"
        ),
        rx.callout(
          "D_DAY", icon="calendar", color_scheme="cyan"
        ),
        rx.card(
          rx.data_list.root(
            rx.data_list.item(
              rx.data_list.label("Status"),
              rx.data_list.value(
                rx.badge(
                  "Authorized",
                  variant="soft",
                  radius="full",
                            )
                        ),
              align="center",
            ),
            rx.data_list.item(
              rx.data_list.label("ID"),
              rx.data_list.value(rx.code("U-3293"),)
            ),
            rx.data_list.item(
              rx.data_list.label("name"),
              rx.data_list.value("Developer Success"),
              align="center"),   
          )
        ),
        rx.vstack(
          rx.list.ordered(items=['a','b','c']),
          rx.list.unordered(
            rx.list.item("Ex 1"),
            rx.list.item("Ex 2")
          ),
          rx.list(
            rx.list.item(rx.icon("circle_check_big", color="green"), "Allowed"),
          )
        ),
        rx.vstack(
          rx.moment(State.date_now, tz="Asia/Seoul", format="YYYY-MM-DD HH:mm:ss"),
          rx.moment(State.date_now, add=rx.MomentDelta(months=2), format="2개월 전: YYYY-MM-DD"),
          rx.moment(State.date_now, from_now=True)
        ),
        rx.card(
          rx.moment(interval=1000, format="HH:mm:ss", color="blue"),
          text_algin = "center", width="60%"
        ),
        rx.hstack(
          rx.moment(
            format="HH:mm:ss", interval = rx.cond(State.updating, 5000, 0), on_change=State.on_update
          ),
          rx.switch(
            is_checked=State.updating, on_change=State.set_updating 
          ),
        ),
        rx.hstack(
          rx.progress(value=State.value, size="3"),
          rx.button("Start", on_click=State.start_progress,),
          width ="80%", align="center"
        ),
        rx.scroll_area(
          rx.flex(
            rx.text("asdfasdfasdf"),
            rx.text("Asdfasdfasd")
          ),
          type="always", scrollbars="vertical", style={"height":100}
        ),
        rx.button("Bookmark", loading=State.b1_loading),
        rx.button("Bookmark", rx.spinner(loading=State.b2_loading), disabled=State.b2_loading)
      )
  )


app = rx.App()