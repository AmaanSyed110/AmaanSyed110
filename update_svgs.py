import re

def update_svg(filepath, text_color, highlight_color):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the insertion point: just before the first <text x="540"
    match = re.search(r'<text x="540"', content)
    if not match:
        print(f"Could not find text nodes in {filepath}")
        return
        
    start_idx = match.start()
    
    # Find the end of the text nodes (the last </text> before </svg>)
    # Actually, let's just remove all lines containing <text x="540"
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if '<text x="540"' not in line:
            new_lines.append(line)
        else:
            # We skip this line
            pass
            
    # Now we construct the new lines to insert
    # We find where to insert them (right after the last <text x="28" ...)
    
    insert_idx = -1
    for i in range(len(new_lines)-1, -1, -1):
        if '<text x="28"' in new_lines[i]:
            insert_idx = i + 1
            break
            
    if insert_idx == -1:
        insert_idx = len(new_lines) - 1 # just before </svg>

    # The summary from the README
    summary_lines = [
        ("─ AmaanSyed110@github ────────────────────────────────────", highlight_color, True),
        ("", text_color, False),
        (". Role:       Principal AI Engineer & Systems Architect", text_color, False),
        (". Experience: 2+ yrs engineering advanced ML workflows", text_color, False),
        ("", text_color, False),
        ("─ Core Focus ─────────────────────────────────────────────", highlight_color, True),
        ("", text_color, False),
        (". 1: Hybrid Vector Search & RAG (BGE-M3, BM25, Cohere)", text_color, False),
        (". 2: Stateful Agent Orchestration (LangGraph, CrewAI)", text_color, False),
        (". 3: Layout-Aware Document Intelligence for complex PDFs", text_color, False),
        ("", text_color, False),
        ("─ Featured Projects ──────────────────────────────────────", highlight_color, True),
        ("", text_color, False),
        (". Smart ATS Pro AI Resume Analyzer", text_color, False),
        (". Multimodal RAG", text_color, False),
        (". Real-Time Semantic Recommendation System", text_color, False),
        (". Youtube Video Summarizer", text_color, False)
    ]
    
    y_start = 103.4
    y_step = 20.0
    
    new_svg_text = []
    
    for i, (text, color, is_title) in enumerate(summary_lines):
        y = y_start + (i * y_step)
        if text.strip() == "":
            continue
            
        if is_title:
            # title styling like in original
            # <tspan fill="#3d444d">─</tspan><tspan fill="#58a6ff"> Contact </tspan><tspan fill="#3d444d">────────────────────────────────────────────────</tspan>
            parts = text.split(' ', 2)
            if len(parts) >= 3:
                dash1 = parts[0]
                title = parts[1]
                dash2 = parts[2]
                
                # Use a specific dash color based on theme
                dash_color = "#3d444d" if "dark" in filepath else "#d0d7de"
                
                line_html = f'  <text x="540" y="{y}" font-family="\'Consolas\', \'Menlo\', \'DejaVu Sans Mono\', monospace" xml:space="preserve" font-size="16"><tspan fill="{dash_color}">{dash1}</tspan><tspan fill="{color}"> {title} </tspan><tspan fill="{dash_color}">{dash2}</tspan></text>'
                new_svg_text.append(line_html)
            else:
                line_html = f'  <text x="540" y="{y}" fill="{color}" font-family="\'Consolas\', \'Menlo\', \'DejaVu Sans Mono\', monospace" xml:space="preserve" font-size="16">{text}</text>'
                new_svg_text.append(line_html)
        else:
            # color the dot and label differently if it contains a colon
            if ": " in text:
                parts = text.split(": ", 1)
                label = parts[0] + ": "
                val = parts[1]
                dot_color = "#ffa657" if "dark" in filepath else "#cf222e" # orange/red
                line_html = f'  <text x="540" y="{y}" font-family="\'Consolas\', \'Menlo\', \'DejaVu Sans Mono\', monospace" xml:space="preserve" font-size="16"><tspan fill="{dot_color}">{label}</tspan><tspan fill="{color}">{val}</tspan></text>'
                new_svg_text.append(line_html)
            else:
                line_html = f'  <text x="540" y="{y}" fill="{color}" font-family="\'Consolas\', \'Menlo\', \'DejaVu Sans Mono\', monospace" xml:space="preserve" font-size="16">{text}</text>'
                new_svg_text.append(line_html)
                
    new_lines = new_lines[:insert_idx] + new_svg_text + new_lines[insert_idx:]
    
    with open(filepath, 'w') as f:
        f.write('\n'.join(new_lines))
        
update_svg('dark_mode.svg', '#c9d1d9', '#58a6ff')
update_svg('light_mode.svg', '#24292f', '#0969da')
