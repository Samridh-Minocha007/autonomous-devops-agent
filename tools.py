import docker
import requests

# Initialize the Docker client
try:
    client = docker.from_env()
except docker.errors.DockerException:
    print("Error: Docker is not running. Please start Docker Desktop.")
    exit()


def list_running_containers(placeholder: str = "") -> str:
    """
    Lists all currently running Docker containers with their names and IDs.
    """
    print("--- TOOL: Listing running containers ---")
    try:
        containers = client.containers.list()
        if not containers:
            return "No containers are currently running."
        # Format the output nicely
        return "\n".join([f"ID: {c.short_id}, Name: {c.name}" for c in containers])
    except Exception as e:
        return f"Error listing containers: {e}"

def restart_container(container_id: str) -> str:
    """Restarts a specific Docker container immediately."""
    print(f"--- TOOL: Attempting to restart container {container_id} ---")
    try:
        container = client.containers.get(container_id)
        container.restart()
        return f"Successfully restarted container {container_id}."
    except docker.errors.NotFound:
        # This is key! If the container is stopped, we use 'docker start'.
        print(f"Container {container_id} not running, attempting to start it.")
        client.containers.client.start(container_id)
        return f"Container {container_id} was stopped and has been started."
    except Exception as e:
        return f"Error restarting container: {e}"
    
def check_webapp_health(placeholder: str = "") -> str:
    """
    Checks the health of the webapp by sending a request to its endpoint.
    """
    print("--- TOOL: Checking webapp health ---")
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            return "Webapp is healthy and running."
        else:
            return f"Webapp is unhealthy. Status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Webapp is down. Connection could not be established."
    except Exception as e:
        return f"An error occurred while checking webapp health: {e}"

# ... (keep all your existing functions) ...

def get_container_logs(container_id: str) -> str:
    """Fetches the last 20 lines of logs for a specific Docker container."""
    print(f"--- TOOL: Fetching logs for container {container_id} ---")
    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=20).decode('utf-8')
        return f"Logs for {container_id}:\n{logs}"
    except docker.errors.NotFound:
        return f"Error: Container {container_id} not found."
    except Exception as e:
        return f"Error fetching logs: {e}"

# --- Test the Tools ---
if __name__ == "__main__":
    print("Running tool tests...")
    print("Checking webapp health:")
    print(check_webapp_health()) # We are now testing the new function