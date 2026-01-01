"""
Unit tests for the random-data-visualization package.
"""

import base64
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest

from visualization import (
    RandomDataVisualizer,
    VisualizationConfig,
    quick_visualize
)


class TestVisualizationConfig:
    """Test cases for VisualizationConfig class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = VisualizationConfig()
        
        assert config.n_points == 100
        assert config.base_value == 200.0
        assert config.noise_std == 1.0
        assert config.random_seed is None
        assert config.figsize == (10, 6)
        assert config.threshold == 195.0
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = VisualizationConfig(
            n_points=50,
            base_value=150.0,
            noise_std=2.0,
            random_seed=42,
            figsize=(8, 4),
            threshold=145.0,
            title="Custom Title",
            color_scheme="dark"
        )
        
        assert config.n_points == 50
        assert config.base_value == 150.0
        assert config.noise_std == 2.0
        assert config.random_seed == 42
        assert config.figsize == (8, 4)
        assert config.threshold == 145.0
        assert config.title == "Custom Title"
        assert config.color_scheme == "dark"
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = VisualizationConfig(n_points=75, random_seed=42)
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert config_dict["n_points"] == 75
        assert config_dict["random_seed"] == 42
        assert "figsize" in config_dict
        assert "color_scheme" in config_dict
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        config_dict = {
            "n_points": 30,
            "base_value": 100.0,
            "noise_std": 3.0,
            "figsize": (6, 3)
        }
        
        config = VisualizationConfig.from_dict(config_dict)
        
        assert config.n_points == 30
        assert config.base_value == 100.0
        assert config.noise_std == 3.0
        assert config.figsize == (6, 3)


class TestRandomDataVisualizer:
    """Test cases for RandomDataVisualizer class."""
    
    def test_initialization_default(self):
        """Test default initialization."""
        visualizer = RandomDataVisualizer()
        
        assert isinstance(visualizer.config, VisualizationConfig)
        assert visualizer._figure is None
        assert visualizer._data is None
    
    def test_initialization_custom(self):
        """Test initialization with custom config."""
        config = VisualizationConfig(n_points=50, base_value=150.0)
        visualizer = RandomDataVisualizer(config)
        
        assert visualizer.config.n_points == 50
        assert visualizer.config.base_value == 150.0
    
    def test_random_seed(self):
        """Test that random seed produces reproducible results."""
        config1 = VisualizationConfig(n_points=10, random_seed=42)
        config2 = VisualizationConfig(n_points=10, random_seed=42)
        
        visualizer1 = RandomDataVisualizer(config1)
        visualizer2 = RandomDataVisualizer(config2)
        
        data1 = visualizer1.generate_data()
        data2 = visualizer2.generate_data()
        
        # y-values should be identical with same seed
        np.testing.assert_array_equal(data1[1], data2[1])
    
    def test_generate_data_default(self):
        """Test data generation with default parameters."""
        visualizer = RandomDataVisualizer()
        x_data, y_data = visualizer.generate_data()
        
        assert len(x_data) == 100
        assert len(y_data) == 100
        assert isinstance(x_data, list)
        assert isinstance(y_data, np.ndarray)
        assert visualizer._data is not None
    
    def test_generate_data_custom(self):
        """Test data generation with custom parameters."""
        config = VisualizationConfig(n_points=75)
        visualizer = RandomDataVisualizer(config)
        x_data, y_data = visualizer.generate_data()
        
        assert len(x_data) == 75
        assert len(y_data) == 75
    
    @pytest.mark.parametrize("n_points", [-1, 0])
    def test_generate_data_invalid_n_points(self, n_points):
        """Test data generation with invalid n_points."""
        config = VisualizationConfig(n_points=n_points)
        visualizer = RandomDataVisualizer(config)
        
        with pytest.raises(ValueError, match="n_points must be positive"):
            visualizer.generate_data()
    
    def test_get_statistics(self):
        """Test statistics calculation."""
        visualizer = RandomDataVisualizer()
        visualizer.generate_data()
        stats = visualizer.get_statistics()
        
        expected_keys = {
            "mean", "median", "std", "min", "max",
            "q1", "q3", "above_threshold", "below_threshold"
        }
        
        assert set(stats.keys()) == expected_keys
        assert all(isinstance(v, float) for v in stats.values())
        
        # Statistics should be consistent with threshold
        _, y_data = visualizer._data
        assert stats["above_threshold"] == float(np.sum(y_data > visualizer.config.threshold))
    
    def test_get_statistics_no_data(self):
        """Test statistics calculation without data."""
        visualizer = RandomDataVisualizer()
        
        with pytest.raises(RuntimeError, match="No data available"):
            visualizer.get_statistics()
    
    def test_create_visualization(self):
        """Test figure creation."""
        visualizer = RandomDataVisualizer()
        fig = visualizer.create_visualization()
        
        assert isinstance(fig, plt.Figure)
        assert visualizer._figure is fig
        assert len(fig.axes) == 1
        
        # Clean up
        visualizer.close_figure()
    
    def test_save_figure(self):
        """Test saving figure to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_figure.png"
            
            visualizer = RandomDataVisualizer()
            visualizer.create_visualization()
            visualizer.save_figure(output_path)
            
            assert output_path.exists()
            assert output_path.stat().st_size > 0
            
            # Clean up
            visualizer.close_figure()
    
    def test_save_figure_no_figure(self):
        """Test saving figure when no figure exists."""
        visualizer = RandomDataVisualizer()
        
        with pytest.raises(RuntimeError, match="No figure available"):
            visualizer.save_figure("test.png")
    
    def test_to_base64(self):
        """Test base64 conversion."""
        visualizer = RandomDataVisualizer()
        visualizer.create_visualization()
        base64_string = visualizer.to_base64()
        
        assert base64_string.startswith("data:image/png;base64,")
        
        # Verify it's valid base64
        encoded = base64_string.split(",")[1]
        decoded = base64.b64decode(encoded)
        assert len(decoded) > 0
        
        # Clean up
        visualizer.close_figure()
    
    def test_to_base64_no_figure(self):
        """Test base64 conversion when no figure exists."""
        visualizer = RandomDataVisualizer()
        
        with pytest.raises(RuntimeError, match="No figure available"):
            visualizer.to_base64()
    
    def test_context_manager(self):
        """Test context manager functionality."""
        with RandomDataVisualizer() as visualizer:
            visualizer.create_visualization()
            assert visualizer._figure is not None
        
        # Figure should be closed after context exit
        assert visualizer._figure is None
    
    def test_close_figure(self):
        """Test figure closing."""
        visualizer = RandomDataVisualizer()
        visualizer.create_visualization()
        
        assert visualizer._figure is not None
        visualizer.close_figure()
        assert visualizer._figure is None


