# Cylindrical Cell Battery Pack Designer - Busbar Interconnect Layout

A high-fidelity Python application for designing and visualizing cylindrical battery packs. This tool provides real-time 3D rendering of cell configurations, polarity flipping, and copper busbar interconnects with a professional engineering interface.

## Features

*   **Dynamic 3D Visualization**: Real-time rendering of cylindrical cells with high-contrast aesthetics.
*   **Intelligent Busbar Logic**: Automatically generates copper series-parallel interconnects based on Series and Parallel inputs.
*   **Automatic Polarity Flipping**: Alternates cell orientation for series groups to simulate professional manufacturing layouts.
*   **Real-time Analytics**: Calculates Total Pack Voltage, Total Internal Resistance, and Max Pulse Power Output instantly.
*   **Multithreaded Rendering**: Background processing ensures the UI remains responsive during complex 3D calculations.
*   **Interactive View**: Full support for rotation, zooming, and panning via the integrated Matplotlib navigation toolbar.

## Screenshots
<img width="1920" height="1023" alt="Snipaste_2026-05-02_08-58-15" src="https://github.com/user-attachments/assets/9c2590b7-f171-451e-b372-128fb124f449" />


| Configuration Sidebar | 3D Busbar Layout |
| :--- | :--- |

| *Professional Dark Mode UI* | *Copper interconnects and polarity indicators* |

## Tech Stack

*   **Python 3.x**
*   **Tkinter**: Main GUI framework with dark-themed styling.
*   **Matplotlib**: 3D rendering engine.
*   **NumPy**: Mathematical computations for cell geometry.
*   **Threading**: Asynchronous task management.

## Installation

1. Ensure you have Python installed.
2. Install the required dependencies via pip:

```bash
pip install matplotlib numpy
```

## Usage

1. Run the script:
   ```bash
   python battery_designer.py
   ```
2. **Configure Parameters**: Enter your Series (S), Parallel (P), Voltage, and Resistance values.
3. Click **Update 3D Model** to generate the design.
4. Use the **Toolbar** at the bottom of the plot to zoom and pan, or **Left-Click + Drag** to rotate.

## Changelog

### v1.3.0
*   **UI Overhaul**: Implemented a dark theme with increased font sizes for better legibility on high-resolution displays.
*   **Stability**: Added Multi-threading to prevent UI freezing during large-scale pack renders.
*   **Navigation**: Embedded standard Matplotlib Navigation Toolbar for precise zoom and pan control.

### v1.2.0
*   **Copper Logic**: Implemented dual-side busbar rendering with automated series-bridging logic.
*   **Responsive Design**: Added grid weights to allow the 3D canvas to expand to full screen.

### v1.1.0
*   Initial release with basic Series/Parallel configuration and 3D cylinder rendering.

---
**Disclaimer:** Verify all electrical calculations against your specific cell manufacturer's datasheet before any physical assembly or prototyping.
