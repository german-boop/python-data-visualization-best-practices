"""
Random Data Visualization with Matplotlib

This module provides functions to generate random data, create visualizations,
and display them inline in Jupyter notebooks.
"""

import base64
import io
from typing import List, Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, Markdown


def generate_random_data(
    n_points: int = 100,
    base_value: float = 200.0,
    noise_std: float = 1.0
) -> Tuple[List[float], np.ndarray]:
    """
    Generate random data points for visualization.
    
    Args:
        n_points: Number of data points to generate (default: 100)
        base_value: Base value around which data is generated (default: 200.0)
        noise_std: Standard deviation of the normal distribution noise (default: 1.0)
        
    Returns:
        Tuple containing:
        - x_values: List of indices [0, 1, ..., n_points-1]
        - y_values: NumPy array of random values
        
    Example:
        >>> x, y = generate_random_data(50, base_value=100, noise_std=2.0)
        >>> len(x)
        50
    """
    # Validate input parameters
    if n_points <= 0:
        raise ValueError("n_points must be positive")
    if noise_std <= 0:
        raise ValueError("noise_std must be positive")
    
    # Generate y-values with normal distribution around base_value
    y_values = base_value + noise_std * np.random.randn(n_points)
    
    # Generate x-values as indices
    x_values = list(range(n_points))
    
    return x_values, y_values


def create_visualization(
    x_values: List[float],
    y_values: np.ndarray,
    figsize: Tuple[float, float] = (8, 4),
    threshold: float = 195.0,
    title: str = "Random Data Visualization",
    y_label: str = "Value",
    x_label: str = "Index"
) -> plt.Figure:
    """
    Create a matplotlib visualization with configurable parameters.
    
    Args:
        x_values: List of x-axis values
        y_values: Array of y-axis values
        figsize: Figure size in inches (width, height) (default: (8, 4))
        threshold: Threshold value for area filling (default: 195.0)
        title: Plot title (default: "Random Data Visualization")
        y_label: Y-axis label (default: "Value")
        x_label: X-axis label (default: "Index")
        
    Returns:
        matplotlib Figure object
        
    Raises:
        ValueError: If x_values and y_values have different lengths
    """
    # Validate input data
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    # Create figure with white background
    fig, ax = plt.subplots(figsize=figsize, facecolor='white')
    
    # Plot the main line
    ax.plot(
        x_values,
        y_values,
        '-',
        color='#1f77b4',  # Matplotlib blue
        linewidth=2,
        alpha=0.8,
        label='Data Series'
    )
    
    # Fill area above threshold
    ax.fill_between(
        x_values,
        y_values,
        threshold,
        where=(y_values > threshold),
        facecolor='#2ca02c',  # Matplotlib green
        alpha=0.4,
        label=f'Above {threshold}'
    )
    
    # Add threshold line
    ax.axhline(
        y=threshold,
        color='#d62728',  # Matplotlib red
        linestyle='--',
        alpha=0.7,
        linewidth=1.5,
        label=f'Threshold ({threshold})'
    )
    
    # Calculate statistics for annotation
    mean_value = np.mean(y_values)
    std_value = np.std(y_values)
    
    # Add statistics annotation
    stats_text = f'Mean: {mean_value:.2f}\nStd: {std_value:.2f}'
    ax.text(
        0.02, 0.98,
        stats_text,
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )
    
    # Customize plot appearance
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel(x_label, fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    
    # Set x-axis limits
    ax.set_xlim(min(x_values), max(x_values))
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Add legend
    ax.legend(
        loc='upper right',
        fontsize=9,
        framealpha=0.9,
        fancybox=True,
        shadow=True
    )
    
    # Adjust layout
    plt.tight_layout()
    
    return fig


def figure_to_base64(
    fig: plt.Figure,
    dpi: int = 150,
    format: str = 'png'
) -> str:
    """
    Convert matplotlib figure to base64 encoded string.
    
    Args:
        fig: matplotlib Figure object
        dpi: Resolution in dots per inch (default: 150)
        format: Image format (default: 'png')
        
    Returns:
        Base64 encoded image string with data URI prefix
    """
    buffer = io.BytesIO()
    
    # Save figure to buffer
    fig.savefig(
        buffer,
        format=format,
        dpi=dpi,
        bbox_inches='tight',
        facecolor=fig.get_facecolor()
    )
    buffer.seek(0)
    
    # Encode to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    # Return data URI
    return f"data:image/{format};base64,{image_base64}"


def display_inline_image(
    image_data: str,
    alt_text: str = "Data Visualization",
    width: Optional[int] = None,
    height: Optional[int] = None
) -> None:
    """
    Display base64 encoded image inline in Jupyter notebook.
    
    Args:
        image_data: Base64 encoded image string or data URI
        alt_text: Alternative text for accessibility
        width: Optional width in pixels
        height: Optional height in pixels
        
    Returns:
        None
    """
    # Build Markdown image tag
    style_parts = []
    if width:
        style_parts.append(f"width: {width}px")
    if height:
        style_parts.append(f"height: {height}px")
    
    style = f' style="{"; ".join(style_parts)}"' if style_parts else ''
    
    # Create and display Markdown
    markdown = f'<img src="{image_data}" alt="{alt_text}"{style}>'
    display(Markdown(markdown))


def main() -> None:
    """
    Main execution function demonstrating the visualization workflow.
    
    This function:
    1. Generates random data
    2. Creates a visualization
    3. Converts it to base64
    4. Displays it inline
    """
    try:
        print("🎨 Generating visualization...")
        
        # Generate data
        x_data, y_data = generate_random_data(
            n_points=100,
            base_value=200.0,
            noise_std=2.0
        )
        
        # Create visualization
        fig = create_visualization(
            x_data,
            y_data,
            figsize=(10, 5),
            threshold=195.0,
            title="Sample Random Data Visualization"
        )
        
        # Convert to base64
        image_data = figure_to_base64(fig, dpi=120)
        
        # Display in notebook
        display_inline_image(
            image_data,
            alt_text="Random Data Plot",
            width=800
        )
        
        # Close figure to free memory
        plt.close(fig)
        
        print("✅ Visualization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        raise


if __name__ == "__main__":
    # For standalone execution
    main()