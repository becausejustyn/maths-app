from shiny import App, ui, render
import polars as pl

app_ui = ui.page_fluid(
    ui.h1("Percentage Difference Calculator"),
    ui.page_sidebar(
        ui.sidebar(
            ui.input_numeric("starting_number", "Starting Number", value=100),
            ui.input_numeric("new_number", "New Number", value=120),
            ui.input_action_button("calculate", "Calculate", class_="btn-primary"),
        ),
        ui.output_ui("result"),
        ui.output_text("explanation")
    )
)

def server(input, output, session):
    @output
    @render.ui
    def result():
        if input.calculate():
            starting = input.starting_number()
            new = input.new_number()
            
            if starting == 0:
                return ui.p("Cannot calculate percentage difference when starting number is zero.", class_="text-danger")
            
            # Using Polars expressions for calculation
            df = pl.DataFrame({
                "starting": [starting],
                "new": [new]
            })
            
            df = df.with_columns(
                percent_diff = ((pl.col("new") - pl.col("starting")) / pl.col("starting").abs()) * 100
            )
            
            percent_diff = df["percent_diff"][0]
            
            if percent_diff > 0:
                color_class = "text-success"
                icon = "↑"
            elif percent_diff < 0:
                color_class = "text-danger"
                icon = "↓"
            else:
                color_class = "text-muted"
                icon = "→"
                
            return ui.div(
                ui.h3(f"{icon} {percent_diff:.2f}%", class_=color_class),
                ui.p(f"Changed from {starting} to {new}")
            )
        
        return ui.p("Press Calculate to see results")
    
    @output
    @render.text
    def explanation():
        if input.calculate():
            starting = input.starting_number()
            new = input.new_number()
            
            if starting == 0:
                return ""
                
            # Using Polars for calculation
            df = pl.DataFrame({
                "starting": [starting],
                "new": [new]
            })
            
            df = df.with_columns(
                percent_diff = ((pl.col("new") - pl.col("starting")) / pl.col("starting").abs()) * 100
            )
            
            percent_diff = df["percent_diff"][0]
                
            return f"""
            Formula used: ((New Number - Starting Number) / |Starting Number|) × 100
            
            Calculation:
            ((({new} - {starting}) / |{starting}|) × 100 = {percent_diff:.2f}%
            """

app = App(app_ui, server)