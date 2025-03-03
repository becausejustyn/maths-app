from shiny import App, ui
from percent_difference_calculator import percent_diff_ui, percent_diff_server
from llm_gpu_calculator import gpu_calc_ui, gpu_calc_server

# Create the main app with navbar
app_ui = ui.page_navbar(
    ui.nav_panel("Percentage Difference Calculator", percent_diff_ui),
    ui.nav_panel("LLM GPU Memory Calculator", gpu_calc_ui),
    title="Model Calculators"
)

def server(input, output, session):
    # Import server functions from each module
    percent_diff_server(input, output, session)
    gpu_calc_server(input, output, session)

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()