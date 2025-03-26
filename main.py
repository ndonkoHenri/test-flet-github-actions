
import flet as ft

import flet_permission_handler as fph


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.appbar = ft.AppBar(title=ft.Text("PermissionHandler Tests"))
    ph = fph.PermissionHandler()
    page.overlay.append(ph)

    def check_permission(e):
        o = ph.check_permission(e.control.data)
        page.add(ft.Text(f"Checked {e.control.data.name}: {o}"))

    def request_permission(e):
        o = ph.request_permission(e.control.data)
        page.add(ft.Text(f"Requested {e.control.data.name}: {o}"))

    def open_app_settings(e):
        o = ph.open_app_settings()
        page.add(ft.Text(f"App Settings: {o}"))

    page.add(
        ft.OutlinedButton(
            "Check Microphone Permission",
            data=fph.PermissionType.MICROPHONE,
            on_click=check_permission,
        ),
        ft.OutlinedButton(
            "Request Microphone Permission",
            data=fph.PermissionType.MICROPHONE,
            on_click=request_permission,
        ),
        ft.OutlinedButton(
            "Open App Settings",
            on_click=open_app_settings,
        ),
    )


ft.app(main)


