from shiny import ui, render

# UI for LLM GPU memory calculator
gpu_calc_ui = ui.page_fluid(
    ui.h2("LLM GPU Memory Calculator"),
    ui.page_sidebar(
        ui.sidebar(
            ui.input_numeric("model_size", "Model Size (in billions)", value=7),
            ui.input_select("quantization", "Quantization (bits)", 
                          {"16": "16-bit (FP16/BF16)", 
                           "8": "8-bit (INT8)", 
                           "4": "4-bit (INT4)"},
                          selected="16"),
            ui.input_slider("overhead", "Memory Overhead Factor", min=1.0, max=1.5, value=1.2, step=0.05),
            ui.input_action_button("calculate_gpu", "Calculate", class_="btn-primary"),
        ),
        ui.output_ui("gpu_result"),
        ui.output_text("gpu_explanation")
    ),
)

def gpu_calc_server(input, output, session):
    @output
    @render.ui
    def gpu_result():
        if not input.calculate_gpu():
            return ui.p("Press Calculate to see results")
            
        P = input.model_size()  # billions of parameters
        Q = int(input.quantization())  # bits for quantization
        overhead = input.overhead()  # overhead factor
        
        # Calculate GPU memory in GB
        memory_gb = (P * Q / 8) * overhead
        
        # Determine if the memory is sufficient for common GPUs
        gpu_tiers = [
            {"name": "NVIDIA RTX 3060 (12GB)", "memory": 12},
            {"name": "NVIDIA RTX 4070 Ti (16GB)", "memory": 16},
            {"name": "NVIDIA RTX 4090 (24GB)", "memory": 24},
            {"name": "NVIDIA A100 (40GB)", "memory": 40},
            {"name": "NVIDIA A100 (80GB)", "memory": 80}
        ]
        
        suitable_gpus = [gpu for gpu in gpu_tiers if gpu["memory"] >= memory_gb]
        
        return ui.div(
            ui.h3(f"Required GPU Memory: {memory_gb:.2f} GB", class_="text-primary"),
            ui.div(
                ui.h4("Suitable GPUs:" if suitable_gpus else "Warning:", 
                      class_="" if suitable_gpus else "text-danger"),
                ui.tags.ul(
                    *[ui.tags.li(f"{gpu['name']}") for gpu in suitable_gpus]
                ) if suitable_gpus else ui.p("No common GPUs have sufficient memory. Consider using a lower quantization level.")
            )
        )
    
    @output
    @render.text
    def gpu_explanation():
        if not input.calculate_gpu():
            return ""
            
        P = input.model_size()
        Q = int(input.quantization())
        overhead = input.overhead()
        memory_gb = (P * Q / 8) * overhead
        
        return f"""
        Formula used: Memory (GB) = (P_billions × Q_bits ÷ 8) × overhead_factor
        
        Where:
        - P = {P} billion parameters
        - Q = {Q} bits (quantization level)
        - Overhead factor = {overhead}
        
        Calculation:
        ({P} × {Q} ÷ 8) × {overhead} = {memory_gb:.2f} GB
        """