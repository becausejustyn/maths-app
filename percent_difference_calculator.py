from shiny import ui, render
# import polars as pl

# UI for percentage difference calculator
percent_diff_ui = ui.page_fluid(
    ui.h2("Percentage Difference Calculator"),
    ui.page_sidebar(
        ui.sidebar(
            ui.input_numeric("start_num", "Starting Number", value=100),
            ui.input_numeric("new_num", "New Number", value=150),
            ui.input_action_button("calculate", "Calculate", class_="btn-primary"),
        ),
        ui.output_ui("result"),
        ui.output_text("explanation")
    ),
)

def percent_diff_server(input, output, session):
    @output
    @render.ui
    def result():
        if not input.calculate():
            return ui.p("Press Calculate to see results")
            
        start = input.start_num()
        new = input.new_num()
        
        if start == 0:
            return ui.p("Cannot calculate percentage difference when starting number is zero.", class_="text-danger")
        
        percent_diff = ((new - start) / abs(start)) * 100
        
        # Determine style based on value
        #match percent_diff:
        #    case diff if diff > 0:
        #        style = {"color_class": "text-success", "icon": "↑"}
        #    case diff if diff < 0:
        #        style = {"color_class": "text-danger", "icon": "↓"}
        #    case _:
        #        style = {"color_class": "text-muted", "icon": "→"}
        if percent_diff > 0:
            style = {"color_class": "text-success", "icon": "↑"}
        elif percent_diff < 0:
            style = {"color_class": "text-danger", "icon": "↓"}
        else:
            style = {"color_class": "text-muted", "icon": "→"}
            
        return ui.div(
            ui.h3(f"{style['icon']} {percent_diff:.2f}%", class_=style["color_class"]),
            ui.p(f"Changed from {start} to {new}")
        )
    
    @output
    @render.text
    def explanation():
        if not input.calculate():
            return ""
            
        start = input.start_num()
        new = input.new_num()
        
        if start == 0:
            return ""
            
        percent_diff = ((new - start) / abs(start)) * 100
            
        return f"""
        Formula used: ((New Number - Starting Number) / |Starting Number|) × 100
        
        Calculation:
        ((({new} - {start}) / |{start}|) × 100 = {percent_diff:.2f}%
        """
