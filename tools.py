import docker
import requests


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
       
        return "\n".join([f"ID: {c.short_id}, Name: {c.name}" for c in containers])
    except Exception as e:
        return f"Error listing containers: {e}"

def restart_container(container_id: str) -> str:
    """Restarts a specific Docker container. If stopped, it attempts to start it."""
    print(f"--- TOOL: Attempting to restart container {container_id} ---")
    try:
        
        container = client.containers.get(container_id)
        container.restart()
        return f"Successfully restarted container {container_id}."
    except docker.errors.NotFound:
        
        try:
           
            container = client.containers.get(container_id, all=True)
            print(f"Container {container_id} found in exited state. Attempting to start it.")
            container.start()
            return f"Container {container_id} was stopped and has been started."
        except docker.errors.NotFound:
            return f"Error: Container {container_id} not found at all (neither running nor stopped)."
        except Exception as e:
            return f"Error starting stopped container {container_id}: {e}"
    except Exception as e:
        return f"Error restarting container {container_id}: {e}"
    
def check_webapp_health(placeholder: str = "") -> str:
    """
    Checks the health of the webapp by sending a request to its endpoint.
    """
    print("--- TOOL: Checking webapp health ---")
    try:
        
        response = requests.get("http://webapp:8000/", timeout=5) 
        if response.status_code == 200:
            return "Webapp is healthy and running."
        else:
            return f"Webapp is unhealthy. Status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Webapp is down. Connection could not be established."
    except Exception as e:
        return f"An error occurred while checking webapp health: {e}"



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
    
def list_webapp_status(placeholder: str = "") -> str:
    """
    Lists all Docker containers related to the 'webapp' service and their current status (running or exited).
    Helps identify which specific webapp instances are currently down.
    """
    print("--- TOOL: Listing webapp container status ---")
    try:
        
        all_containers = client.containers.list(all=True)
        webapp_containers_info = []
        for c in all_containers:
            if c.name.startswith('devopsagent-webapp-'): 
                status = c.status
                
                if c.attrs.get('State', {}).get('Health'):
                    health_status = c.attrs['State']['Health']['Status']
                    status = f"{status} (Health: {health_status})"
                webapp_containers_info.append(f"ID: {c.short_id}, Name: {c.name}, Status: {status}")

        if not webapp_containers_info:
            return "No webapp containers found with 'devopsagent-webapp-' prefix."
        
        return "\n".join(webapp_containers_info)
    except Exception as e:
        return f"Error listing webapp status: {e}"


if __name__ == "__main__":
    print("Running tool tests...")
    print("Checking webapp health:")
    print(check_webapp_health()) 
    print("Running tool tests...")
    print("Listing webapp status:")
    print(list_webapp_status())