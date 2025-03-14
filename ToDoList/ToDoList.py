import reflex as rx

class State(rx.State):
    text: str
    todo:list[str] = ["영어공부", "운동"]
    completed: list[bool] = [False, False]
    on_edit: list[bool] = [False, False]
    
    def add_todo(self):
        self.todo = self.todo + [self.text]
        self.completed = self.completed + [False]
        self.on_edit = self.on_edit + [False]

    def set_todo(self,value):
        self.text = value
    
    def pop_todo(self, idx: int):
        self.todo.pop(idx)
        self.completed.pop(idx)
        self.on_edit.pop(idx)
        
    def toggle(self,idx: int):
        self.completed[idx] = not self.completed[idx]

    def toggle_edit(self, idx):
        self.on_edit[idx] = not self.on_edit[idx]
        
    def update_todo(self, x:dict[str:str]):
        i, val = x.popitem()  
        i = int(i)  
        self.todo[i] = val
        self.on_edit[i] = False

def render_fn(item, idx):
    return rx.hstack(
        rx.cond(
            State.completed[idx],
            rx.icon("circle-check-big", size=10, on_click=lambda: State.toggle(idx)),
            rx.icon("circle",size=10, on_click=lambda: State.toggle(idx))
        ),
        rx.cond(
            State.completed[idx],
            rx.text(item, style={"text-decoration": "line-through"}),
            rx.cond(
                State.on_edit[idx],
                rx.form(
                    rx.input(default_value=item, autofocus=True,
                             on_change=State.set_todo, name=idx.to_string()),
                    on_submit=lambda e:State.update_todo(e),
                    reset_on_submit=True
                ),
                rx.text(item, on_click=lambda: State.toggle_edit(idx))
            ),
        ),

        rx.icon("trash-2", on_click=lambda: State.pop_todo(idx)),   
        align='center'
    )
        

def index():
    return rx.container(
        rx.form(
            rx.input(on_change=State.set_todo),
            on_submit = lambda x: State.add_todo(),
            reset_on_submit=True
        ),
        rx.button("추가", on_click=State.add_todo),
        rx.vstack(
        rx.foreach(State.todo, 
            lambda val, idx: render_fn(val, idx),
        )
            )
    )
    
    
app = rx.App()
app.add_page(index)