import dataclasses

@dataclasses.dataclass
class ExecutionCancelToken:
    IsCancellationRequested: bool
