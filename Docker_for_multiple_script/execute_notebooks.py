import schedule
import time
import papermill as pm

# List of notebooks to execute
notebooks = [
    "Kiel_Event_Calendar.ipynb",
    "OSM_version_2.ipynb",

]

# Function to execute notebooks
def execute_notebooks():
    for notebook in notebooks:
        try:
            print(f"Executing {notebook}")
            pm.execute_notebook(
                input_path=notebook,
                output_path=f"executed_{notebook.split('/')[-1]}"  # Save output notebook
            )
            print(f"Execution completed for {notebook}")
        except Exception as e:
            print(f"Error while executing {notebook}: {e}")

# Schedule the execution every 24 hours
schedule.every(24).hours.do(execute_notebooks)

# Run the scheduler
print("Scheduler is running. Notebooks will execute every 24 hours.")
execute_notebooks()  # Run once immediately
while True:
    schedule.run_pending()
    time.sleep(1)
