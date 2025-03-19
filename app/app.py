import reflex as rx
import random

class State(rx.State):
    def download_random_data(self):
        return rx.download(
            data=",".join(
                [str(random.randint(0,100)) for _ in range(100)]
            ),
            filename="random_numbers.csv",
        )
        
    @rx.event
    async def handle_upload(self, files:list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

meta = [
    {"name": "theme_color", "content": "#FFFFFF"},
    {"char_set": "UTF-8"},
    {"property": "og:url", "content": "url"},
    {"property": "og:title", "content":"og 제목입력"},
    {"property": "og:description", "content":"og 설명입력"} 
]

@rx.page(
    title = "My App",
    description = "A app built with Reflex",
    image ="/splash.png",
    meta=meta
)
def index():
    return rx.vstack(
        rx.heading("이미지 다운로드"),
        rx.link(
            "DOWNLOAD",
            title="클릭 시 다운로드 시작",
            href="/logo.jpge"
        ),
        rx.button("DOWNLOAD", 
                  on_click=rx.download(
                      url="/ex1.jpeg",
                      filename="new_name.jpeg"))
        ,rx.heading("랜덤 숫자 생성")
        ,rx.button(
            "Download Random Nums",
            on_click=State.download_random_data,
        )
        ,rx.upload("Drag and drop files here or clock to select files",id="upload1"),
        rx.foreach(rx.selected_files("upload1"), rx.text),
        rx.button("UPLOAD",
                  on_click=State.handle_upload(rx.upload_files(upload_id="upload1")))
        
        
    )

@rx.page(title="About Page")
def about():
    return rx.text("About Page")


app= rx.App(
    head_components=[
        rx.el.link(rel="canonical", href="https://example.com/page")
    ]
)