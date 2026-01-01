"""
Data Visualization Module
Creates interactive visualizations with Matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import io
import base64


def create_time_series_visualization(
    data_length: int = 100,
    baseline: float = 200,
    threshold: float = 195,
    save_path: str = None
) -> Tuple[str, np.ndarray]:
    """
    Create a time series visualization with threshold highlighting.
    
    Parameters:
    -----------
    data_length : int
        Number of data points
    baseline : float
        Baseline value for the time series
    threshold : float
        Threshold for fill_between
    save_path : str, optional
        Path to save the image
    
    Returns:
    --------
    tuple : (base64_image, data_array)
    """
    
    # Generate sample data
    np.random.seed(42)  # For reproducibility
    ys = baseline + np.random.randn(data_length)
    x = np.arange(data_length)
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    
    # Plot main line
    ax.plot(x, ys, '-', color='#2E86AB', linewidth=2, label='Time Series')
    
    # Highlight area above threshold
    ax.fill_between(
        x, ys, threshold,
        where=(ys > threshold),
        facecolor='#A3D9B1',
        alpha=0.6,
        label=f'Above {threshold}'
    )
    
    # Add threshold line
    ax.axhline(
        y=threshold,
        color='#E76F51',
        linestyle='--',
        linewidth=1.5,
        label=f'Threshold ({threshold})'
    )
    
    # Customize plot
    ax.set_title(
        'Time Series Visualization with Threshold Highlighting',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    
    ax.set_xlabel('Time Index', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', framealpha=0.9)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save or convert to base64
    if save_path:
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches='tight',
            facecolor='white'
        )
        print(f"Plot saved to: {save_path}")
    
    # Convert to base64 for web display
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    
    # Generate base64 string
    base64_image = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    
    return f"data:image/png;base64,{base64_image}", ys


def generate_markdown_demo() -> str:
    """Generate markdown with embedded visualization"""
    
    image_base64, data = create_time_series_visualization()
    
    markdown_content = f"""
# Data Visualization Demo

## Interactive Time Series Plot

![Time Series Visualization]({image_base64})

## Features
- ✅ Clean, reproducible visualizations
- ✅ Threshold highlighting
- ✅ Responsive design
- ✅ Export to multiple formats

## Statistics Summary
```python
Mean: {np.mean(data):.2f}
Std Dev: {np.std(data):.2f}
Max: {np.max(data):.2f}
Min: {np.min(data):.2f}