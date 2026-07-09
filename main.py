from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

@app.post("/process")
def trigger_workflow(background_tasks: BackgroundTasks):
    def run():
        workflow = Workflow()
        workflow.process_new_emails()
    background_tasks.add_task(run)
    return {"status": "processing"}