---
description: Procedura Standard pentru implementarea modulului de colorat (Paint Pro - Windows Dark Style)
---

# Procedura Colorat (Paint Pro Module)

Această procedură documentează pachetul software complet pentru funcționalitatea de desenat "Paint Pro". Conține structura, stilul și logica necesară pentru a replica interfața "Windows Paint Dark" oriunde în aplicație.

## 1. Structura HTML (Overlay)

Acesta este containerul principal. Trebuie plasat direct în `<body>`, preferabil la finalul fișierului HTML.

**Elemente Cheie:**
*   `z-index: 99999` (Critic pentru a sta peste header).
*   Ribbon Bar cu Unelte (Pensulă, Marker, Creion, Gumă, Coș de Gunoi).
*   Slidere Verticale pentru Mărime și Opacitate.

```html
<!-- PAINT APP OVERLAY (WINDOWS PAINT STYLE) -->
<div id="paintOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#202020; z-index:99999; flex-direction:column; font-family: 'Segoe UI', sans-serif;">
    
    <!-- HEADER / RIBBON -->
    <div style="background:#2b2b2b; padding:10px 20px; display:flex; align-items:center; gap:20px; border-bottom:1px solid #444; height:60px;">
        <div id="paintTitle" style="color:white; font-size:14px; font-weight:bold; margin-right:20px;">🎨 Paint Pro</div>
        
        <!-- Tools Group -->
        <div class="toolbar-group">
            <div class="tool-icon active" onclick="useTool('brush')" title="Brush">🖌️</div>
            <div class="tool-icon" onclick="useTool('marker')" title="Marker">🖍️</div>
            <div class="tool-icon" onclick="useTool('pencil')" title="Pencil">✏️</div>
            <div class="tool-icon" onclick="useTool('eraser')" title="Eraser">🧽</div>
            <div class="tool-icon" onclick="clearCanvas()" title="Clear All (Trash)">🗑️</div>
            <div class="tool-icon" onclick="undoLast()" title="Undo">↩️</div>
        </div>

        <!-- Separator -->
        <div style="width:1px; height:30px; background:#555;"></div>

        <!-- Colors Group -->
        <div class="toolbar-group">
            <input type="color" id="mainColor" value="#ff0000" onchange="setColor(this.value)" title="Choose Color">
            <!-- Quick Colors -->
            <div class="quick-color" style="background:red;" onclick="setQuickColor('red')"></div>
            <div class="quick-color" style="background:blue;" onclick="setQuickColor('blue')"></div>
            <div class="quick-color" style="background:green;" onclick="setQuickColor('green')"></div>
            <div class="quick-color" style="background:yellow;" onclick="setQuickColor('yellow')"></div>
            <div class="quick-color" style="background:black;" onclick="setQuickColor('black')"></div>
            <div class="quick-color" style="background:white;" onclick="setQuickColor('white')"></div>
        </div>

        <div style="flex:1;"></div>

        <!-- Window Controls -->
        <div class="toolbar-group">
            <button class="win-btn print" onclick="printDrawing()">🖨️ Print</button>
            <button class="win-btn close" onclick="closePainter()">❌ Exit</button>
        </div>
    </div>

    <!-- MAIN WORKSPACE -->
    <div style="flex:1; display:flex; position:relative; overflow:hidden;">
        
        <!-- LEFT PANEL (SLIDERS) -->
        <div style="width:80px; background:#333; display:flex; flex-direction:column; align-items:center; padding-top:20px; border-right:1px solid #444;">
            <!-- Size Slider -->
            <div class="slider-container">
                <label>Size</label>
                <input type="range" orient="vertical" id="brushSize" min="1" max="50" value="5" oninput="setSize(this.value)">
                <span id="sizeVal">5px</span>
            </div>
            
            <div style="height:20px;"></div>

            <!-- Opacity Slider -->
            <div class="slider-container">
                <label>Opacity</label>
                <input type="range" orient="vertical" id="brushOpacity" min="1" max="100" value="100" oninput="setOpacity(this.value)">
                <span id="opacityVal">100%</span>
            </div>
        </div>

        <!-- CANVAS AREA -->
        <div style="flex:1; background:#1e1e1e; display:flex; align-items:center; justify-content:center; overflow:auto; padding:20px;">
            <div id="printableArea" style="position:relative; width:500px; height:500px; background:white; box-shadow:0 0 30px rgba(0,0,0,0.5);">
                <img id="paintBg" src="" style="position:absolute; width:100%; height:100%; object-fit:contain; pointer-events:none; opacity:0.3;">
                <canvas id="paintCanvas" width="500" height="500" style="position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
            </div>
        </div>
    </div>
</div>
```

