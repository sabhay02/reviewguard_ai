from contextlib import ExitStack
from langgraph.checkpoint.sqlite import SqliteSaver

_stack = ExitStack()

import pathlib
pathlib.Path("data").mkdir(parents=True, exist_ok=True)

checkpointer = _stack.enter_context(
    SqliteSaver.from_conn_string("data/reviewguard.db")
)