class TestQuickVisualize:
    """Test cases for quick_visualize function."""
    
    def test_quick_visualize_default(self):
        """Test quick_visualize with default parameters."""
        visualizer = quick_visualize()
        
        assert isinstance(visualizer, RandomDataVisualizer)
        assert visualizer._figure is not None
        
        # Clean up
        visualizer.close_figure()
    
    def test_quick_visualize_custom(self):
        """Test quick_visualize with custom parameters."""
        visualizer = quick_visualize(
            n_points=50,
            threshold=180.0,
            title="Custom Quick Viz",
            display_in_notebook=False
        )
        
        assert visualizer.config.n_points == 50
        assert visualizer.config.threshold == 180.0
        assert visualizer.config.title == "Custom Quick Viz"
        assert visualizer._figure is not None
        
        # Clean up
        visualizer.close_figure()
    
    def test_quick_visualize_kwargs(self):
        """Test quick_visualize with additional kwargs."""
        visualizer = quick_visualize(
            n_points=30,
            base_value=100.0,
            color_scheme="dark",
            figsize=(8, 4)
        )
        
        assert visualizer.config.n_points == 30
        assert visualizer.config.base_value == 100.0
        assert visualizer.config.color_scheme == "dark"
        assert visualizer.config.figsize == (8, 4)
        
        # Clean up
        visualizer.close_figure()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])