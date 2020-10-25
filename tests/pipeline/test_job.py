from pathlib import Path

from podder_task_foundation import MODE, Context, Payload, Process
from podder_task_foundation.pipeline import Job


def test_job_create():
    context = Context(mode=MODE.TEST,
                      config_path=Path(__file__).parent.parent.joinpath("data", "config"))
    job = Job(process=Process(mode=MODE.TEST, context=context))
    assert job
