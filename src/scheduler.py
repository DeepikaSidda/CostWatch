"""Update scheduler for AWS Cost Widget."""

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from widget import AWSCostWidget
    from cost_fetcher import CostData


class UpdateScheduler:
    """Manages periodic data refresh for the widget."""
    
    def __init__(self, widget: 'AWSCostWidget', fetcher: Callable[[], 'CostData'], interval: int):
        """
        Initialize scheduler with widget, data fetcher, and interval.
        
        Args:
            widget: The widget to update
            fetcher: Function that returns CostData
            interval: Refresh interval in seconds
        """
        self.widget = widget
        self.fetcher = fetcher
        self.interval = interval * 1000  # Convert to milliseconds
        self._scheduled_id = None
    
    def start(self) -> None:
        """Start the update scheduler."""
        self.perform_update()
    
    def stop(self) -> None:
        """Stop the update scheduler."""
        if self._scheduled_id is not None:
            self.widget.root.after_cancel(self._scheduled_id)
            self._scheduled_id = None
    
    def schedule_update(self) -> None:
        """Schedule the next data refresh."""
        self._scheduled_id = self.widget.root.after(self.interval, self.perform_update)
    
    def perform_update(self) -> None:
        """Fetch new data and update widget display."""
        try:
            cost_data = self.fetcher()
            self.widget.update_display(cost_data)
        except Exception as e:
            # Log error but continue scheduling
            print(f"Error fetching cost data: {e}")
        
        # Schedule next update
        self.schedule_update()
