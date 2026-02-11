from fpdf import FPDF, XPos, YPos
import datetime
import os


class ProjectDocPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        font_dir = os.path.dirname(__file__)
        mono_font_path = os.path.join(font_dir, "DejaVuSansMono.ttf")
        base_font_path = os.path.join(font_dir, "DejaVuSans.ttf")

        # Register base Unicode font if available
        if os.path.exists(base_font_path):
            self.add_font("Base", "", base_font_path)
            self.add_font("Base", "B", base_font_path)
            self.add_font("Base", "I", base_font_path)
            self.base_font = "Base"
        else:
            self.base_font = "helvetica"

        # Register monospaced Unicode font if available
        if os.path.exists(mono_font_path):
            self.add_font("Mono", "", mono_font_path)
            # We will not use bold style for Mono to avoid undefined font errors
            self.mono_font = "Mono"
        else:
            self.mono_font = self.base_font

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.base_font, "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(
                0,
                10,
                f"Talend-to-dbt Migration Agent Technical Manual - Page {self.page_no()}",
                align="R",
                new_x=XPos.RMARGIN,
                new_y=YPos.TOP,
            )
            self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.base_font, "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(
            0,
            10,
            f"Confidential - Generated on {datetime.datetime.now().strftime('%Y-%m-%d')}",
            align="C",
            new_x=XPos.LMARGIN,
            new_y=YPos.TOP,
        )

    def section_title(self, label: str):
        self.set_font(self.base_font, "B", 16)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(52, 152, 219)
        x = self.l_margin
        y = self.get_y()
        self.line(x, y, x + 190, y)
        self.ln(5)

    def sub_section(self, label: str):
        self.set_font(self.base_font, "B", 12)
        self.set_text_color(52, 73, 94)
        self.cell(0, 8, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def body_text(self, text: str):
        self.set_font(self.base_font, "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(4)

    def code_block(self, text: str):
        self.set_fill_color(245, 245, 245)
        self.set_font(self.mono_font, "", 9)
        self.multi_cell(0, 5, text, fill=True, border=1)
        self.ln(4)


def generate_report():
    pdf = ProjectDocPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- TITLE PAGE ---
    pdf.add_page()
    pdf.ln(60)

    pdf.set_font(pdf.base_font, "B", 32)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(
        0,
        20,
        "Talend-to-dbt",
        align="C",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.cell(
        0,
        20,
        "Migration Agent",
        align="C",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.ln(10)
    pdf.set_font(pdf.base_font, "", 14)
    pdf.cell(
        0,
        10,
        "Technical Specification & Operational Manual",
        align="C",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.set_draw_color(44, 62, 80)
    pdf.line(50, 135, 160, 135)

    pdf.ln(80)
    pdf.set_font(pdf.base_font, "I", 10)
    pdf.cell(
        0,
        10,
        "Version 1.0.1 | Optimized for DuckDB & Temporal.io",
        align="C",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    # --- ARCHITECTURE DIAGRAM SECTION ---
    pdf.add_page()
    pdf.section_title("1. System Architecture")
    pdf.body_text(
        "The agent utilizes a decoupled architecture to separate metadata parsing from logical code generation."
    )

    pdf.set_font(pdf.mono_font, "", 10)
    diagram = (
        " [ Talend XML ] ----> [ ProjectGraph Mapper ]\n"
        "          |\n"
        "          v\n"
        " [ LLM / Ollama ] <--- [ Migration Engine ] ---> [ Knowledge Base ]\n"
        "             |                          |   (800+ Rules)\n"
        "             v                          v\n"
        "   [ dbt SQL Models ]         [ Temporal Workflows ]\n"
    )
    pdf.multi_cell(0, 6, diagram, align="C", border=1)
    pdf.ln(5)

    pdf.sub_section("1.1 Core Components")
    pdf.body_text(
        "- Knowledge Base: More than 800+ rules for components and full Java Routine translation."
    )
    pdf.body_text(
        "- Migration Engine: Parallel multi-threaded processing optimized for i7-14700K."
    )
    pdf.body_text(
        "- Sourav Agent: Context-aware inference engine using local LLMs via Ollama."
    )

    # --- FOLDER STRUCTURE ---
    pdf.add_page()
    pdf.section_title("2. Project Framework")
    pdf.sub_section("2.1 Directory Structure")

    tree = (
        "talendtodbtsouravagent/\n"
        "├── input_data/           # Source Talend .item files\n"
        "├── output/\n"
        "│   ├── models/          # Generated dbt SQL models\n"
        "│   ├── macros/          # Reusable Joblet macros\n"
        "│   └── temporal/        # Python workflow files\n"
        "├── src/\n"
        "│   ├── main_engine.py   # Orchestration logic\n"
        "│   ├── agent_llm.py     # LLM interface\n"
        "│   └── knowledge_base.py# Rule Encyclopedia\n"
        "└── run_migration.py     # Entry point"
    )
    pdf.code_block(tree)

    # --- INSTALLATION & HARDWARE ---
    pdf.section_title("3. Installation & Optimization")
    pdf.sub_section("3.1 Environment Setup")
    pdf.body_text("1. Install Dependencies: pip install -r requirements.txt")
    pdf.body_text(
        "2. Configure Ollama: Ensure 'llama3' or 'mistral' is pulled and 'ollama serve' is active."
    )

    pdf.sub_section("3.2 Hardware Saturation (RTX 5070)")
    pdf.body_text("The agent is configured to squeeze maximum performance from 12GB VRAM:")
    pdf.code_block(
        "num_ctx   = 4096  # VRAM safe limit - increase if needed\n"
        "num_gpu   = 999   # 100% offload\n"
        "num_thread= 8     # P-core target\n"
    )

    # --- USER MANUAL & SAMPLES ---
    pdf.add_page()
    pdf.section_title("4. Operational Guidelines")
    pdf.body_text(
        "Run 'python run_migration.py' to begin. The engine will topologically sort components "
        "and generate valid CTE chains."
    )

    pdf.sub_section("4.1 Sample Input (Talend XML)")
    pdf.code_block("...")

    pdf.sub_section("4.2 Sample Output (dbt SQL)")
    pdf.code_block(
        "WITH tFileInput_1 AS (\n"
        "    SELECT * FROM {{ source('raw', 'data') }}\n"
        "),\n"
        "tMap_1 AS (\n"
        "    SELECT col1, upper(col2) FROM tFileInput_1\n"
        "),\n"
        "final_cte AS (\n"
        "    SELECT * FROM tMap_1\n"
        ")\n"
        "SELECT * FROM final_cte;"
    )

    pdf.output("Talend_to_dbt_Migration_Agent_Manual.pdf")
    print(
        "[SUCCESS] Professional PDF Manual generated: "
        "Talend_to_dbt_Migration_Agent_Manual.pdf"
    )


if __name__ == "__main__":
    generate_report()
