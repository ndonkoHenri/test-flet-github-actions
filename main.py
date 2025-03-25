import sys

# from core.config import ConfigApp
import flet as ft

if sys.platform == "emscripten":
    import packages.flet_easy as fs
else:
    import flet_easy as fs
app = fs.FletEasy(route_init="/")



async def home(data: fs.Datasy):
    page = data.page

    async def navbar_click(e: ft.ControlEvent):
        print("navbar_click")

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="首页",
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME_FILLED,
            ),
            ft.Divider(),
        ],
        on_change=navbar_click,
    )
    page.drawer = drawer
    appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_size=27,
            on_click=lambda _: page.open(drawer),
            offset=ft.Offset(x=0.1, y=0),
        ),
        leading_width=30,
        title=ft.Text("首页"),
        center_title=False,
        bgcolor=ft.Colors.BLUE,
        actions=[
            ft.IconButton(ft.Icons.SEARCH, tooltip="搜索"),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="导入向导", on_click=data.go("/welcome")),
                    ft.PopupMenuItem(),  # divider
                ],
                tooltip="选项",
            ),
        ],
    )

    # async def load_msg(page: ft.Page):
        

    # await load_msg(data, page, mainview, dialog, drawer, appbar)

    return ft.View(
        appbar=appbar,
        drawer=drawer,
    )

# We define the routes of the application.
app.add_routes(
    [
        fs.Pagesy("/",home, title="Qviewer | 首页"),

    ]
)


# We run the application
app.run()
