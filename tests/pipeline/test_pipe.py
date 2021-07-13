from pathlib import Path

from podder_task_foundation import MODE, Context, Payload, Process
from podder_task_foundation.pipeline import Job, Pipe


def test_pipe_create():
    context = Context(mode=MODE.TEST,
                      config_path=Path(__file__).parent.parent.joinpath("data", "config"))

    job1 = Job(process=Process(mode=MODE.TEST, context=context))
    job2 = Job(process=Process(mode=MODE.TEST, context=context))

    pipe = Pipe(units=[job1, job2], execute_type=Pipe.Type.SERIAL)
    assert pipe


def test_pipe_execute_serial():
    context = Context(mode=MODE.TEST,
                      config_path=Path(__file__).parent.parent.joinpath("data", "config"))

    job1 = Job(process=Process(mode=MODE.TEST, context=context))
    job2 = Job(process=Process(mode=MODE.TEST, context=context))

    pipe = Pipe(units=[job1, job2], execute_type=Pipe.Type.SERIAL)
    output = pipe.execute(Payload())
    assert isinstance(output, Payload)


def test_pipe_execute_parallel():
    context = Context(mode=MODE.TEST,
                      config_path=Path(__file__).parent.parent.joinpath("data", "config"))

    job1 = Job(process=Process(mode=MODE.TEST, context=context))
    job2 = Job(process=Process(mode=MODE.TEST, context=context))

    pipe = Pipe(units=[job1, job2], execute_type=Pipe.Type.PARALLEL)
    output = pipe.execute(Payload())
    assert isinstance(output, Payload)

