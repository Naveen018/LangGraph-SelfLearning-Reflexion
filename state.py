from mimetypes import init
from typing import TypedDict
from urllib import response
from langgraph.graph import END, StateGraph


class SimpleState(TypedDict):
    count: int
    sum: int
    
def increment(state: SimpleState) -> SimpleState:
    """Increment the count in the state."""
    state['count'] += 1
    state['sum'] += state['count']
    return state    # Can also return a dict like return {'count': state['count'] + 1} 
                    # but this returns only the count disregarding the other state fields.

def should_continue(state: SimpleState):
    """Check if the count is less than 10."""
    if state['count'] < 5:
        return 'increment'
    else:
        return END

graph = StateGraph(SimpleState)

graph.add_node('increment', increment)
graph.set_entry_point('increment')
graph.add_conditional_edges('increment',should_continue)

app = graph.compile()

initial_state = SimpleState(count=0, sum=0)    # It can also be a dict like initial_state = {'count': 0}
response = app.invoke(initial_state)
print(response)  # Should print {'count': 5}
print(response['count'])  # Should print 5
print(response['sum'])  # Should print 15 (1+2+3+4+5)