## 2. Stiluri CSS Necesare

Aceste stiluri asigură aspectul "Dark Mode" și funcționarea sliderelor verticale.

```css
<style>
    .toolbar-group { display:flex; gap:10px; align-items:center; }
    .tool-icon { 
        width:36px; height:36px; display:flex; align-items:center; justify-content:center; 
        border-radius:5px; cursor:pointer; font-size:18px; background:#3a3a3a; color:white;
        transition: background 0.2s;
    }
    .tool-icon:hover { background:#505050; }
    .tool-icon.active { background:#4C8BF5; }
    
    .quick-color { width:24px; height:24px; border-radius:50%; cursor:pointer; border:2px solid #555; }
    .quick-color:hover { transform:scale(1.2); border-color:white; }
    
    #mainColor { width:30px; height:30px; border:none; background:none; cursor:pointer; padding:0; }

    .win-btn { border:none; color:white; padding:8px 16px; border-radius:4px; cursor:pointer; font-weight:bold; display:flex; align-items:center; gap:5px;}
    .win-btn.print { background:#2196F3; }
    .win-btn.close { background:#d32f2f; }
    .win-btn:hover { opacity:0.9; }

    .slider-container { display:flex; flex-direction:column; align-items:center; gap:5px; color:#ccc; font-size:12px; }
    
    /* Vertical Range Input Styling Standardized */
    input[type=range][orient=vertical] {
        writing-mode: bt-lr; /* IE */
        -webkit-appearance: slider-vertical; /* WebKit */
        appearance: slider-vertical; /* Standard */
        width: 8px;
        height: 120px;
        padding: 0 5px;
    }

    @media print {
        body * { visibility: hidden; }
        #printableArea, #printableArea * { visibility: visible; }
        #printableArea { position: absolute; left: 0; top: 0; width: 100%; height: 100%; border: none; box-shadow:none; }
        #paintOverlay { background: white !important; display: block !important; }
    }
</style>
```

## 3. Logica JavaScript "Core"

Aceasta este inima aplicației (Engine-ul).

**Funcționalități Cheie:**
*   `openPainter(imgSrc, title)`: Deschide editorul cu imaginea specificată și setează titlul.
*   `useTool(name)`: Comută între Brush, Marker (transparent), Pencil (subțire), Eraser.
*   `clearCanvas()`: Funcția de "Coș de Gunoi".
*   `undoLast()`: Istoric de desenare.
*   Suport Touch & Mouse Events.

*(Codul complet se regăsește în gallery-drawings.html)*

## 4. Ghid de Utilizare / Multiplicare

Pentru a folosi această procedură pe o imagine nouă (Slot Nou):

1.  Creează un `div` cu clasa `slot filled`.
2.  Adaugă imaginea.
3.  Pe imagine, adaugă atributul `onclick` apelând funcția de deschidere:
    ```html
    onclick="openPainter('cale/catre/imagine.png', 'Numele Desenuluiici')"
    ```
4.  Exemplu:
    ```html
    <div class="slot filled">
        <span class="slot-number">4</span>
        <img src="assets/images/unicorn.png" 
             class="slot-content" 
             onclick="openPainter('assets/images/unicorn.png', 'Magic Unicorn')">
    </div>
    ```
