"""Tasks management API."""

from typing import List, Dict, Any


class TaskAPI:
    """API for managing scheduled tasks."""

    def __init__(self, client):
        self.client = client

    def list(self) -> List[Dict[str, Any]]:
        """
        List all tasks.

        Returns:
            List of tasks
        """
        response = self.client.get('/v1/tasks')
        return response.json()

    def get(self, task_id: str) -> Dict[str, Any]:
        """
        Get task details.

        Args:
            task_id: Task ID

        Returns:
            Task details
        """
        response = self.client.get(f'/v1/tasks/{task_id}')
        return response.json()

    def run(self, task_id: str) -> None:
        """
        Run a task immediately.

        Args:
            task_id: Task ID to run
        """
        self.client.post(f'/v1/tasks/{task_id}/run')

    def stop(self, task_id: str) -> None:
        """
        Stop a running task.

        Args:
            task_id: Task ID to stop
        """
        self.client.post(f'/v1/tasks/{task_id}/stop')
