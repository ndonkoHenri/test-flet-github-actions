
import flet as ft
import xlwings as xw



def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("Playground"))
    page.horizontal_alignment = page.vertical_alignment = "center"

    def test():
        page.add(ft.Text("starting..."))
        # Create a new Excel app (visible so you can see it working)
        app = xw.App(visible=True)

        # Add a new workbook
        wb = app.books.add()

        # Select first sheet
        sheet = wb.sheets[0]

        # Write something into cell A1
        sheet.range("A1").value = "xlwings is working!"

        # Save the file (optional)
        wb.save("xlwings_test.xlsx")

        # Close workbook
        wb.close()

        # Quit Excel
        app.quit()
        page.add(ft.Text("quit..."))

    page.add(
        ft.SafeArea(
            content=ft.TextButton(f"Hello, xlwings v{xw.__version__}!", on_click=test),
        )
    )


ft.run(main)


