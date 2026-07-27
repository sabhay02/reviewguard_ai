from contextlib import ExitStack
from langgraph.checkpoint.sqlite import SqliteSaver

_stack = ExitStack()

checkpointer = _stack.enter_context(
    SqliteSaver.from_conn_string("reviewguard.db")
)